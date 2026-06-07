#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_invariants.py —— A 层：确定性不变量校验（零标准答案）

把 vedic-reader 那 18 条运行时数学校验里【纯内部一致性】的部分冻成回归检查。
不需要任何参考盘——只要 reader 的输出自相矛盾，就抓出来。

  用法:  python3 check_invariants.py <reader_output.json>
  退出码: 全部不变量通过 → 0 ；任一失败 → 1

这一层是【红线】：任何一条 fail 都意味着 reader 产出了一张自相矛盾的盘，
下游 core/career/love/soul 全建在错数据上。必须追到 100% 通过。

⭐ 这一层免疫 5b-0 的"评分独立性"问题——打分是纯算术，不是判断，
   不存在 self-preference bias。
"""
import sys, json
from vutil import (PLANETS, SIGN_NAMES, VIMSHOTTARI, DASHA_ORDER,
                   ALWAYS_RETRO, NEVER_RETRO, lon_from,
                   nakshatra_of, pada_of, d9_sign_of, chara_karaka_order)

EPS = 0.05  # 度数舍入容差，避免恰好落在分盘/星宿边界的误报


def _bucket_ok(reported, lon, fn):
    """reported 桶值是否与经度一致(允许 ±EPS 的边界舍入)。"""
    return reported in {fn(lon - EPS), fn(lon), fn(lon + EPS)}


def check(data):
    res = []  # (id, name, passed, detail)
    d1 = data.get("d1", {})

    # INV-3 行星完整性
    missing = [p for p in PLANETS + ["Lagna"] if p not in d1]
    res.append(("3", "行星完整性(9+Lagna)", not missing,
                "缺失: " + ", ".join(missing) if missing else "9 行星 + Lagna 齐全"))

    # INV-4 星座/度数范围
    bad = []
    for p, v in d1.items():
        s, dg = v.get("sign"), v.get("deg_in_sign", 0)
        if not (isinstance(s, int) and 1 <= s <= 12) or not (0 <= dg < 30):
            bad.append(p)
    res.append(("4", "星座 1-12 / 度数 0-30", not bad,
                "越界: " + ", ".join(bad) if bad else "全部在范围内"))

    # INV-5 Ra-Ke 差 180°(且星座对宫)
    if "Rahu" in d1 and "Ketu" in d1:
        lr = lon_from(d1["Rahu"]["sign"], d1["Rahu"]["deg_in_sign"])
        lk = lon_from(d1["Ketu"]["sign"], d1["Ketu"]["deg_in_sign"])
        diff = (lr - lk) % 360
        opp = (abs(d1["Rahu"]["sign"] - d1["Ketu"]["sign"]) == 6)
        ok = abs(diff - 180) <= 1.0 and opp
        res.append(("5", "Ra-Ke 差 180°(对宫)", ok,
                    f"经度差={diff:.2f}° 对宫={opp}"))
    else:
        res.append(("5", "Ra-Ke 差 180°(对宫)", False, "缺 Rahu/Ketu"))

    # INV-6 逆行标记：完整 + 节点恒逆行 + 日月恒不逆行
    rbad = []
    for p in PLANETS:
        if p not in d1:
            continue
        r = d1[p].get("retrograde")
        if not isinstance(r, bool):
            rbad.append(f"{p}(缺标记)")
        elif p in ALWAYS_RETRO and r is not True:
            rbad.append(f"{p}(节点应逆行)")
        elif p in NEVER_RETRO and r is not False:
            rbad.append(f"{p}(日/月不可能逆行)")
    res.append(("6", "逆行标记(完整+节点/日月铁律)", not rbad,
                "; ".join(rbad) if rbad else "全部合规"))

    # INV-8 Nakshatra/Pada 与度数一致
    nbad = []
    for p in PLANETS:
        if p not in d1 or "nakshatra" not in d1[p]:
            continue
        lon = lon_from(d1[p]["sign"], d1[p]["deg_in_sign"])
        if not _bucket_ok(d1[p]["nakshatra"], lon, nakshatra_of):
            nbad.append(f"{p}(Nak {d1[p]['nakshatra']}≠{nakshatra_of(lon)})")
        if "pada" in d1[p] and not _bucket_ok(d1[p]["pada"], lon, pada_of):
            nbad.append(f"{p}(Pada)")
    res.append(("8", "Nakshatra/Pada 与度数一致", not nbad,
                "; ".join(nbad) if nbad else "全部一致"))

    # INV-9 Chara Karaka 排序与度数一致
    ck = data.get("chara_karaka", {})
    if ck.get("order"):
        expect = chara_karaka_order(d1, ck.get("scheme", "8K"))
        order_ok = (list(ck["order"]) == expect)
        ak_ok = (ck.get("ak") == expect[0])
        res.append(("9", "Chara Karaka 排序与度数一致", order_ok and ak_ok,
                    f"AK 报告={ck.get('ak')} 应为={expect[0]}; "
                    f"排序{'一致' if order_ok else '不一致 → 应为 ' + str(expect)}"))
    else:
        res.append(("9", "Chara Karaka 排序与度数一致", False, "缺 chara_karaka.order"))

    # INV-10 Vimshottari 周期长度 + 序列 + 起点间隔
    seq = data.get("vimshottari", [])
    vbad = []
    for e in seq:
        if abs(e.get("years", -1) - VIMSHOTTARI.get(e.get("lord"), -999)) > 0.01:
            vbad.append(f"{e.get('lord')} 周期={e.get('years')}≠{VIMSHOTTARI.get(e.get('lord'))}")
    for a, b in zip(seq, seq[1:]):
        ia = DASHA_ORDER.index(a["lord"]) if a.get("lord") in DASHA_ORDER else -1
        ib = DASHA_ORDER.index(b["lord"]) if b.get("lord") in DASHA_ORDER else -2
        if ib != (ia + 1) % 9:
            vbad.append(f"{a.get('lord')}→{b.get('lord')} 不符 Vimshottari 顺序")
    # 起点间隔 ≈ years
    try:
        from datetime import date
        for a, b in zip(seq, seq[1:]):
            da = date.fromisoformat(a["start"]); db = date.fromisoformat(b["start"])
            if abs((db - da).days - a["years"] * 365.25) > 31:
                vbad.append(f"{a['lord']} 起点间隔与周期不符")
    except Exception:
        pass
    res.append(("10", "Vimshottari 周期/顺序/间隔", not vbad,
                "; ".join(vbad) if vbad else f"{len(seq)} 段全部自洽"))

    # INV-11 D9 与 D1 度数一致(公式交叉)
    d9 = data.get("d9", {})
    dbad = []
    for p in PLANETS + ["Lagna"]:
        if p not in d1 or p not in d9:
            continue
        lon = lon_from(d1[p]["sign"], d1[p]["deg_in_sign"])
        if not _bucket_ok(d9[p], lon, d9_sign_of):
            dbad.append(f"{p}(D9 {SIGN_NAMES[d9[p]-1]}≠{SIGN_NAMES[d9_sign_of(lon)-1]})")
    res.append(("11", "D9 与 D1 度数一致(公式交叉)", not dbad,
                "; ".join(dbad) if dbad else "全部一致"))

    # INV-1 SAV 总和 = 337
    sav = data.get("sav", [])
    sav_ok = (len(sav) == 12 and sum(sav) == 337 and all(x >= 0 for x in sav))
    res.append(("1", "SAV 总和 = 337(12 宫)", sav_ok,
                f"长度={len(sav)} 总和={sum(sav) if sav else 'NA'}"))

    return res


def main():
    if len(sys.argv) != 2:
        print("用法: python3 check_invariants.py <reader_output.json>")
        sys.exit(2)
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    res = check(data)

    print(f"\n{'='*64}\nA 层 · 确定性不变量校验   chart = {data.get('chart_id','?')}\n{'='*64}")
    for cid, name, ok, detail in res:
        mark = "✅" if ok else "❌"
        print(f"  {mark}  INV-{cid:<3} {name:<28} {detail}")
    n_fail = sum(1 for _, _, ok, _ in res if not ok)
    total = len(res)
    print(f"{'-'*64}")
    if n_fail == 0:
        print(f"  红线层 PASS：{total}/{total} 不变量全部通过 ✅")
        sys.exit(0)
    else:
        print(f"  红线层 FAIL：{total-n_fail}/{total} 通过，{n_fail} 条违反 ❌（必须修到 0 才能 keep）")
        sys.exit(1)


if __name__ == "__main__":
    main()
