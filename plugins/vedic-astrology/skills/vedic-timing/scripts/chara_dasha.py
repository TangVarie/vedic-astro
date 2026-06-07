"""
Jaimini Chara Dasha Calculator
================================
基于 KN Rao 简化 odd/even Lagna 方向规则计算 Jaimini Chara Mahadasha.

⚠️ 流派说明: 
  本脚本采用 KN Rao 主流变体 — odd/even Lagna 决定方向, 
  Scorpio/Aquarius 双主取较近 (Mars vs Ketu / Saturn vs Rahu).
  其他变体 (Savya/Apasavya, Rangacharya, SJC, PVR) 未实现 — 
  若用户软件采用其他算法, 先核对流派, 不要直接判为脚本错误.
  参考: vedic-timing/resources/chara_dasha_rules.md

用法:
  python chara_dasha.py --lagna Aries --positions positions.json --birth 1990-05-21
  
  positions.json 格式 (8 行星 + Lagna 各自在哪个星座):
  {
    "Lagna":   "Aries",
    "Sun":     "Aries",
    "Moon":    "Gemini",
    "Mars":    "Leo",
    "Mercury": "Pisces",
    "Jupiter": "Sagittarius",
    "Venus":   "Capricorn",
    "Saturn":  "Aquarius",
    "Rahu":    "Aquarius",
    "Ketu":    "Leo"
  }
  
  或者直接命令行传:
  python chara_dasha.py --lagna Aries --birth 1990-05-21 \
    --sun Aries --moon Gemini --mars Leo --mercury Pisces \
    --jupiter Sagittarius --venus Capricorn --saturn Aquarius \
    --rahu Aquarius --ketu Leo

依赖: 仅标准库.
"""

from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple

# ────────────────────────────────────────────────────────────────
# 星座 / 主星常量
# ────────────────────────────────────────────────────────────────

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
SIGN_IDX = {s: i for i, s in enumerate(SIGNS)}  # 0-based

# 每个星座的主星 (含 Scorpio/Aquarius 副主)
SIGN_LORDS = {
    "Aries":       ["Mars"],
    "Taurus":      ["Venus"],
    "Gemini":      ["Mercury"],
    "Cancer":      ["Moon"],
    "Leo":         ["Sun"],
    "Virgo":       ["Mercury"],
    "Libra":       ["Venus"],
    "Scorpio":     ["Mars", "Ketu"],      # Mars 主, Ketu 副 (KN Rao)
    "Sagittarius": ["Jupiter"],
    "Capricorn":   ["Saturn"],
    "Aquarius":    ["Saturn", "Rahu"],    # Saturn 主, Rahu 副
    "Pisces":      ["Jupiter"],
}

# Lagna 奇偶判定 (1-index): Aries=1 奇, Taurus=2 偶, ...
# 在 0-index 下: Aries=0 是奇 (1), Taurus=1 是偶 (2), ...
# 所以 0-index 奇偶判定: index % 2 == 0 → 奇数星座 → 顺行
def is_odd_sign_0idx(sign_idx_0: int) -> bool:
    """0-index 下的奇数星座 = 1-index 的奇数 = 顺行."""
    return sign_idx_0 % 2 == 0


# ────────────────────────────────────────────────────────────────
# 距离计算
# ────────────────────────────────────────────────────────────────

def distance(from_idx: int, to_idx: int, forward: bool) -> int:
    """计算两星座之间的距离 (含终点不含起点).
    
    顺行: 从 from 走到 to, 计步数. 同宫 = 12.
    逆行: 从 from 逆向走到 to, 计步数. 同宫 = 12.
    """
    if forward:
        d = (to_idx - from_idx) % 12
    else:
        d = (from_idx - to_idx) % 12
    return d if d != 0 else 12


def compute_md_years(
    sign: str, planet_positions: Dict[str, str], forward: bool,
) -> Tuple[int, str, str]:
    """计算某个星座作为 MD 时的时长 (年).
    
    时长 = 从该大运星座数到其主星所在星座的距离 (含终点不含起点; 同宫 = 12).
    Scorpio/Aquarius 双主时取较近 (较短距离 = KN Rao 先到优先).
    
    返回: (years, used_lord, lord_position)
    
    实现细节:
      顺行: from=sign, to=lord, 顺数;
      逆行: from=sign, to=lord, 反向数.
    """
    sign_idx = SIGN_IDX[sign]
    lords = SIGN_LORDS[sign]
    
    distances = []
    for lord in lords:
        if lord not in planet_positions:
            raise ValueError(f"Position of {lord} not provided")
        lord_sign = planet_positions[lord]
        if lord_sign not in SIGN_IDX:
            raise ValueError(f"Unknown sign for {lord}: {lord_sign}")
        lord_idx = SIGN_IDX[lord_sign]
        # 从 sign 到 lord 的距离 (含终点不含起点; 同宫 = 12)
        d = distance(sign_idx, lord_idx, forward)
        distances.append((lord, lord_sign, d))
    
    # 取较近 (较短) — KN Rao 先到优先
    chosen = min(distances, key=lambda x: x[2])
    return chosen[2], chosen[0], chosen[1]  # (years, used_lord, lord_position)


# ────────────────────────────────────────────────────────────────
# 完整 MD 序列生成
# ────────────────────────────────────────────────────────────────

DAYS_PER_YEAR = 365.25

@dataclass
class CharaMD:
    index: int
    sign: str
    years: int
    used_lord: str        # 实际计算用的主星 (Scorpio/Aquarius 时显示哪个主胜出)
    lord_position: str    # 该主星所在星座
    start: str
    end: str


def generate_chara_md_sequence(
    lagna: str,
    planet_positions: Dict[str, str],
    birth_date: datetime,
    max_years: Optional[float] = None,
) -> List[CharaMD]:
    """从 Lagna 起算完整 12 个 Chara MD (一个 Chara Dasha 循环).
    
    起运 = Lagna 星座.
    方向 = Lagna 奇偶判定 (1-index 奇 → 顺, 偶 → 逆).
    
    max_years 行为 (v3.4 修订):
      None (默认): 始终输出完整 12 个 MD, 不提前截断.
                   即使累计超过 100/120 年也照样输出 — Chara 循环就是 12 个 MD,
                   累计可达 144 年.
      数值:        仅当用户显式希望按年龄截断 (例如只想看前 80 年) 时设置.
    
    ⚠️ 旧版默认 max_years=100 + 累计 >= 100 即 break, 会导致某些盘
       在第 11 个 MD 就停止输出, 与"完整循环 12 MD"语义不一致.
       v3.4 修复.
    """
    lagna_idx = SIGN_IDX[lagna]
    forward = is_odd_sign_0idx(lagna_idx)
    
    sequence = []
    current_idx = lagna_idx
    current_date = birth_date
    cumulative = 0.0
    
    for i in range(12):
        sign = SIGNS[current_idx]
        years, used_lord, lord_pos = compute_md_years(sign, planet_positions, forward)
        end_date = current_date + timedelta(days=years * DAYS_PER_YEAR)
        
        sequence.append(CharaMD(
            index=i,
            sign=sign,
            years=years,
            used_lord=used_lord,
            lord_position=lord_pos,
            start=current_date.date().isoformat(),
            end=end_date.date().isoformat(),
        ))
        
        current_date = end_date
        cumulative += years
        
        # 下一个星座 (同方向)
        if forward:
            current_idx = (current_idx + 1) % 12
        else:
            current_idx = (current_idx - 1) % 12
        
        # 仅当用户显式指定 max_years 时才提前截断
        if max_years is not None and cumulative >= max_years:
            break
    
    return sequence


# ────────────────────────────────────────────────────────────────
# AD (Antardasha) — 简化均分版
# ────────────────────────────────────────────────────────────────

@dataclass
class CharaAD:
    md_index: int
    md_sign: str
    ad_index: int
    ad_sign: str
    months: float
    start: str
    end: str


def generate_ad_for_md(md: CharaMD, forward: bool) -> List[CharaAD]:
    """为一个 Chara MD 生成 12 个 AD (简化均分版, ±2 个月精度).
    
    AD 顺序: 从 MD 自身开始, 按 MD 同方向循环 12 个星座.
    AD 时长 ≈ MD 时长 / 12.
    """
    md_start = datetime.fromisoformat(md.start)
    md_end = datetime.fromisoformat(md.end)
    md_days = (md_end - md_start).days
    ad_days = md_days / 12
    ad_months = (ad_days / DAYS_PER_YEAR) * 12
    
    md_sign_idx = SIGN_IDX[md.sign]
    ad_list = []
    current_date = md_start
    
    for i in range(12):
        if forward:
            ad_idx = (md_sign_idx + i) % 12
        else:
            ad_idx = (md_sign_idx - i) % 12
        ad_sign = SIGNS[ad_idx]
        end_date = current_date + timedelta(days=ad_days)
        ad_list.append(CharaAD(
            md_index=md.index,
            md_sign=md.sign,
            ad_index=i,
            ad_sign=ad_sign,
            months=round(ad_months, 2),
            start=current_date.date().isoformat(),
            end=end_date.date().isoformat(),
        ))
        current_date = end_date
    
    return ad_list


# ────────────────────────────────────────────────────────────────
# 校验
# ────────────────────────────────────────────────────────────────

def validate_total(seq: List[CharaMD]) -> dict:
    """校验 14/15a/15b: Chara MD 起算 / MD 数 / 累计年数.
    
    校验 14:  起算 = Lagna (由调用方在生成 seq 时保证, 此处不重算)
    校验 15a: MD 数 = 12 (完整循环, 硬校验)
    校验 15b: 累计 80-144 年 (软警戒)
              典型样例多落 90-110, 极端可接近 144.
              ⚠️ 80 不是绝对下限 — Chara MD 每段 1-12 年, 完整 12 段
                 理论上未必 ≥ 80. 累计 < 80 时不直接判错, 标记为 atypical,
                 让用户核对流派 / 双主处理 / 软件输出.
    """
    total = sum(md.years for md in seq)
    in_typical = 80 <= total <= 144
    return {
        "total_years": total,
        "md_count": len(seq),
        "md_count_ok": len(seq) == 12,
        "in_typical_range_80_144": in_typical,
        "atypical": not in_typical,
    }


# ────────────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────────────

def load_positions(args) -> Dict[str, str]:
    if args.positions:
        with open(args.positions) as f:
            return json.load(f)
    
    required = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]
    out = {"Lagna": args.lagna}
    for r in required:
        val = getattr(args, r)
        if not val:
            print(f"Error: --{r} or --positions required", file=sys.stderr)
            sys.exit(1)
        out[r.capitalize()] = val
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Jaimini Chara Dasha calculator (KN Rao simplified rules).",
        epilog="参考 vedic-timing/resources/chara_dasha_rules.md. "
               "其他流派 (Savya/Apasavya, SJC 等) 未实现.",
    )
    parser.add_argument("--lagna", required=True, choices=SIGNS, help="Ascendant sign")
    parser.add_argument("--birth", required=True, help="Birth date YYYY-MM-DD")
    parser.add_argument("--positions", help="JSON file with planetary positions")
    parser.add_argument("--sun", choices=SIGNS, help="Sun's sign")
    parser.add_argument("--moon", choices=SIGNS, help="Moon's sign")
    parser.add_argument("--mars", choices=SIGNS, help="Mars's sign")
    parser.add_argument("--mercury", choices=SIGNS, help="Mercury's sign")
    parser.add_argument("--jupiter", choices=SIGNS, help="Jupiter's sign")
    parser.add_argument("--venus", choices=SIGNS, help="Venus's sign")
    parser.add_argument("--saturn", choices=SIGNS, help="Saturn's sign")
    parser.add_argument("--rahu", choices=SIGNS, help="Rahu's sign")
    parser.add_argument("--ketu", choices=SIGNS, help="Ketu's sign")
    parser.add_argument("--max-years", type=float, default=None,
                        help="Max years of MD to generate. Default: None = output "
                             "all 12 MDs (complete Chara Dasha cycle, ~80-144 years). "
                             "Set explicitly only if you want to truncate by age.")
    parser.add_argument("--include-ad", action="store_true",
                        help="Also output AD (sub-period) breakdown for first 3 MDs")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    positions = load_positions(args)
    birth_dt = datetime.strptime(args.birth, "%Y-%m-%d")
    lagna_idx = SIGN_IDX[args.lagna]
    forward = is_odd_sign_0idx(lagna_idx)
    
    md_seq = generate_chara_md_sequence(args.lagna, positions, birth_dt, args.max_years)
    validation = validate_total(md_seq)
    
    if args.json:
        out = {
            "input": {
                "lagna": args.lagna,
                "lagna_1idx": lagna_idx + 1,
                "direction": "forward (顺行)" if forward else "reverse (逆行)",
                "scheme": "KN Rao simplified (odd/even Lagna)",
                "birth_date": args.birth,
                "positions": positions,
            },
            "mahadashas": [asdict(m) for m in md_seq],
            "validation": validation,
        }
        if args.include_ad:
            out["antardashas_first_3_mds"] = []
            for md in md_seq[:3]:
                out["antardashas_first_3_mds"].extend(asdict(a) for a in generate_ad_for_md(md, forward))
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    
    print(f"# Jaimini Chara Dasha 计算结果")
    print(f"# Lagna: {args.lagna} (1-index: {lagna_idx + 1}, {'奇数 → 顺行' if forward else '偶数 → 逆行'})")
    print(f"# 流派: KN Rao 简化 odd/even Lagna 规则")
    print(f"# 出生日期: {args.birth}")
    print()
    print(f"行星位置:")
    for k in ["Lagna", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        print(f"  {k:<8} → {positions.get(k, '(missing)')}")
    print()
    print(f"{'#':>3} {'Sign':<14} {'Years':>5}  {'Used Lord':<20} {'Start':<12} {'End':<12}")
    print("-" * 82)
    for md in md_seq:
        lord_note = f"{md.used_lord} in {md.lord_position}"
        print(f"{md.index:>3} {md.sign:<14} {md.years:>5}  {lord_note:<20} {md.start:<12} {md.end:<12}")
    
    print()
    print(f"## 校验")
    print(f"  累计年数:   {validation['total_years']}")
    print(f"  MD 数:      {validation['md_count']}")
    print(f"  校验 14:    起算 = Lagna ({args.lagna})  ✓ (脚本保证)")
    print(f"  校验 15a:   MD 数 = 12 (完整循环):  {'✓' if validation['md_count_ok'] else '✗ 仅 ' + str(validation['md_count']) + ' 个'}")
    if validation['in_typical_range_80_144']:
        print(f"  校验 15b:   累计在典型区间 80-144 年:  ✓")
    else:
        print(f"  校验 15b:   累计 {validation['total_years']} 年 — atypical (典型 80-144)")
        print(f"               ⚠️ 不直接判错, 完整 12 MD 已输出. 请核对:")
        print(f"               - 流派 (本脚本用 KN Rao 简化 odd/even Lagna 规则)")
        print(f"               - Scorpio/Aquarius 双主处理 (取较近, 见上方表)")
        print(f"               - 与 JHora 等占星软件的输出是否一致")
    
    if args.include_ad:
        print()
        print(f"## AD (前 3 个 MD)")
        print(f"⚠️ AD 顺序: 从 MD 自身开始, 同方向循环 12 个星座.")
        for md in md_seq[:3]:
            print()
            print(f"### MD {md.index}: {md.sign} ({md.start} ~ {md.end})")
            print(f"{'AD#':>4} {'Sign':<14} {'Months':>7}  {'Start':<12} {'End':<12}")
            print("-" * 58)
            for ad in generate_ad_for_md(md, forward):
                print(f"{ad.ad_index:>4} {ad.ad_sign:<14} {ad.months:>7.2f}  {ad.start:<12} {ad.end:<12}")


if __name__ == "__main__":
    main()
