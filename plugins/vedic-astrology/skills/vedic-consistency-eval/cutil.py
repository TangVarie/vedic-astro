#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cutil.py —— 跨 skill 一致性校验用的确定性规则【单一来源】。
canonical_facts 的派生 与 一致性检查 共用，保证两边算法一致。

只编码【无争议】的共享锚点：星座主星(宫主) + 经典尊贵度(Exalted/Debilitated/Own)。
不碰 friend/enemy/neutral 的自然友谊表(那需要更细的体系，且各派略有出入)——
非"旺/陷/入庙"一律归 "Other"，一致性检查只在确定类别间判矛盾。
"""

SIGN_NAMES = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]

# 星座主星（index 0=Ar … 11=Pi）
SIGN_LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
             "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

# 入旺星座（1..12）
EXALT = {"Sun": 1, "Moon": 2, "Mars": 10, "Mercury": 6, "Jupiter": 4, "Venus": 12, "Saturn": 7}
# 入陷 = 入旺对宫
DEBIL = {p: ((s + 6 - 1) % 12) + 1 for p, s in EXALT.items()}
# 庙（自己的星座）
OWN = {"Sun": {5}, "Moon": {4}, "Mars": {1, 8}, "Mercury": {3, 6},
       "Jupiter": {9, 12}, "Venus": {2, 7}, "Saturn": {10, 11}}


def house_lords(lagna_sign):
    """由上升星座(1..12) 推 12 宫主。键为字符串 '1'..'12'，值为行星名。"""
    return {str(h): SIGN_LORD[((lagna_sign - 1) + (h - 1)) % 12] for h in range(1, 13)}


def dignity(planet, sign):
    """经典尊贵度：Exalted / Debilitated / Own / Other。节点等无经典尊贵 → Other。"""
    if planet in EXALT and sign == EXALT[planet]:
        return "Exalted"
    if planet in DEBIL and sign == DEBIL[planet]:
        return "Debilitated"
    if planet in OWN and sign in OWN[planet]:
        return "Own"
    return "Other"
