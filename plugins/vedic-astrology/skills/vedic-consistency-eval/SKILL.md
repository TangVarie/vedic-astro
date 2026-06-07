---
name: vedic-consistency-eval
description: "检查 vedic-core / vedic-career / vedic-love / vedic-soul 四个解读 skill 在【确定性事实】上是否一致、且忠于 structured_data.md 源数据。当用户想【确认四个解读 skill 没在事实上互相打架】、在改动某个解读 skill 后验证事实地基没塌、或排查为什么不同 skill 对同一张盘的事实说法不一时，使用本 skill。触发词：'一致性检查''skill 矛盾''四个 skill 打架''core 和 career 说法不一''改完 core/career 验证''解读 skill 回归''事实是否一致''保真度检查''skill 一致性 eval''跨 skill 校验'。⚠️ 本 skill 只查确定性事实（AK/宫主/行星星座/尊贵度/D9 上升/Dasha），【不评解读质量】——解读好坏靠 vedic-reader 的验前事 + 人工判断，不要用本 skill 给解读打分。"
---

# 跨 skill 一致性 harness

检查 **core / career / love / soul** 在**确定性事实**上 ①忠于源数据（`structured_data.md`）、
②彼此不打架。

## 何时用 / 不用
- **用**：确认四个解读 skill 事实不矛盾、改完某 skill 验证事实没塌、排查 skill 间说法冲突。
- **不用**：评"解读写得好不好"——那没标准答案，靠 `vedic-reader` 的**验前事** + 你的判断。

## 为什么是这个、而不是"解读质量评分"
解读层没有标准答案——"土星落 7 宫对婚姻意味着什么"无法 A/B 打分，更不能用 LLM-judge 假装能打。
但这四个 skill 都读同一份 `structured_data.md`，所以它们引用的**确定性事实**（AK、各宫主、
行星星座/尊贵度、D9 上升、Dasha）**必须一致且忠于源数据**。这是解读层里唯一能被确定性检验的东西，
而且**眼睛逐个看单 skill 根本看不出来**。

## 查两件事（都通过 `check_consistency.py`，比对纯算术，免疫评分独立性问题）
- **保真度 fidelity**：某 skill 自己把 10 宫主读错 / 把尊贵度说反 / AK 选错（偏离源数据）。
- **跨 skill 一致性**：core 说 10 宫主火星、career 说土星（四个独立长出来的 skill 互相矛盾）。

## 数据流
```
structured_data.md ──蒸馏──▶ canonical_facts.json   (源数据真相，单一真相)
各 skill 输出 ──抽取确定性主张──▶ skill_claims_<skill>.json
        │
        ▼  check_consistency.py
   ① 各 claims vs canonical（保真度）   ② 多 claims 互比（跨 skill）
```
抽取那步（prose → JSON）是 **Claude 辅助**的；**比对那步是确定性脚本**。

## 工作流程（一张盘）
1. 跑 `vedic-reader` 得 `structured_data.md` → 按 `schema.md` 蒸馏成 `canonical_facts.json`（Claude 做）。
2. 这张盘依次跑 `vedic-core` / `vedic-career` / `vedic-love` / `vedic-soul`。
3. 从每个 skill 的输出里抽它**明确陈述为事实**的确定性项 → `skill_claims_<skill>.json`
   （按 `schema.md`，Claude 做）。**只抽事实**（"10 宫主是火星""土星入庙"），**不抽解读**。
4. 跑检查：
   ```bash
   python3 check_consistency.py fixtures/<chart>/canonical_facts.json fixtures/<chart>/
   ```
   目录模式会自动扫该目录下所有 `skill_claims_*.json`。退出码：无矛盾 0 / 有矛盾 1。

## 改解读 skill 时当回归门
0. **baseline**：5-10 张盘，每张跑四个 skill→抽 claims→`check_consistency` 应全绿，写 `iteration-log.md`。
1. 改某个 skill 一处话术/规则。
2. 对同一批盘重抽 claims→重跑。
3. 出现**任何新的事实矛盾** → **revert**（事实退步零容忍）；全绿 → 事实地基没塌，再凭判断看解读。

跨多张盘反复出现的同类矛盾（如 career 总把某宫主读错）→ 提名成对那个 skill 的明确改动。

## 与 vedic-reader-eval 的关系
**提取正确（`vedic-reader-eval` 保证）→ 四个 skill 都忠于提取（本 skill 保证）→ 解读才站在可靠地基上。**
解读本身好不好——验前事 + 你这个行家的判断，工具测不了，也不该假装能测。

## 示例（解压即可跑）
`fixtures/example_chart/` 含 `canonical_facts` + 四份 `skill_claims`（career 故意注入 2 个矛盾）：
```bash
python3 check_consistency.py fixtures/example_chart/canonical_facts.json fixtures/example_chart/
```
应 **FAIL** 并指出 career 的两处矛盾（10 宫主、土星尊贵度）——既是保真度也是跨 skill 命中，演示检查器有牙齿。

## 文件
- `check_consistency.py` — 保真度 + 跨 skill 检查
- `cutil.py` — 宫主/尊贵度规则**单一来源**
- `gen_consistency_example.py` — 可选，复用 `vedic-reader-eval` 示例盘造一份可跑通示例
- `schema.md` — `canonical_facts.json` / `skill_claims_*.json` 字段定义
- `methodology.md` — 深入说明 + 限制
- `iteration-log.md` — 迭代日志模板
- `fixtures/example_chart/` — 可跑通示例

## 限制（详见 methodology.md）
只查确定性事实（AK/宫主/星座/尊贵度/D9 上升/Dasha）；尊贵度只到
`Exalted/Debilitated/Own/Other` 四档；`canonical_facts` 字段应按你四个 skill 实际引用的事实扩
（要查 D10 上升、AL/UL、特定 Karaka，加进 schema + canonical + 各 claims 即可）；
claims 抽取是 LLM 辅助步骤，抽完最好扫一眼确认抽的是"陈述为事实"的项、而非把解读修辞误当事实。
