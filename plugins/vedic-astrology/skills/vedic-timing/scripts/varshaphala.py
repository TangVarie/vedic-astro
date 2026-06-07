"""
Varshaphala (Annual Chart) Calculator
=======================================
基于 Tajaka 体系的年盘核心计算: Muntha + Year Lord 候选评分.

⚠️ 本脚本是简化版:
  - Muntha 计算 (生日年度的进运 Lagna) - 完整实现
  - Year Lord 候选 + 5-Vargiya Bala 简化评分 - 部分实现 (Kshetra + Uchcha)
  - 太阳回归时刻 (年盘起算) - 需要 ephem, 本脚本提供生日近似
  - Sahams (16 个核心 + 罕见扩展) - 脚本未实现, 见 resources/sahams.md 公式手算
    或由 JHora 提取

完整年盘需要补充 Hadda Bala / Drekkana Bala / Navamsa Bala — 这三项依赖
年盘的真实行星位置, 必须由占星软件 (JHora) 提供.

用法:
  # 仅 Muntha:
  python varshaphala.py --lagna Aries --age 28
  python varshaphala.py --lagna Pisces --age 0     # 边界测试: 应得 Pisces

  # Muntha + Year Lord 简化评分 (需要年盘行星尊贵度):
  python varshaphala.py --lagna Aries --age 28 \
    --year-lagna Cancer --year-chart year_chart.json

依赖: 仅标准库.
"""

from __future__ import annotations
import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
SIGN_IDX = {s: i for i, s in enumerate(SIGNS)}

SIGN_RULER = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# 入旺 / 入陷 (Exaltation / Debilitation)
EXALTATION = {
    "Sun":     ("Aries",       10),
    "Moon":    ("Taurus",      3),
    "Mars":    ("Capricorn",   28),
    "Mercury": ("Virgo",       15),
    "Jupiter": ("Cancer",      5),
    "Venus":   ("Pisces",      27),
    "Saturn":  ("Libra",       20),
}
DEBILITATION = {p: (SIGNS[(SIGN_IDX[s] + 6) % 12], d) for p, (s, d) in EXALTATION.items()}

# 入庙 (Own Sign)
OWN_SIGNS = {
    "Sun":     ["Leo"],
    "Moon":    ["Cancer"],
    "Mars":    ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Venus":   ["Taurus", "Libra"],
    "Saturn":  ["Capricorn", "Aquarius"],
}

# 友/敌 (Parashari 自然关系, 简化版)
FRIENDS = {
    "Sun":     ["Moon", "Mars", "Jupiter"],
    "Moon":    ["Sun", "Mercury"],
    "Mars":    ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus":   ["Mercury", "Saturn"],
    "Saturn":  ["Mercury", "Venus"],
}
ENEMIES = {
    "Sun":     ["Venus", "Saturn"],
    "Moon":    [],  # Moon 无敌
    "Mars":    ["Mercury"],
    "Mercury": ["Moon"],
    "Jupiter": ["Mercury", "Venus"],
    "Venus":   ["Sun", "Moon"],
    "Saturn":  ["Sun", "Moon", "Mars"],
}


# ────────────────────────────────────────────────────────────────
# Muntha 计算 (v3.4 安全 1-index 公式)
# ────────────────────────────────────────────────────────────────

def compute_muntha(natal_lagna: str, age: int) -> Dict:
    """计算 Muntha 星座 (进运 Lagna).
    
    公式: Muntha 星座号 = ((natal Lagna 星座号 - 1 + age) % 12) + 1
    
    用 1-index 安全形式, 避免 Pisces=12 + age=0 时回到 0 的边界 bug.
    """
    if natal_lagna not in SIGN_IDX:
        raise ValueError(f"Unknown Lagna: {natal_lagna}")
    if age < 0:
        raise ValueError(f"Age must be >= 0, got {age}")
    
    natal_idx_1 = SIGN_IDX[natal_lagna] + 1   # 1-12
    muntha_idx_1 = ((natal_idx_1 - 1 + age) % 12) + 1
    muntha_sign = SIGNS[muntha_idx_1 - 1]
    return {
        "natal_lagna": natal_lagna,
        "natal_lagna_1idx": natal_idx_1,
        "age": age,
        "muntha_sign": muntha_sign,
        "muntha_1idx": muntha_idx_1,
        "muntha_ruler": SIGN_RULER[muntha_sign],
    }


def muntha_in_year_chart_house(muntha_sign: str, year_lagna: str) -> int:
    """Muntha 在年盘的哪一宫 (1-12).
    
    宫位 = (Muntha sign 0-idx - year Lagna 0-idx) % 12 + 1
    """
    if year_lagna not in SIGN_IDX:
        raise ValueError(f"Unknown year_lagna: {year_lagna}")
    diff = (SIGN_IDX[muntha_sign] - SIGN_IDX[year_lagna]) % 12
    return diff + 1


# 12 宫主题 (简化)
MUNTHA_HOUSE_THEMES = {
    1: "自我重塑年 — 身份切换 / 健康活力",
    2: "财富 / 家庭 / 言语年",
    3: "勇气 / 沟通 / 兄弟年 — 准备期",
    4: "家庭 / 不动产 / 母亲年",
    5: "创造 / 恋爱 / 子女 / 教育年 — 通常吉",
    6: "竞争 / 健康 / 工作压力年 — 经典凶位",
    7: "伴侣 / 合伙 / 合作年",
    8: "转化 / 危机 / 遗产 / 隐藏事件 — 经典凶位",
    9: "导师 / 远方 / 运气 / 灵性年 — 极吉",
    10: "事业巅峰 / 责任年",
    11: "收入 / 社交 / 目标实现年 — 经典最吉",
    12: "灵性 / 隐居 / 损耗 / 海外年",
}


# ────────────────────────────────────────────────────────────────
# Year Lord 候选评分 (简化版: Kshetra + Uchcha)
# ────────────────────────────────────────────────────────────────

def compute_kshetra_bala(planet: str, planet_sign: str) -> int:
    """Kshetra Bala (领地力量) 0-5 分.
    
    入旺=5 / 入庙=4 / 友星=3 / 中性=2 / 敌星=1 / 入陷=0
    """
    if planet in EXALTATION and EXALTATION[planet][0] == planet_sign:
        return 5
    if planet in OWN_SIGNS and planet_sign in OWN_SIGNS[planet]:
        return 4
    if planet in DEBILITATION and DEBILITATION[planet][0] == planet_sign:
        return 0
    
    sign_ruler = SIGN_RULER[planet_sign]
    if sign_ruler == planet:
        return 4  # 自己主导, 等同 own sign
    if sign_ruler in FRIENDS.get(planet, []):
        return 3
    if sign_ruler in ENEMIES.get(planet, []):
        return 1
    return 2


def compute_uchcha_bala(planet: str, planet_sign: str, deg_in_sign: float) -> float:
    """Uchcha Bala (高位力量) 0-5 分.
    
    距离精确入旺点的角度 → 力量.
    0° (精确入旺) = 5, 180° (精确入陷) = 0, 线性插值.
    """
    if planet not in EXALTATION:
        return 2.5  # 中性 (Rahu/Ketu 不参与)
    exalt_sign, exalt_deg = EXALTATION[planet]
    # 行星绝对经度
    planet_abs = SIGN_IDX[planet_sign] * 30 + deg_in_sign
    exalt_abs = SIGN_IDX[exalt_sign] * 30 + exalt_deg
    # 短弧距离
    diff = abs(planet_abs - exalt_abs)
    if diff > 180:
        diff = 360 - diff
    return round(5.0 * (1.0 - diff / 180.0), 2)


def score_year_lord_candidates(year_chart: Dict[str, Dict]) -> List[Dict]:
    """对 Year Lord 候选行星做简化评分.
    
    year_chart 格式: {"Sun": {"sign": "Aries", "deg": 12.5}, ...}
    候选: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn (Rahu/Ketu 不参与).
    
    本简化版只计 Kshetra + Uchcha 两项 (max 10 分).
    完整 25 分版需要 Hadda / Drekkana / Navamsa 三项, 依赖年盘真实分盘.
    """
    candidates = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    scores = []
    for p in candidates:
        if p not in year_chart:
            continue
        sign = year_chart[p].get("sign")
        deg = year_chart[p].get("deg", 15.0)
        if sign not in SIGN_IDX:
            continue
        kshetra = compute_kshetra_bala(p, sign)
        uchcha = compute_uchcha_bala(p, sign, deg)
        total = kshetra + uchcha
        scores.append({
            "planet": p,
            "year_chart_sign": sign,
            "year_chart_deg": deg,
            "kshetra_bala": kshetra,
            "uchcha_bala": uchcha,
            "simplified_total": round(total, 2),
            "missing_metrics": ["Hadda Bala", "Drekkana Bala", "Navamsa Bala"],
        })
    
    scores.sort(key=lambda x: -x["simplified_total"])
    return scores


# ────────────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Varshaphala (Tajaka annual chart) — Muntha + Year Lord scoring.",
        epilog="完整年盘需要 Hadda/Drekkana/Navamsa 三项, 见 varshaphala_rules.md",
    )
    parser.add_argument("--lagna", required=True, choices=SIGNS,
                        help="Natal Lagna sign (本盘 Lagna)")
    parser.add_argument("--age", required=True, type=int,
                        help="Age at year start (该年生日时的年龄)")
    parser.add_argument("--year-lagna", choices=SIGNS,
                        help="Year chart Lagna (年盘 Lagna). 若提供, 会算 Muntha 在年盘的宫位.")
    parser.add_argument("--year-chart", type=str,
                        help='JSON file with year chart planetary positions, '
                             'e.g. {"Sun":{"sign":"Aries","deg":12.5},...}. '
                             "若提供, 会算 Year Lord 候选评分.")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    out = {"muntha": compute_muntha(args.lagna, args.age)}
    
    if args.year_lagna:
        muntha_sign = out["muntha"]["muntha_sign"]
        muntha_house = muntha_in_year_chart_house(muntha_sign, args.year_lagna)
        out["muntha_in_year_chart"] = {
            "year_lagna": args.year_lagna,
            "muntha_house": muntha_house,
            "theme": MUNTHA_HOUSE_THEMES[muntha_house],
        }
    
    if args.year_chart:
        with open(args.year_chart) as f:
            yc = json.load(f)
        out["year_lord_candidates"] = score_year_lord_candidates(yc)
        out["year_lord_note"] = (
            "简化版评分 (Kshetra + Uchcha, max 10). 完整版需要 Hadda + Drekkana + Navamsa "
            "三项, 依赖年盘真实分盘数据 — 请由 JHora 等软件提供并人工核对."
        )
    
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    
    print("# Varshaphala (Tajaka 年盘) 计算结果\n")
    print(f"## Muntha (进运 Lagna)")
    m = out["muntha"]
    print(f"  本盘 Lagna:    {m['natal_lagna']} (1-idx: {m['natal_lagna_1idx']})")
    print(f"  年龄:          {m['age']}")
    print(f"  Muntha 星座:   {m['muntha_sign']} (1-idx: {m['muntha_1idx']})")
    print(f"  Muntha 主:     {m['muntha_ruler']}")
    print(f"  公式:          ((Lagna_1idx - 1 + age) % 12) + 1")
    print(f"                = (({m['natal_lagna_1idx']} - 1 + {m['age']}) % 12) + 1")
    print(f"                = {m['muntha_1idx']} → {m['muntha_sign']}")
    
    if "muntha_in_year_chart" in out:
        my = out["muntha_in_year_chart"]
        print(f"\n## Muntha 在年盘的宫位")
        print(f"  年盘 Lagna: {my['year_lagna']}")
        print(f"  Muntha 落在: 第 {my['muntha_house']} 宫")
        print(f"  主题: {my['theme']}")
    
    if "year_lord_candidates" in out:
        print(f"\n## Year Lord 候选评分 (简化版)")
        print(f"  ⚠️ {out['year_lord_note']}")
        print()
        print(f"  {'Rank':>4}  {'Planet':<8} {'In Sign':<12} {'Kshetra':>7} {'Uchcha':>7} {'Total':>7}")
        print("  " + "-" * 55)
        for i, s in enumerate(out["year_lord_candidates"], 1):
            print(f"  {i:>4}  {s['planet']:<8} {s['year_chart_sign']:<12} "
                  f"{s['kshetra_bala']:>7} {s['uchcha_bala']:>7} {s['simplified_total']:>7}")
        if out["year_lord_candidates"]:
            winner = out["year_lord_candidates"][0]
            print(f"\n  → 简化版 Year Lord 提名: {winner['planet']} "
                  f"({winner['simplified_total']}/10 简化分)")
            print(f"    完整判定需补 3 项 Bala — 请用 JHora 输出补全后再确认.")


if __name__ == "__main__":
    main()
