#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例盘生成器 (OPTIONAL — 仅用于造一张天文学上真实的示例盘)

⚠️ 你自己跑回归套装时【不需要】这个脚本，也不需要装 swisseph。
   你的真值(ground truth)应当来自 JHora / Parashara's Light 的导出，
   那才是和你实际使用的软件一致的权威答案。
   这个脚本只是用来生成 fixtures/example_chart/ 里那张"模板示例盘"，
   让你看清 schema 长什么样、让 check_invariants.py / score_extraction.py
   能端到端跑通。

它做的事：
  1. 用 Swiss Ephemeris 算一张恒星黄道(Lahiri)真实 D1
  2. 按 vedic-reader SKILL.md 里给定的公式推 Nakshatra / D9 / Chara Karaka
  3. 写出三个 fixture：
       ground_truth.json          —— 真值
       reader_output.clean.json   —— 完美提取(应当满分、全部不变量通过)
       reader_output.with_errors.json —— 故意注入 7 个错误(用来演示检查器有牙齿)

依赖：pip install pyswisseph   （没有也行，会退化到一组内置的、天文学上自洽的经度）
"""
import json, copy, os
from vutil import (PLANETS, SIGN_NAMES, VIMSHOTTARI, DASHA_ORDER,
                   sign_of, deg_in_sign, nakshatra_of, pada_of, d9_sign_of,
                   karaka_degree, chara_karaka_order)

# ---- 模板出生数据（清楚标注为模板，不是任何真人）----
BIRTH = {
    "label": "EXAMPLE TEMPLATE — 非真人，仅用于演示。请用你 JHora 验证过的盘替换。",
    "date": "1990-06-15", "time_local": "08:30", "tz_hours": 8.0,
    "place": "Shanghai (template)", "lat": 31.23, "lon": 121.47,
    "ayanamsa": "Lahiri", "node_type": "mean",
}

# 常数与公式见 vutil.py（单一来源）


# (公式已移至 vutil.py)


def build_d1_swisseph():
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    ut = float(BIRTH["time_local"][:2]) + float(BIRTH["time_local"][3:]) / 60.0 - BIRTH["tz_hours"]
    y, m, d = [int(x) for x in BIRTH["date"].split("-")]
    jd = swe.julday(y, m, d, ut)
    flags = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED  # Moshier：无需星历文件
    ids = {"Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
           "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE}
    d1 = {}
    for name, pid in ids.items():
        xx = swe.calc_ut(jd, pid, flags)[0]
        lon, speed = xx[0] % 360.0, xx[3]
        retro = speed < 0
        if name == "Rahu":
            retro = True  # 月交点恒为逆行
        d1[name] = {"sign": sign_of(lon), "deg_in_sign": round(deg_in_sign(lon), 2),
                    "retrograde": retro, "nakshatra": nakshatra_of(lon), "pada": pada_of(lon),
                    "_lon": round(lon, 4)}
    # Ketu = Rahu + 180
    klon = (d1["Rahu"]["_lon"] + 180.0) % 360.0
    d1["Ketu"] = {"sign": sign_of(klon), "deg_in_sign": round(deg_in_sign(klon), 2),
                  "retrograde": True, "nakshatra": nakshatra_of(klon), "pada": pada_of(klon),
                  "_lon": round(klon, 4)}
    # Lagna (恒星)：用回归上升 - ayanamsa，稳健
    asc_trop = swe.houses(jd, BIRTH["lat"], BIRTH["lon"], b'P')[1][0]
    ayan = swe.get_ayanamsa_ut(jd)
    asc = (asc_trop - ayan) % 360.0
    d1["Lagna"] = {"sign": sign_of(asc), "deg_in_sign": round(deg_in_sign(asc), 2),
                   "_lon": round(asc, 4)}
    return d1


def build_d1_fallback():
    # 天文学上自洽的退化经度(swisseph 缺失时用)：水星<28°、金星<47° 距日，Ra-Ke 差 180°
    lon = {"Sun": 60.8, "Moon": 222.4, "Mars": 133.1, "Mercury": 78.2, "Jupiter": 95.6,
           "Venus": 41.0, "Saturn": 268.7, "Rahu": 304.5}
    lon["Ketu"] = (lon["Rahu"] + 180.0) % 360.0
    d1 = {}
    for p in PLANETS:
        L = lon[p]
        d1[p] = {"sign": sign_of(L), "deg_in_sign": round(deg_in_sign(L), 2),
                 "retrograde": p in ("Saturn", "Rahu", "Ketu"),
                 "nakshatra": nakshatra_of(L), "pada": pada_of(L), "_lon": round(L, 4)}
    asc = 150.5
    d1["Lagna"] = {"sign": sign_of(asc), "deg_in_sign": round(deg_in_sign(asc), 2), "_lon": asc}
    return d1


def derive(d1):
    """从 D1 推 D9 / Karaka / SAV / Vimshottari，组装完整真值。"""
    d9 = {p: d9_sign_of(d1[p]["_lon"]) for p in PLANETS}
    d9["Lagna"] = d9_sign_of(d1["Lagna"]["_lon"])
    order8 = chara_karaka_order(d1, "8K")
    ak = order8[0]

    # SAV：12 宫数值，总和必须=337。这里造一组自洽的(astro 不精确，仅示意总和不变量)。
    sav = [28, 25, 30, 32, 22, 31, 24, 27, 29, 30, 31, 28]  # sum = 337
    assert sum(sav) == 337

    # Vimshottari 大运：起点 lord 与余额本应由 Moon 星宿推；这里造一条【周期长度正确】的时间线
    moon_nak = d1["Moon"]["nakshatra"]
    start_lord = DASHA_ORDER[(moon_nak - 1) % 9]
    seq, year = [], 1989
    idx = DASHA_ORDER.index(start_lord)
    for k in range(6):
        lord = DASHA_ORDER[(idx + k) % 9]
        yrs = VIMSHOTTARI[lord]
        seq.append({"lord": lord, "start": f"{year}-01-01", "years": yrs})
        year += yrs

    return {
        "chart_id": "example_template_1990",
        "meta": {k: BIRTH[k] for k in ("label", "date", "time_local", "tz_hours",
                                       "place", "ayanamsa", "node_type")},
        "d1": {p: {kk: vv for kk, vv in d1[p].items() if kk != "_lon"} for p in d1},
        "d9": d9,
        "chara_karaka": {"scheme": "8K", "ak": ak, "order": order8},
        "sav": sav,
        "vimshottari": seq,
    }


def main():
    try:
        d1 = build_d1_swisseph()
        src = "swisseph (Moshier, Lahiri, mean node)"
    except Exception as e:
        d1 = build_d1_fallback()
        src = f"fallback longitudes (swisseph unavailable: {e})"
    gt = derive(d1)
    gt["meta"]["_generated_by"] = src

    here = os.path.dirname(os.path.abspath(__file__))
    fdir = os.path.join(here, "fixtures", "example_chart")
    os.makedirs(fdir, exist_ok=True)

    with open(os.path.join(fdir, "ground_truth.json"), "w", encoding="utf-8") as f:
        json.dump(gt, f, ensure_ascii=False, indent=2)

    # 完美提取 = 真值原样(代表"reader 一字不差地读对了")
    clean = copy.deepcopy(gt)
    clean["meta"]["_role"] = "reader_output (clean / perfect extraction)"
    with open(os.path.join(fdir, "reader_output.clean.json"), "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, indent=2)

    # 故意注入 7 个错误，覆盖两层、多种不变量
    err = copy.deepcopy(gt)
    err["meta"]["_role"] = "reader_output (with 7 injected errors — for demo)"
    err["meta"]["_injected_errors"] = [
        "E1 Moon.sign +1            -> 红线: 星座错",
        "E2 Mars.retrograde flipped -> 红线: 逆行标记错",
        "E3 Saturn D9 设成错误星座  -> A层不变量#11: D9 与 D1 度数不一致",
        "E4 SAV 改成总和 335        -> A层不变量#1: SAV != 337",
        "E5 Ketu.sign +1            -> A层不变量#5: Ra-Ke 不再差 180°",
        "E6 chara_karaka.ak 改成最低度数的行星 -> 红线 + 不变量#9: AK/排序与度数矛盾",
        "E7 某大运 years 改错        -> A层不变量#10: Vimshottari 周期长度错",
    ]
    err["d1"]["Moon"]["sign"] = (err["d1"]["Moon"]["sign"] % 12) + 1            # E1
    err["d1"]["Mars"]["retrograde"] = not err["d1"]["Mars"]["retrograde"]      # E2
    err["d9"]["Saturn"] = (err["d9"]["Saturn"] % 12) + 1                       # E3
    err["sav"] = err["sav"][:]; err["sav"][0] -= 2                             # E4 -> sum 335
    err["d1"]["Ketu"]["sign"] = (err["d1"]["Ketu"]["sign"] % 12) + 1           # E5
    err["chara_karaka"]["ak"] = err["chara_karaka"]["order"][-1]               # E6
    err["vimshottari"] = copy.deepcopy(err["vimshottari"])
    err["vimshottari"][2]["years"] = err["vimshottari"][2]["years"] + 3        # E7
    with open(os.path.join(fdir, "reader_output.with_errors.json"), "w", encoding="utf-8") as f:
        json.dump(err, f, ensure_ascii=False, indent=2)

    print("生成完成，来源：", src)
    print("AK =", gt["chara_karaka"]["ak"], "| Karaka 排序 =", gt["chara_karaka"]["order"])
    print("D1 星座：", {p: SIGN_NAMES[gt["d1"][p]["sign"] - 1] for p in PLANETS})
    print("Lagna：", SIGN_NAMES[gt["d1"]["Lagna"]["sign"] - 1],
          round(gt["d1"]["Lagna"]["deg_in_sign"], 1), "°")
    print("SAV 总和：", sum(gt["sav"]))


if __name__ == "__main__":
    main()
