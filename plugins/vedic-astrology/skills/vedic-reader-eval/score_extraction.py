#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
score_extraction.py —— B 层：对标 JHora 真值，算提取准确率

  用法:  python3 score_extraction.py <ground_truth.json> <reader_output.json>
  退出码: 红线层全过 → 0 ；红线层有失败 → 1

两层分开看（对应种草那套红线/高分的精神）：
  红线层(必须 100%)：星座 / 逆行 / Lagna 星座 / AK —— 错一个，下游全废
  覆盖层(看准确率) ：度数(±1°) / Nakshatra+Pada / D9 / Karaka 排序 / Dasha 起点

⚠️ 真值来自 JHora / Parashara's Light 导出，不是 LLM 重算。
⚠️ 测试盘输入应当是 PDF/截图(易错路径)；文字粘贴当输入会 trivially 满分，没有测试意义。
"""
import sys, json
from vutil import PLANETS, SIGN_NAMES

DEG_TOL = 1.0       # 度数容差(度)
DATE_TOL_DAYS = 31  # Dasha 起点容差(天)


def main():
    if len(sys.argv) != 3:
        print("用法: python3 score_extraction.py <ground_truth.json> <reader_output.json>")
        sys.exit(2)
    gt = json.load(open(sys.argv[1], encoding="utf-8"))
    rd = json.load(open(sys.argv[2], encoding="utf-8"))
    gd, rdd = gt.get("d1", {}), rd.get("d1", {})

    # ---------- 红线层 ----------
    redline_fail = []
    for p in PLANETS:
        if gd.get(p, {}).get("sign") != rdd.get(p, {}).get("sign"):
            redline_fail.append(f"{p} 星座 (真值 {SIGN_NAMES[gd[p]['sign']-1]} / 提取 "
                                f"{SIGN_NAMES[rdd.get(p,{}).get('sign',1)-1] if rdd.get(p,{}).get('sign') else 'NA'})")
        if gd.get(p, {}).get("retrograde") != rdd.get(p, {}).get("retrograde"):
            redline_fail.append(f"{p} 逆行 (真值 {gd[p].get('retrograde')} / 提取 {rdd.get(p,{}).get('retrograde')})")
    if gd.get("Lagna", {}).get("sign") != rdd.get("Lagna", {}).get("sign"):
        redline_fail.append("Lagna 星座")
    if gt.get("chara_karaka", {}).get("ak") != rd.get("chara_karaka", {}).get("ak"):
        redline_fail.append(f"AK (真值 {gt.get('chara_karaka',{}).get('ak')} / 提取 {rd.get('chara_karaka',{}).get('ak')})")

    # ---------- 覆盖层 ----------
    def rate(hits, tot):
        return (hits / tot * 100) if tot else 0.0

    cov = []  # (name, hits, total, misses)

    # 度数 ±1°
    h, t, miss = 0, 0, []
    for p in PLANETS:
        if "deg_in_sign" in gd.get(p, {}) and "deg_in_sign" in rdd.get(p, {}):
            t += 1
            if abs(gd[p]["deg_in_sign"] - rdd[p]["deg_in_sign"]) <= DEG_TOL and gd[p]["sign"] == rdd[p]["sign"]:
                h += 1
            else:
                miss.append(p)
    cov.append((f"度数(±{DEG_TOL}°)", h, t, miss))

    # Nakshatra + Pada
    h, t, miss = 0, 0, []
    for p in PLANETS:
        if "nakshatra" in gd.get(p, {}) and "nakshatra" in rdd.get(p, {}):
            t += 1
            if gd[p]["nakshatra"] == rdd[p]["nakshatra"] and gd[p].get("pada") == rdd[p].get("pada"):
                h += 1
            else:
                miss.append(p)
    cov.append(("Nakshatra+Pada", h, t, miss))

    # D9 落座
    gd9, rd9 = gt.get("d9", {}), rd.get("d9", {})
    h, t, miss = 0, 0, []
    for p in PLANETS + ["Lagna"]:
        if p in gd9 and p in rd9:
            t += 1
            if gd9[p] == rd9[p]:
                h += 1
            else:
                miss.append(p)
    cov.append(("D9 落座", h, t, miss))

    # Karaka 排序(整体一致)
    go, ro = gt.get("chara_karaka", {}).get("order"), rd.get("chara_karaka", {}).get("order")
    ck_ok = (go is not None and list(go) == list(ro or []))
    cov.append(("Karaka 排序(整体)", 1 if ck_ok else 0, 1, [] if ck_ok else ["排序不一致"]))

    # Vimshottari 起点(lord 对 + 起点 ±31 天)
    from datetime import date
    gs, rs = gt.get("vimshottari", []), rd.get("vimshottari", [])
    h, t, miss = 0, 0, []
    rmap = {e["lord"]: e.get("start") for e in rs}
    for e in gs:
        t += 1
        lord = e["lord"]
        try:
            if lord in rmap and abs((date.fromisoformat(rmap[lord]) - date.fromisoformat(e["start"])).days) <= DATE_TOL_DAYS:
                h += 1
            else:
                miss.append(lord)
        except Exception:
            miss.append(lord)
    cov.append(("Vimshottari 起点", h, t, miss))

    # ---------- 输出 ----------
    print(f"\n{'='*64}\nB 层 · 对标 JHora 真值   chart = {gt.get('chart_id','?')}\n{'='*64}")
    print("【红线层】(必须 100%)")
    if not redline_fail:
        print("  ✅ PASS — 星座 / 逆行 / Lagna / AK 全部命中")
    else:
        print(f"  ❌ FAIL — {len(redline_fail)} 项错误:")
        for m in redline_fail:
            print(f"       - {m}")

    print("\n【覆盖层】(看准确率，追高分篇数而非 100%)")
    cov_rates = []
    for name, hh, tt, miss in cov:
        r = rate(hh, tt)
        cov_rates.append(r)
        tail = ("  miss: " + ", ".join(map(str, miss))) if miss else ""
        print(f"  {name:<18} {hh:>2}/{tt:<2}  {r:5.1f}%{tail}")
    overall = sum(cov_rates) / len(cov_rates) if cov_rates else 0
    print(f"{'-'*64}")
    print(f"  覆盖层综合: {overall:.1f}%")
    print(f"{'='*64}")

    if redline_fail:
        print("结论: 红线层未过 → 本轮 DISCARD（立刻 revert）")
        sys.exit(1)
    else:
        print("结论: 红线层通过 → 看覆盖层综合是否 ≥ baseline 决定 keep/revert")
        sys.exit(0)


if __name__ == "__main__":
    main()
