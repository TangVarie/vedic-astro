# 解读 skill 一致性迭代日志

改 core / career / love / soul 任一处时，把跨 skill 一致性当**回归门**。
这套**不评解读好坏**（那靠验前事 + 你的判断），只守"四个 skill 的确定性事实不塌、不打架"。

## 元信息
- 冻结的盘数：N = ___（建议 5-10，覆盖不同 Lagna / 不同强弱格局）
- 每张盘要跑的 skill：core / career / love / soul
- canonical_facts 覆盖的字段：ak / d9_lagna / house_lords / planet_sign / planet_dignity / dasha
  （按你的 skill 实际引用的事实扩充）

## Baseline (v0)
- 保真度：___/N 张盘全绿（四个 skill 都忠于源数据）
- 跨 skill 一致性：___/N 张盘无分歧
- 最常见的矛盾：________（跨盘统计，见底部）

## 轮次 N — [keep / discard]
- 改了哪个 skill 的哪一处：一句话
- 假设：想改进什么（通常是某段解读逻辑）
- 保真度：___/N → ___/N 全绿
- 跨 skill：___/N → ___/N 无分歧
- 出现的新矛盾（若有）：具体到 skill × 字段
- 决策：有新确定性矛盾 → DISCARD；全绿 → 保留，再凭判断看解读是否更好
- 备注

---

## 收敛条件
1. 保真度 = N/N 全绿（所有 skill 忠于 structured_data.md）
2. 跨 skill 一致性 = N/N 无分歧
3. （解读质量本身不在此评——用 vedic-reader 的验前事 + 你的判断）

---

## 跨盘矛盾聚合表

| skill × 字段 | 命中盘数 | 矛盾形态 | 指向该 skill 的哪处 | 是否提名改 |
|---|---|---|---|---|
| 例：career × house_lords[10] | 0/N | — | — | — |
| 例：soul × ak | 1/N | 偶发选错 AK | AK 取数环节 | 待定 |
| 例：career × planet_dignity | 4/N | 把入庙说成陷 | 尊贵度判定话术 | 是 → 轮次 K |

> 跨多张盘反复出现的同类矛盾 = 该 skill 在某个取数/陈述环节有结构性 bug，
> 提名成对那个 skill 的一次明确改动，而不是逐张盘打补丁。
