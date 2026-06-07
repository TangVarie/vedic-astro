"""
Yogini Dasha Calculator
========================
基于 KN Rao 传承 / BPHS 标准计算 Yogini Mahadasha + Antardasha。

用法:
  # 给定 Moon Nakshatra 编号 (1-27) 和 Pada (1-4) 与出生日期, 输出完整 MD 序列
  python yogini_dasha.py --nakshatra 7 --pada 2 --birth 1990-05-21 --years 90

  # 或直接给 Moon 在星座内的度数, 让脚本算 Nakshatra/Pada
  python yogini_dasha.py --moon-sign 4 --moon-deg 8.5 --birth 1990-05-21 --years 90

  # 输出 AD（小运）需要额外指定 --include-ad
  python yogini_dasha.py --nakshatra 7 --pada 2 --birth 1990-05-21 --years 90 --include-ad

参考: vedic-timing/resources/yogini_dasha_rules.md
依赖: 仅标准库 (datetime, argparse, json)
"""

from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional

# ────────────────────────────────────────────────────────────────
# Yogini 体系常量
# ────────────────────────────────────────────────────────────────

# 8 个 Yogini 自然顺序 + 时长 + 行星
YOGINI_SEQ = [
    ("Mangala",  "Moon",     1),
    ("Pingala",  "Sun",      2),
    ("Dhanya",   "Jupiter",  3),
    ("Bhramari", "Mars",     4),
    ("Bhadrika", "Mercury",  5),
    ("Ulka",     "Saturn",   6),
    ("Siddha",   "Venus",    7),
    ("Sankata",  "Rahu",     8),
]
YOGINI_NAMES = [y[0] for y in YOGINI_SEQ]
YOGINI_LEN = {y[0]: y[2] for y in YOGINI_SEQ}
YOGINI_PLANET = {y[0]: y[1] for y in YOGINI_SEQ}
YOGINI_NATURE = {
    "Mangala": "auspicious",
    "Pingala": "malefic",
    "Dhanya": "highly auspicious",
    "Bhramari": "malefic",
    "Bhadrika": "auspicious",
    "Ulka": "malefic",
    "Siddha": "highly auspicious",
    "Sankata": "malefic",
}

# Nakshatra → Yogini 索引 (公式 (N + 3) % 8, 其中 N = 1..27)
# 索引说明: remainder 0 → Sankata, 1 → Mangala, 2 → Pingala, ...
REMAINDER_TO_YOGINI = {
    0: "Sankata",
    1: "Mangala",
    2: "Pingala",
    3: "Dhanya",
    4: "Bhramari",
    5: "Bhadrika",
    6: "Ulka",
    7: "Siddha",
}

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "P.Phalguni", "U.Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "P.Ashadha",
    "U.Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "P.Bhadrapada", "U.Bhadrapada", "Revati",
]

NAKSHATRA_SPAN_MIN = 800   # 13°20' = 800 分 (精确, 不用 13.333°)
PADA_SPAN_MIN = 200        # 3°20' = 200 分


# ────────────────────────────────────────────────────────────────
# Nakshatra / Pada 计算
# ────────────────────────────────────────────────────────────────

def moon_position_to_nakshatra(moon_sign: int, moon_deg_in_sign: float) -> tuple[int, int, float]:
    """从 Moon 的星座 (1=Ar..12=Pi) 和星座内度数 → (Nakshatra 编号 1-27, Pada 1-4, Nakshatra 内已走分钟数)
    
    所有距离用 '分' 计算 (避免 3.333 近似误差).
    """
    if not 1 <= moon_sign <= 12:
        raise ValueError(f"moon_sign must be 1-12, got {moon_sign}")
    if not 0 <= moon_deg_in_sign < 30:
        raise ValueError(f"moon_deg_in_sign must be 0-30, got {moon_deg_in_sign}")
    
    absolute_minutes = (moon_sign - 1) * 30 * 60 + moon_deg_in_sign * 60
    nakshatra_idx_0 = int(absolute_minutes // NAKSHATRA_SPAN_MIN)  # 0-26
    minutes_in_nak = absolute_minutes - nakshatra_idx_0 * NAKSHATRA_SPAN_MIN
    pada = int(minutes_in_nak // PADA_SPAN_MIN) + 1  # 1-4
    return nakshatra_idx_0 + 1, pada, minutes_in_nak


def nakshatra_to_yogini(nakshatra_num: int) -> str:
    """Nakshatra (1-27) → 起算 Yogini, 公式 (N + 3) % 8 (KN Rao 派)."""
    if not 1 <= nakshatra_num <= 27:
        raise ValueError(f"nakshatra_num must be 1-27, got {nakshatra_num}")
    remainder = (nakshatra_num + 3) % 8
    return REMAINDER_TO_YOGINI[remainder]


# ────────────────────────────────────────────────────────────────
# 出生时残余 (balance) — 用 Pada 简化估算
# ────────────────────────────────────────────────────────────────
# 严格说: 出生时 balance = (1 - Moon 在 Nakshatra 内已走的比例) × 该 Yogini 总年数
# 这里用 Pada 简化 (KN Rao 教学常用近似): 在 Pada N 中已走 0..200 分钟
# 实际 balance 比例 = 1 - (Nakshatra 内已走分钟 / 800)

def compute_balance_years(starting_yogini: str, minutes_in_nak: float) -> float:
    """出生时第一个 Yogini 还剩多少年.
    
    Moon 在 Nakshatra 内已走的比例 = minutes_in_nak / 800
    剩余比例 = 1 - 已走比例
    残余年数 = 剩余比例 × 该 Yogini 总年数
    """
    total_years = YOGINI_LEN[starting_yogini]
    remaining_ratio = 1.0 - (minutes_in_nak / NAKSHATRA_SPAN_MIN)
    return total_years * remaining_ratio


# ────────────────────────────────────────────────────────────────
# 时长 → 起止日期换算 (1 Yogini 年 = 365.25 天, 简化)
# ────────────────────────────────────────────────────────────────

DAYS_PER_YEAR = 365.25

def years_to_timedelta(years: float) -> timedelta:
    return timedelta(days=years * DAYS_PER_YEAR)


# ────────────────────────────────────────────────────────────────
# MD 序列生成
# ────────────────────────────────────────────────────────────────

@dataclass
class MahadashaPeriod:
    index: int                 # 0-based 序号
    yogini: str
    planet: str
    nature: str
    years: float
    start: str                 # ISO date
    end: str
    is_balance: bool = False   # 是否是出生时残余的第一个 MD


def generate_md_sequence(
    starting_yogini: str,
    balance_years: float,
    birth_date: datetime,
    total_years: float = 90,
) -> List[MahadashaPeriod]:
    """生成从出生到出生后 N 年的完整 MD 序列.
    
    第 1 个 MD = 起算 Yogini 的 balance (残余年数)
    之后按 Yogini 自然顺序循环, 每个 MD 用其完整时长.
    """
    sequence = []
    start_idx = YOGINI_NAMES.index(starting_yogini)
    current_date = birth_date
    i = 0
    cumulative = 0.0
    
    while cumulative < total_years:
        if i == 0:
            # 第一个 MD 是 balance
            yog_name = starting_yogini
            years = balance_years
            is_bal = True
        else:
            # 从下一个 Yogini 开始循环
            yog_idx = (start_idx + i) % 8
            yog_name = YOGINI_NAMES[yog_idx]
            years = YOGINI_LEN[yog_name]
            is_bal = False
        
        end_date = current_date + years_to_timedelta(years)
        sequence.append(MahadashaPeriod(
            index=i,
            yogini=yog_name,
            planet=YOGINI_PLANET[yog_name],
            nature=YOGINI_NATURE[yog_name],
            years=round(years, 4),
            start=current_date.date().isoformat(),
            end=end_date.date().isoformat(),
            is_balance=is_bal,
        ))
        current_date = end_date
        cumulative += years
        i += 1
        if i > 100:  # 防御性退出 (实际不会超过 ~13 个 MD / 90 年)
            break
    
    return sequence


# ────────────────────────────────────────────────────────────────
# AD (Antardasha) — 从 MD 自身开始循环 (v3.4 修正后的顺序)
# ────────────────────────────────────────────────────────────────

@dataclass
class AntardashaPeriod:
    md_index: int              # 所属 MD 序号
    md_yogini: str
    ad_index: int              # 0-based AD 序号 (0..7)
    ad_yogini: str
    ad_planet: str
    months: float
    start: str
    end: str


def generate_ad_for_md(md: MahadashaPeriod) -> List[AntardashaPeriod]:
    """为一个 MD 生成 8 个 AD.
    
    ⚠️ v3.4 规则: AD 从 MD 自身开始, 按自然顺序循环.
    每个 AD 时长 = MD 时长 × (该 AD Yogini 总年数 / 36)
    """
    md_start = datetime.fromisoformat(md.start)
    md_end = datetime.fromisoformat(md.end)
    md_duration_days = (md_end - md_start).days
    
    start_idx = YOGINI_NAMES.index(md.yogini)
    ad_list = []
    current_date = md_start
    
    for i in range(8):
        ad_yog_idx = (start_idx + i) % 8
        ad_yog_name = YOGINI_NAMES[ad_yog_idx]
        ad_proportion = YOGINI_LEN[ad_yog_name] / 36.0
        ad_days = md_duration_days * ad_proportion
        ad_months = (ad_days / DAYS_PER_YEAR) * 12
        
        end_date = current_date + timedelta(days=ad_days)
        ad_list.append(AntardashaPeriod(
            md_index=md.index,
            md_yogini=md.yogini,
            ad_index=i,
            ad_yogini=ad_yog_name,
            ad_planet=YOGINI_PLANET[ad_yog_name],
            months=round(ad_months, 3),
            start=current_date.date().isoformat(),
            end=end_date.date().isoformat(),
        ))
        current_date = end_date
    
    return ad_list


# ────────────────────────────────────────────────────────────────
# 验证 (校验 16: 累计 = 36 年)
# ────────────────────────────────────────────────────────────────

def validate_md_cycle(starting_yogini: str) -> bool:
    """从任一 Yogini 起算, 完整循环 8 个 MD 应累计 36 年."""
    start_idx = YOGINI_NAMES.index(starting_yogini)
    total = sum(YOGINI_LEN[YOGINI_NAMES[(start_idx + i) % 8]] for i in range(8))
    return total == 36


# ────────────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Yogini Dasha calculator (KN Rao / BPHS standard).",
        epilog="参考 vedic-timing/resources/yogini_dasha_rules.md",
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--nakshatra", type=int, help="Moon Nakshatra (1-27, Ashwini=1)")
    src.add_argument("--moon-sign", type=int, help="Moon star sign (1=Aries..12=Pisces)")
    
    parser.add_argument("--pada", type=int, default=1, choices=[1,2,3,4],
                        help="Moon's pada within nakshatra (1-4). Used to estimate balance.")
    parser.add_argument("--moon-deg", type=float, default=None,
                        help="Moon's degree within sign (0-30). Used with --moon-sign. "
                             "Gives more precise balance than --pada.")
    parser.add_argument("--birth", required=True, help="Birth date YYYY-MM-DD")
    parser.add_argument("--years", type=float, default=90,
                        help="How many years of MD to generate (default 90)")
    parser.add_argument("--include-ad", action="store_true",
                        help="Also output Antardasha (sub-period) breakdown")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # 解析 Moon 位置
    if args.nakshatra:
        nak_num = args.nakshatra
        # 用 pada 估算 Nakshatra 内位置 (取该 pada 的中点)
        minutes_in_nak = (args.pada - 0.5) * PADA_SPAN_MIN
        pada = args.pada
    else:
        if args.moon_deg is None:
            print("Error: --moon-sign requires --moon-deg", file=sys.stderr)
            sys.exit(1)
        nak_num, pada, minutes_in_nak = moon_position_to_nakshatra(args.moon_sign, args.moon_deg)
    
    if not 1 <= nak_num <= 27:
        print(f"Error: nakshatra out of range: {nak_num}", file=sys.stderr)
        sys.exit(1)
    
    starting_yog = nakshatra_to_yogini(nak_num)
    balance = compute_balance_years(starting_yog, minutes_in_nak)
    birth_dt = datetime.strptime(args.birth, "%Y-%m-%d")
    
    # 校验
    assert validate_md_cycle(starting_yog), "Yogini MD 累计 != 36 年, 计算错误"
    
    md_seq = generate_md_sequence(starting_yog, balance, birth_dt, args.years)
    
    if args.json:
        out = {
            "input": {
                "nakshatra_num": nak_num,
                "nakshatra_name": NAKSHATRA_NAMES[nak_num - 1],
                "pada": pada,
                "minutes_in_nakshatra": round(minutes_in_nak, 2),
                "birth_date": args.birth,
            },
            "starting_yogini": starting_yog,
            "starting_planet": YOGINI_PLANET[starting_yog],
            "balance_years": round(balance, 4),
            "mahadashas": [asdict(m) for m in md_seq],
        }
        if args.include_ad:
            out["antardashas"] = []
            for md in md_seq:
                out["antardashas"].extend(asdict(a) for a in generate_ad_for_md(md))
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    
    # 文本输出
    print(f"# Yogini Dasha 计算结果")
    print(f"# Moon Nakshatra: {nak_num} ({NAKSHATRA_NAMES[nak_num - 1]}), Pada {pada}")
    print(f"# Nakshatra 内已走: {minutes_in_nak:.1f}' / 800'  ({minutes_in_nak/8:.1f}%)")
    print(f"# 出生日期: {args.birth}")
    print(f"# 起算 Yogini: {starting_yog} ({YOGINI_PLANET[starting_yog]}, {YOGINI_LEN[starting_yog]} 年, {YOGINI_NATURE[starting_yog]})")
    print(f"# 出生时残余: {balance:.3f} 年 (= {balance * 12:.1f} 个月)")
    print()
    print(f"{'#':>3} {'Yogini':<10} {'Planet':<9} {'Years':>7}  {'Start':<12} {'End':<12} {'Note':<10}")
    print("-" * 78)
    for md in md_seq:
        note = "← balance" if md.is_balance else ""
        print(f"{md.index:>3} {md.yogini:<10} {md.planet:<9} {md.years:>7.3f}  {md.start:<12} {md.end:<12} {note}")
    
    if args.include_ad:
        print()
        print(f"## Antardasha (AD) breakdown")
        print(f"⚠️ AD 顺序: 每个 MD 内, AD 从 MD 自身开始, 按自然顺序循环 (v3.4 修正后).")
        for md in md_seq[:3]:  # 只详细列前 3 个 MD, 避免输出过长
            print()
            print(f"### MD {md.index}: {md.yogini} ({md.start} ~ {md.end})")
            print(f"{'AD#':>4} {'Yogini':<10} {'Planet':<9} {'Months':>8}  {'Start':<12} {'End':<12}")
            print("-" * 65)
            for ad in generate_ad_for_md(md):
                print(f"{ad.ad_index:>4} {ad.ad_yogini:<10} {ad.ad_planet:<9} {ad.months:>8.2f}  {ad.start:<12} {ad.end:<12}")
        if len(md_seq) > 3:
            print()
            print(f"... ({len(md_seq) - 3} more MDs, use --json for full output)")


if __name__ == "__main__":
    main()
