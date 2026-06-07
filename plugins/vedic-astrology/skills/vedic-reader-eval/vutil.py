#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vutil.py —— 确定性占星公式的【单一来源】。
gen_example.py / check_invariants.py / score_extraction.py 全部从这里 import，
保证"生成真值"和"校验提取"用的是同一套公式，不会各算各的。

公式出处：vedic-reader/SKILL.md
  - D9：navamsa 每份 = 3°20' = 10/3 度(200 分)，不是 3.333 近似
  - Nakshatra：每个 13°20' = 40/3 度；pada 每个 3°20' = 10/3 度
  - Chara Karaka：按宫内度降序；Rahu 用 30 - 宫内度(逆向)
"""

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
SIGN_NAMES = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]

# Vimshottari 大运周期常数(年)；总和必须 = 120
VIMSHOTTARI = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
               "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

# 恒为逆行 / 恒不逆行 的确定性事实
ALWAYS_RETRO = ("Rahu", "Ketu")
NEVER_RETRO = ("Sun", "Moon")


def lon_from(sign, deg_in_sign):
    """由 星座(1..12) + 宫内度 还原黄道经度(0..360)。"""
    return (int(sign) - 1) * 30.0 + float(deg_in_sign)


def sign_of(lon):
    return int(lon // 30) + 1


def deg_in_sign(lon):
    return lon % 30.0


def nakshatra_of(lon):
    return int(lon // (40.0 / 3.0)) + 1


def pada_of(lon):
    return int((lon % (40.0 / 3.0)) // (10.0 / 3.0)) + 1


def d9_sign_of(lon):
    nav_index = int(lon // (10.0 / 3.0))
    return (nav_index % 12) + 1


def karaka_degree(planet, dis):
    """Chara Karaka 用度数：Rahu 取 30 - 宫内度(逆向)，其余取宫内度。"""
    return (30.0 - dis) if planet == "Rahu" else dis


def chara_karaka_order(d1, scheme="8K"):
    """
    返回按 karaka 度数降序排好的行星列表。
    只计算【确定性排序】，不裁决 7K/8K 的梵文角色命名(那是 vedic-reader 的职责)。
    7K = 不含 Rahu；8K = 含 Rahu。AK = 列表第一(度数最高)，无争议。
    """
    grahas = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    if scheme == "8K":
        grahas = grahas + ["Rahu"]
    scored = [(p, karaka_degree(p, d1[p]["deg_in_sign"])) for p in grahas]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [p for p, _ in scored]
