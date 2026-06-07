# vedic-consistency-eval · 跨 skill 一致性 harness

检查 **core / career / love / soul** 这四个解读 skill，在**确定性事实**上是否
①忠于源数据(`structured_data.md`)、②彼此不打架。

> **为什么是这个、而不是"解读质量评分"**：解读层没有标准答案——
> "土星落 7 宫对婚姻意味着什么"无法 A/B 打分，更不能用 LLM-judge 假装能打。
> 但这四个 skill 都读同一份 `structured_data.md`，所以它们引用的**确定性事实**
> （AK、各宫主、行星星座/尊贵度、D9 上升、Dasha 起止）**必须一致且忠于源数据**。
> 这是解读层里唯一能被确定性检验的东西——而且眼睛逐个看单 skill 根本看不出来。
> （唯一合法的"解读层评测"是 vedic-reader 里那套验前事——人把预测对照真实人生——你已经有了。）

---

## 查两件事

| 检查 | 抓什么 |
|---|---|
| **保真度 fidelity** | 某个 skill 自己把 10 宫主读错、把尊贵度说反、AK 选错——即偏离源数据 |
| **跨 skill 一致性** | core 说 10 宫主是火星、career 说是土星——四个独立长出来的 skill 互相矛盾 |

两者都通过 `check_consistency.py`，比对是**纯算术**——**免疫 5b-0** 的评分独立性问题。
**本 harness 不评解读质量**，只查确定性事实是否自洽。

---

## 数据流

```
structured_data.md ──蒸馏──▶ canonical_facts.json   (源数据真相，单一来源)
                                      │
   ┌──────────┬──────────┬───────────┤  各 skill 跑完后，从其输出里
 core 输出   career 输出  love 输出  soul 输出   抽取"确定性主张"
   │          │          │          │
   ▼          ▼          ▼          ▼
 skill_claims_core/career/love/soul.json
                                      │
                                      ▼
                         check_consistency.py
                  ① 每份 claims vs canonical (保真度)
                  ② 多份 claims 互相比 (跨 skill)
```

抽取那步（prose → JSON）是 Claude 辅助的；**比对那步是确定性脚本**。
canonical_facts 是源数据，是唯一真相——任何 skill 引用事实时都必须忠于它。

---

## 怎么用（一张盘）

1. 跑 vedic-reader 得到 `structured_data.md`，把其中确定性事实蒸馏成 `canonical_facts.json`
   （按 `schema.md`；可让 Claude 归一化）。
2. 把这张盘依次跑 core / career / love / soul。
3. 从每个 skill 的输出里抽取它**断言过的确定性事实**，写成
   `skill_claims_<skill>.json`（同样按 `schema.md`，可让 Claude 抽）。
   ——只抽它明确陈述为事实的项（"你的 10 宫主是火星""土星入庙"），不抽解读。
4. 跑检查：
   ```
   python3 check_consistency.py fixtures/<chart>/canonical_facts.json fixtures/<chart>/
   # 目录模式会自动扫该目录下所有 skill_claims_*.json
   ```

---

## 与 ① 的关系（两套合起来才完整）

```
①  vedic-reader-eval        ②  vedic-consistency-eval
   读盘提取是否正确             解读 skill 是否忠于提取结果 + 彼此一致
   (对标 JHora 真值)            (对标 structured_data.md + 跨 skill)
        │                              │
        └──────────────┬───────────────┘
                       ▼
        提取正确  →  四个 skill 都忠于提取  →  解读才站在可靠地基上
        (①保证)        (②保证)                (验前事去验，reader 已有)
```

①管"数据对不对"，②管"四个 skill 用数据用得一不一致"。
解读本身好不好——那是验前事 + 你这个行家的判断，工具测不了，也不该假装能测。

---

## 改解读 skill 时怎么用（达尔文回归门）

编辑 core/career/love/soul 任一处后，把这套当**回归门**：
```
0. baseline：选 5-10 张盘，每张跑四个 skill → 抽 claims → check_consistency 应全绿。
1. 改某个 skill 一处话术/规则。
2. 对同一批盘重抽 claims → 重跑 check_consistency。
3. 保真度/一致性出现任何新矛盾 → DISCARD（事实退步零容忍）。
   全绿 → 解读层的"事实地基"没塌，再凭你的判断看解读有没有变好。
```
跨多张盘反复出现的同类矛盾（如 career 总把某宫主读错）→ 提名成对那个 skill 的明确改动。

---

## 文件

```
vedic-consistency-eval/
├── SKILL.md                      # skill 入口（frontmatter 触发 + 操作流程）
├── methodology.md                # 本文件（深入说明）
├── cutil.py                      # 宫主/尊贵度规则（单一来源）
├── check_consistency.py          # 保真度 + 跨 skill 检查
├── gen_consistency_example.py    # 可选：复用①示例盘造一份可跑通的示例
├── schema.md                     # canonical_facts / skill_claims 字段定义
├── iteration-log.md              # 改解读 skill 的迭代日志模板
└── fixtures/
    └── example_chart/
        ├── canonical_facts.json
        ├── skill_claims_core.json
        ├── skill_claims_career.json   # 含 2 个注入矛盾（演示）
        ├── skill_claims_love.json
        └── skill_claims_soul.json
```

---

## 限制（诚实摆出来）

- **只查确定性事实**：AK / 宫主 / 行星星座 / 尊贵度 / D9 上升 / Dasha。解读不查。
- **尊贵度**只到 `Exalted / Debilitated / Own / Other` 四档（friend/enemy/neutral 归 Other），
  避免自然友谊表的体系分歧。要更细可在 `cutil.dignity` 扩。
- **canonical_facts 的字段**应按你四个 skill 实际会引用的事实扩充
  （如要查 D10 上升、AL/UL、特定 Karaka，加进 schema + canonical + 各 claims 即可）。
- **claims 抽取是 LLM 辅助步骤**——抽完最好扫一眼，确认抽的是 skill"陈述为事实"的项，
  而不是把解读里的修辞误当事实。比对本身是确定性的，不受影响。
```
