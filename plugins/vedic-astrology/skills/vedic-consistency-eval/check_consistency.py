#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_consistency.py —— 跨 skill 一致性 / 源数据保真度校验

  用法:
    python3 check_consistency.py <canonical_facts.json> <skill_claims_*.json> [更多 skill_claims ...]
    # 或目录模式：自动扫描目录里所有 skill_claims_*.json
    python3 check_consistency.py <dir>

  退出码: 无矛盾 → 0 ；有 fidelity 或 cross-skill 矛盾 → 1

检查两件事：
  1. 保真度 (fidelity)：每个 skill 断言的确定性事实，必须与 canonical_facts(源数据)一致。
     —— 抓"某 skill 自己把 10 宫主读错/把尊贵度说反"。
  2. 跨 skill 一致性 (cross-skill)：被 ≥2 个 skill 同时断言的同一事实，必须彼此相同。
     —— 抓"core 说 10 宫主是火星、career 说是土星"这类互相打架。

⚠️ 本检查【不评解读质量】，只查确定性事实是否自洽。解读层没有标准答案，不在此列。
⚠️ 这一步免疫 5b-0：比对是纯算术，不是判断。
"""
import sys, json, os, glob
from datetime import date

# 可比对的确定性字段
SCALAR = ["ak", "d9_lagna"]          # 单值
MAP = ["house_lords", "planet_sign", "planet_dignity"]  # 字典(键 → 值)


def load_claims(args):
    files = []
    if len(args) == 1 and os.path.isdir(args[0]):
        files = sorted(glob.glob(os.path.join(args[0], "skill_claims_*.json")))
    else:
        files = list(args)
    return [json.load(open(f, encoding="utf-8")) for f in files]


def dasha_equal(a, b, tol_days=31):
    try:
        return (a.get("lord") == b.get("lord")
                and abs((date.fromisoformat(a["start"]) - date.fromisoformat(b["start"])).days) <= tol_days
                and abs(a.get("years", -1) - b.get("years", -2)) < 0.01)
    except Exception:
        return False


def check_fidelity(canon, claims):
    """返回 {skill: [错误描述,...]}"""
    out = {}
    for c in claims:
        sk = c.get("skill", "?")
        errs = []
        for f in SCALAR:
            if f in c and canon.get(f) is not None and c[f] != canon[f]:
                errs.append(f"{f}: 断言 {c[f]} ≠ 源数据 {canon[f]}")
        for f in MAP:
            for k, v in (c.get(f) or {}).items():
                cv = (canon.get(f) or {}).get(k)
                if cv is not None and v != cv:
                    errs.append(f"{f}[{k}]: 断言 {v} ≠ 源数据 {cv}")
        # dasha 列表
        cmap = {e["lord"]: e for e in (canon.get("dasha") or [])}
        for e in (c.get("dasha") or []):
            ce = cmap.get(e.get("lord"))
            if ce and not dasha_equal(e, ce):
                errs.append(f"dasha[{e.get('lord')}]: 起止/周期与源数据不符")
        if errs:
            out[sk] = errs
    return out


def check_cross_skill(claims):
    """被 ≥2 skill 同时断言的事实必须一致。返回 [矛盾描述,...]"""
    issues = []
    # 标量
    for f in SCALAR:
        votes = {}
        for c in claims:
            if f in c and c[f] is not None:
                votes.setdefault(c[f], []).append(c.get("skill", "?"))
        if len(votes) > 1:
            desc = "; ".join(f"{val}←{'/'.join(sks)}" for val, sks in votes.items())
            issues.append(f"{f} 出现分歧: {desc}")
    # 字典字段，逐键
    for f in MAP:
        keyvotes = {}  # key -> {value: [skills]}
        for c in claims:
            for k, v in (c.get(f) or {}).items():
                keyvotes.setdefault(k, {}).setdefault(v, []).append(c.get("skill", "?"))
        for k, votes in keyvotes.items():
            if len(votes) > 1:
                desc = "; ".join(f"{val}←{'/'.join(sks)}" for val, sks in votes.items())
                issues.append(f"{f}[{k}] 出现分歧: {desc}")
    return issues


def main():
    if len(sys.argv) < 2:
        print("用法: python3 check_consistency.py <canonical_facts.json> <skill_claims...> | <dir>")
        sys.exit(2)
    canon = json.load(open(sys.argv[1], encoding="utf-8"))
    claims = load_claims(sys.argv[2:])
    if not claims:
        print("未找到任何 skill_claims_*.json"); sys.exit(2)

    fid = check_fidelity(canon, claims)
    cross = check_cross_skill(claims)

    print(f"\n{'='*64}\n跨 skill 一致性校验   chart = {canon.get('chart_id','?')}"
          f"   skills = {[c.get('skill') for c in claims]}\n{'='*64}")

    print("【保真度】各 skill 的确定性主张 vs 源数据(structured_data.md)")
    if not fid:
        print("  ✅ 全部 skill 忠于源数据")
    else:
        for sk, errs in fid.items():
            print(f"  ❌ {sk}:")
            for e in errs:
                print(f"       - {e}")

    print("\n【跨 skill 一致性】多个 skill 共同断言的事实是否彼此一致")
    if not cross:
        print("  ✅ 无分歧")
    else:
        for i in cross:
            print(f"  ❌ {i}")

    print(f"{'-'*64}")
    nbad = sum(len(v) for v in fid.values()) + len(cross)
    if nbad == 0:
        print("  PASS：确定性事实全部自洽 ✅")
        sys.exit(0)
    else:
        print(f"  FAIL：{nbad} 处确定性矛盾 ❌（解读可以各有侧重，但事实不能打架）")
        sys.exit(1)


if __name__ == "__main__":
    main()
