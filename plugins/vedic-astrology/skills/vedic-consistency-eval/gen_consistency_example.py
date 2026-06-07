#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_consistency_example.py —— 造一份可跑通的一致性示例。

复用 ① (vedic-reader-eval) 那张示例盘的 ground_truth.json，
派生出 canonical_facts.json（这是"源数据真相"），
再造 4 份 skill_claims（core/career/love/soul），其中 career 故意注入 2 个矛盾。

你自己用时不需要这个脚本：
  - canonical_facts.json 由 reader 的 structured_data.md 蒸馏而来；
  - skill_claims_*.json 由各 skill 的输出中抽取确定性主张而来。
两者都可让 Claude 按 schema.md 归一化。
"""
import json, os, copy
from cutil import SIGN_NAMES, house_lords, dignity

# ① 示例盘真值的位置（若不在则用内置回退）
SRC_CANDIDATES = [
    "/home/claude/vedic-reader-eval/fixtures/example_chart/ground_truth.json",
    os.path.join(os.path.dirname(__file__), "..", "vedic-reader-eval",
                 "fixtures", "example_chart", "ground_truth.json"),
]
PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


def load_src():
    for p in SRC_CANDIDATES:
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8"))
    # 回退：与 ① 示例一致的最小数据
    return {
        "chart_id": "example_template_1990",
        "d1": {"Sun": {"sign": 2}, "Moon": {"sign": 11}, "Mars": {"sign": 12},
               "Mercury": {"sign": 2}, "Jupiter": {"sign": 3}, "Venus": {"sign": 1},
               "Saturn": {"sign": 10}, "Lagna": {"sign": 4}},
        "d9": {"Lagna": 9},
        "chara_karaka": {"ak": "Sun"},
        "vimshottari": [{"lord": "Venus", "start": "1989-01-01", "years": 20},
                        {"lord": "Sun", "start": "2009-01-01", "years": 6}],
    }


def build_canonical(src):
    lagna_sign = src["d1"]["Lagna"]["sign"]
    planet_sign = {p: src["d1"][p]["sign"] for p in PLANETS}
    return {
        "chart_id": src.get("chart_id", "example"),
        "ak": src.get("chara_karaka", {}).get("ak"),
        "d9_lagna": src.get("d9", {}).get("Lagna"),
        "house_lords": house_lords(lagna_sign),
        "planet_sign": planet_sign,
        "planet_dignity": {p: dignity(p, planet_sign[p]) for p in PLANETS},
        "dasha": src.get("vimshottari", []),
    }


def main():
    src = load_src()
    canon = build_canonical(src)
    fdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "example_chart")
    os.makedirs(fdir, exist_ok=True)
    json.dump(canon, open(os.path.join(fdir, "canonical_facts.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    hl, ds = canon["house_lords"], canon["dasha"]

    # core：全景，引用一批事实，全部忠于源数据
    core = {"skill": "core", "ak": canon["ak"], "d9_lagna": canon["d9_lagna"],
            "house_lords": {"1": hl["1"], "7": hl["7"], "10": hl["10"], "9": hl["9"]},
            "planet_dignity": {"Saturn": canon["planet_dignity"]["Saturn"]},
            "dasha": ds[:2]}

    # career：10宫/事业。⚠️ 注入 2 个矛盾，用来演示检查器有牙齿
    career = {"skill": "career", "ak": canon["ak"],
              "house_lords": {"1": hl["1"], "10": "Saturn"},     # ❌ 应为 hl["10"]=Mars
              "planet_dignity": {"Saturn": "Debilitated"},        # ❌ 应为 Own
              "dasha": ds[:2]}
    career["_injected_errors"] = [
        f"house_lords['10']=Saturn  应为 {hl['10']}（与 canonical + core 都矛盾）",
        "planet_dignity['Saturn']=Debilitated  应为 Own",
    ]

    # love：5宫/7宫/配偶，忠于源数据
    love = {"skill": "love",
            "house_lords": {"5": hl["5"], "7": hl["7"]},
            "planet_sign": {"Venus": canon["planet_sign"]["Venus"]},
            "dasha": ds[:2]}

    # soul：AK/Karakamsa，忠于源数据
    soul = {"skill": "soul", "ak": canon["ak"], "d9_lagna": canon["d9_lagna"],
            "planet_sign": {"Saturn": canon["planet_sign"]["Saturn"]}}

    for c in (core, career, love, soul):
        json.dump(c, open(os.path.join(fdir, f"skill_claims_{c['skill']}.json"), "w",
                          encoding="utf-8"), ensure_ascii=False, indent=2)

    print("canonical_facts 派生完成  chart =", canon["chart_id"])
    print("  Lagna 宫主表:", {h: canon["house_lords"][h] for h in ["1", "7", "10"]}, "...")
    print("  Saturn 尊贵度:", canon["planet_dignity"]["Saturn"], "| AK:", canon["ak"],
          "| D9 Lagna:", SIGN_NAMES[canon["d9_lagna"] - 1] if canon["d9_lagna"] else "?")
    print("  已写 4 份 skill_claims（career 含 2 个注入矛盾）")


if __name__ == "__main__":
    main()
