---
name: vedic-reader-eval
description: "vedic-reader 读盘准确率的回归测试套装(对标 JHora 真值 + 确定性不变量)。当用户想【评测 / 回归测试 vedic-reader 的提取质量】、给读盘建带标准答案的测试集、在改动 vedic-reader 的 SKILL.md 后确认提取准确率没退步、或排查 reader 是否把星座/逆行/Nakshatra/D9/分盘读错时，使用本 skill。触发词：'评测读盘''读盘回归''reader 回归''读盘测试集''读盘准确率''reader 改完测一下''给我的盘建 ground truth''读盘 eval''验证提取''reader baseline''读盘 fixture'。⚠️ 这是【评测 reader 的工具】，不是读盘本身——用户只是想读/分析一张盘时用 vedic-reader，不要触发本 skill。"
---

# vedic-reader 读盘回归测试套装

把 vedic-reader 的 18 条运行时数学校验，冻成**带标准答案、可回归**的评测——
每次改动 reader 后用数字确认"提取准确率有没有掉"，而不是凭感觉。

## 何时用 / 不用
- **用**：评测/回归测试 reader 的提取、给盘建测试集、改完 reader 想验证、排查提取错误。
- **不用**：用户只是想读/分析一张盘（那是 `vedic-reader`，不是本 skill）。

## 为什么 reader 值得这样测
读盘输出（行星落座/度数/Nakshatra/D9/AK/Dasha 起止）**100% 有确定答案**——是整个占星
skill 栈里确定性回归能干净落地、且杠杆最大的地方（reader 读错一颗逆行/认错南北盘，
下游 core/career/love/soul 全建在错数据上）。**解读层没标准答案，不在本 skill 范围**——
别用 LLM-judge 给"解读质量"打分。

## 两层评分（详见 methodology.md）
- **A 层 `check_invariants.py`**：**零标准答案**。把 18 条里的确定性不变量
  （SAV=337、Ra-Ke 差 180°、日月恒不逆行/节点恒逆行、Nakshatra/D9/Karaka 排序与度数一致、
  Vimshottari 周期）冻成回归检查，跑 reader 输出就能抓内部矛盾。**红线，必须 100%**。
  ⭐ 免疫评分独立性问题——纯算术不是判断。
- **B 层 `score_extraction.py`**：对标 JHora 真值。**红线层**(星座/逆行/Lagna/AK 必须 100%)
  + **覆盖层**(度数±1°/Nakshatra+Pada/D9/Karaka 排序/Dasha 起点，看准确率)。

## 🔑 fixture 设计铁律
**测试盘的输入必须是 PDF/截图（reader 易错的路径），真值来自同一张盘的 JHora 文字导出。**
文字粘贴当输入 → reader 只是复述文本 → trivially 100% → **白测**。reader 真正会错的地方在
视觉提取：南北盘识别、逆行小括号遗漏、D10/D4/D5 小盘图误读。

## 工作流程

### 加一张盘（每张盘三件）
`fixtures/<chart_id>/` 下放：`input.pdf`（或 `.png`）、`ground_truth.json`、`reader_output.json`。
1. **真值**：把用户 JHora 的行星表/Dasha/SAV 文字，按 `schema.md` 蒸馏成 `ground_truth.json`
   （Claude 直接做这步归一化）。⚠️ 必须用**用户 JHora 的设置**（岁差体系 / 节点 mean 还是 true）。
2. **输入**：同一张盘的 PDF/截图放成 `input.pdf`。
3. **跑 reader → 归一化**：让 vedic-reader 处理 `input.pdf`，把它输出的 `structured_data.md`
   按 `schema.md` 归一化成 `reader_output.json`。

### 跑评测
```bash
python3 check_invariants.py fixtures/<id>/reader_output.json
python3 score_extraction.py fixtures/<id>/ground_truth.json fixtures/<id>/reader_output.json
```
A 层应全绿；B 层红线应 100%、覆盖层记录百分比。退出码：通过 0 / 失败 1。

### 改 reader 时的 keep/revert 循环
0. **baseline**：全部 fixture 跑 reader→两检查器，记 A 层全绿数 + B 覆盖层综合%，写 `iteration-log.md`。
1. 单变量改 `vedic-reader/SKILL.md` 一处，git commit。
2. 对**同一批冻结的 input** 重跑 reader→两检查器。
3. A 层任一掉绿 → **revert**；A 全绿且 B 覆盖 ≥ baseline → **keep**；A 全绿但 B 覆盖↓ → **revert**。

提取评分是确定性的，没有噪声带 δ 的烦恼；视觉识别本身的随机性可对同一盘跑 2-3 次取一致结果压掉。

### 跨盘聚合
跑完 N 张，把失败项按"检查×盘类型"汇总，找**系统性失败** → 指向 reader 某处该改
（如 D10 落座在多张盘 miss = 该改 reader 的 D10 提取话术），而不是逐张盘打补丁。详见 `methodology.md`。

## 示例（解压即可跑）
`fixtures/example_chart/` 是 swisseph 真算的**模板盘** + 完美/注入错误两份提取：
```bash
python3 check_invariants.py fixtures/example_chart/reader_output.with_errors.json   # 应抓出多条不变量违反
python3 score_extraction.py fixtures/example_chart/ground_truth.json fixtures/example_chart/reader_output.clean.json  # 应满分
```
把它换成你 JHora 验证过的 **10-20 张真盘**即可（南/北印、有/无逆行、Lagna 边界、含/不含分盘）。

## 文件
- `check_invariants.py` / `score_extraction.py` — 两个检查器（A / B 层）
- `vutil.py` — 确定性公式**单一来源**（D9/Nakshatra/Karaka），三个脚本共用
- `gen_example.py` — 可选，造示例盘（需 `pip install pyswisseph`；你自己用时**不需要**跑）
- `schema.md` — `ground_truth.json` / `reader_output.json` 字段定义
- `methodology.md` — 两层评分、达尔文循环、跨盘聚合、限制（深入说明）
- `iteration-log.md` — 迭代日志模板
- `fixtures/example_chart/` — 可跑通示例

## 限制（详见 methodology.md）
真值须匹配你 JHora 的岁差/节点设置；SAV/Shadbala/Dasha 日期请直接从 JHora 填、**不要脚本重算**
（独立重算极易与 JHora 出现细微偏差，反而污染真值）；本 skill 只管**提取**，解读层的事实一致性
用 `vedic-consistency-eval`，解读质量本身用 vedic-reader 的验前事 + 你的判断。
