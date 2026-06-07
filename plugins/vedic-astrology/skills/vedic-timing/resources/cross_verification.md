# 多 Dasha 交叉验证逻辑

> 用途：vedic-timing Mode B (多 Dasha) Step 4 交汇矩阵构造时引用

---

## 核心思想

```
预测的精度 = 信号收敛的程度

一个 Dasha 说"今年事业转折" = 低置信信号
两个 Dasha 都说"今年事业转折" = 中置信信号
三个 Dasha 都说"今年事业转折" = 高置信信号

但："三个 Dasha 收敛"不是说"用词一样"，
而是"指向同一主题领域 + 同一事件烈度"。

⚠️ v3 修订（反馈意见处理）：
v2 这里写"概率 30-40% / 60-70% / 85%+"是错误的，因为：
  - 这些百分比没有经过历史回测统计校准
  - 用具体百分比会给用户造成"已经过统计验证"的错觉
  - 实际是"内部置信等级"，不是真实统计概率

v3 改用 "低/中/高 置信信号" 三级定性表达。
未来如做了 100+ 案例回测统计，再回填具体百分比。
```

---

## 主题归类系统

为做交叉验证，把所有 Dasha 信号归入以下主题大类：

```
A. 关系类（婚姻/伴侣/合伙/重大友谊）
B. 事业类（升职/转行/创业/重大职务变动）
C. 财富类（收入显著变化/重大投资/置业）
D. 健康类（重病/手术/慢性病/长期康复）
E. 家庭类（搬迁/家人重大事件/继承）
F. 教育/灵性类（深造/重大学习/灵性突破）
G. 出行/海外类（移民/长期出国/重大旅行）
H. 创造类（出版/作品发布/创业/生育）
I. 转化类（重大丧失/转化/危机）
J. 自我重塑类（身份转变/性格剧变）
```

每个 Dasha 信号都需归入这 10 类之一（可重叠）。

---

## Vimshottari 信号→主题映射

```
Vim MD/AD 是 1L (Lagna 主)：J. 自我重塑
Vim MD/AD 是 2L：C. 财富 / E. 家庭
Vim MD/AD 是 3L：B. 事业（小） / H. 创造
Vim MD/AD 是 4L：E. 家庭 / G. 出行（迁居）
Vim MD/AD 是 5L：F. 教育 / H. 创造（生育）/ A. 关系（恋爱）
Vim MD/AD 是 6L：D. 健康 / I. 转化（争议）
Vim MD/AD 是 7L：A. 关系 / B. 事业（合伙）
Vim MD/AD 是 8L：I. 转化 / D. 健康
Vim MD/AD 是 9L：F. 教育/灵性 / G. 出行（远方）
Vim MD/AD 是 10L：B. 事业
Vim MD/AD 是 11L：C. 财富 / A. 关系（友谊网络）
Vim MD/AD 是 12L：G. 出行（海外）/ F. 灵性 / I. 转化（损失）

Vim 行星本身：
  Sun → B. 事业（权威） / D. 健康（心脏/活力）
  Moon → E. 家庭（母亲） / J. 自我（情绪）
  Mars → B. 事业（行动） / I. 转化（冲突） / D. 健康（手术）
  Mercury → B. 事业（沟通） / F. 教育
  Jupiter → F. 教育/灵性 / A. 关系（导师） / H. 创造（子女）
  Venus → A. 关系 / C. 财富 / H. 创造（艺术）
  Saturn → B. 事业（长期） / D. 健康（慢性） / I. 转化
  Rahu → G. 出行（外缘） / B. 事业（突变） / I. 转化（剧变）
  Ketu → F. 灵性 / I. 转化（解脱）

最终 Vim 信号 = 上述两层（管宫 + 自身性质）的合集
```

---

## Chara Dasha 信号→主题映射

```
Chara MD = 本盘 1 宫：J. 自我重塑
Chara MD = 本盘 2 宫：C. 财富 / E. 家庭
Chara MD = 本盘 3 宫：B. 事业（小） / H. 创造
Chara MD = 本盘 4 宫：E. 家庭 / G. 出行（搬迁）
Chara MD = 本盘 5 宫：H. 创造 / A. 关系（恋爱）/ F. 教育
Chara MD = 本盘 6 宫：D. 健康 / I. 转化
Chara MD = 本盘 7 宫：A. 关系
Chara MD = 本盘 8 宫：I. 转化 / D. 健康
Chara MD = 本盘 9 宫：F. 灵性 / G. 出行
Chara MD = 本盘 10 宫：B. 事业
Chara MD = 本盘 11 宫：C. 财富
Chara MD = 本盘 12 宫：G. 海外 / F. 灵性

附加层（Karaka 主题强化）：
Chara MD = AK 所在星座 → 加权 J. 自我重塑
Chara MD = AmK 所在星座 → 加权 B. 事业
Chara MD = DK 所在星座 → 加权 A. 关系
Chara MD = PK 所在星座 → 加权 H. 创造
Chara MD = MK 所在星座 → 加权 E. 家庭
Chara MD = GK 所在星座 → 加权 D. 健康 / I. 转化
```

---

## Yogini Dasha 信号→主题映射

```
Mangala (Moon) → E. 家庭 / J. 自我（情绪）
Pingala (Sun) → B. 事业 / D. 健康（权威/心脏）
Dhanya (Jupiter) → F. 教育/灵性 / H. 创造（生育）/ G. 远行
Bhramari (Mars) → B. 事业 / I. 转化（冲突） / D. 健康（手术）
Bhadrika (Mercury) → B. 事业（沟通） / F. 教育
Ulka (Saturn) → I. 转化（损失） / D. 健康（慢性） / B. 事业（长期）
Siddha (Venus) → A. 关系 / C. 财富 / H. 创造（艺术）
Sankata (Rahu) → G. 出行 / I. 转化（剧变） / B. 事业（突变）
```

---

## 收敛度评分算法（v3 修订，加主次主题权重）

```
v2 旧版用纯 Jaccard 系数 = |A∩B| / |A∪B|
问题：同一个 Dasha 信号可归多类（如 5 宫主 → F.教育 / H.创造 / A.恋爱），
     多类归属会让 Jaccard 分子分母都膨胀，产生"虚假高收敛"。

v3 修订：主题分主次，加权计算。

主题归属规则（每个 Dasha 信号必须分配）：
  主要主题（primary）：该信号最直接指向的 1 个主题，权重 1.0
  次要主题（secondary）：该信号可能波及的 0-2 个主题，权重 0.5

例：Vim Antardasha = Venus（5 宫主）
  主要主题：A. 关系（Venus 的天然 Karaka 主题最强）
  次要主题：F. 教育（5 宫学习）、H. 创造（5 宫创造力）

对每年（或每季度），收集三套 Dasha 各自的"主题信号"加权集合：
  Vim:    {A: 1.0, F: 0.5, H: 0.5}
  Chara:  {A: 1.0, B: 0.5}
  Yogini: {A: 1.0, C: 0.5}

加权 Jaccard 计算（每个主题取三方权重的 min/max）：
  Weighted_Jaccard(A, B) = Σ min(w_A, w_B) / Σ max(w_A, w_B)

三方共同主题判定：
  对每个主题 t，若三方都包含 t（不论主次）→ 算共同
  其中主要主题三方都命中 → 加强信号（权重 ×1.5）

判定（v3 加严）：
  三方都有同一【主要主题】+ 三个 Dasha 判定（吉/凶/混）一致 → 【极高置信度】
  三方都有同一主题（含次要）+ 加权 Jaccard 平均 ≥ 0.5  → 【高置信度】
  两两加权 Jaccard 平均 0.3-0.5                          → 【中置信度】
  两两加权 Jaccard 平均 < 0.3                            → 【低置信度，信号分歧】

特殊：吉凶判定冲突（一套大吉一套大凶）→ 【信号冲突，按"双轨人生"解读】
```

---

## 吉凶判定（每 Dasha 独立，v3 修订）

```
⚠️ v3 修订：Vimshottari 单期吉凶必须使用 house_framework.md 的
"6 条正面 + 6 条负面"完整规则，不再使用本文件的简化四级表。
这避免了"timing 和 core 用不同尺度判定同一个 Dasha"的不一致。

引用：vedic-core/resources/house_framework.md "Dasha 事件推导硬约束"段

#### Vimshottari 正面条件（满足≥2条→判定为正面）
  1. P1 身份 = 吉角色（Core-Driver / Yogakaraka / Faithful）
  2. P7 尊贵度 ≥ 友方（Friend/Own/Exalted）
  3. P9 Shadbala ≥ 120%
  4. 落在吉路（1/4/5/7/9/10 宫）
  5. 管的宫位 SAV ≥ 28
  6. Vargottama 或 Dig Bala 加成

#### Vimshottari 负面条件（满足任一即标注风险）
  1. P1 身份 = 凶角色（Trika-Lord 管 8/12 或 Growth-Hacker 管 6）
  2. P2 受损（燃烧/落陷/败相）
  3. 落在凶路（6/8/12 宫）且无 VRY 补救
  4. P9 Shadbala < 100%
  5. 管的宫位 SAV < 25
  6. 与凶星紧密合相（< 5°）

#### Vimshottari 判定逻辑
  正面 ≥2 且 负面 = 0   → 正面期
  正面 ≥2 且 负面 ≥1   → 混合期
  正面 < 2 且 负面 ≥1   → 困难期
  正面 = 0 且 负面 ≥2   → 危机期

⚠️ Functional 维度叠加：判定后必须再查 p1_p12.md P1.5 Functional 矩阵
  FB（Functional Benefic）期 → 判定可加 0.5 级（正面期 → 强正面）
  FM（Functional Malefic）期 → 判定降 0.5 级（混合期 → 偏困难）
  这是为了对齐 core 的 PAC 联合判定标准。

Chara 单期吉凶：
  Chara MD = 本盘 1/2/4/5/7/9/10/11 = 吉
  Chara MD = 本盘 3/6/8/12 = 看是否 VRY 激活
  Chara MD 中有吉星（Jupiter/Venus，状态好） = 加吉
  Chara MD 中有凶星（Mars/Saturn 受损） = 加凶
  Chara MD 星座主在 6/8/12 = 偏凶

Yogini 单期吉凶：
  按 Yogini 自然性质（吉/凶）+ 对应行星本盘状态
  自然吉 + 行星状态好 = 大吉
  自然吉 + 行星状态弱 = 吉但弱
  自然凶 + 行星状态好 = 高压有产出
  自然凶 + 行星状态弱 = 凶
```

---

## 信号冲突的处理

```
当三套 Dasha 吉凶判定明显冲突时，不强行调和，而是：

1. 标注"双轨人生"
   例：Vim Saturn MD（凶/限制） + Yogini Siddha（吉/爱情）
   → 同期内可能同时存在"事业受压"和"感情甜蜜"
   → 解读："2027 是你压力很大的一年，但感情可能在此期间显著进展。
           不要因为事业压力就忽略感情机会，二者并行。"

2. 优先级判定（极端情况下）：
   - 健康/危机信号优先（D类、I类主题）
   - 即一套 Dasha 给出强健康警示 + 其他给吉 → 仍标注健康警示为主
   - 这是临床安全原则

3. "心理"vs"外在"分层（KN Rao 原则）：
   Vim 偏心理感受，Chara 偏外在事件
   两者冲突常常是真实的"内外不一"：
     Vim 吉 + Chara 凶 = "心情还行但环境难"
     Vim 凶 + Chara 吉 = "外在收获但心累"
```

---

## 历史回测的"事件→Dasha"反向校准

```
回测步骤：
  1. 用户提供过去 5-10 年的人生事件年份（不需要细节，只需主题）
  2. 对每个事件，查那一年的三 Dasha 状态
  3. 看该年是否被本算法标为"高/极高置信度年"
  4. 统计命中率

命中标准（宽松）：
  事件主题 ∈ 当年三 Dasha 综合主题集合 = 命中
  
命中率解读：
  ≥ 60%：体系对此人有效，未来预测可信度高
  40-60%：部分有效，建议结合 Gochara
  ≤ 40%：可能出生时间需要校准（敏感度: Chara > Yogini > Vim）

时间校准建议：
  如果命中率低，但 Vim 部分命中率较高（如 ≥ 50%）→ 时间偏差不大但需精确化
  如果三套都低 → 时间偏差较大，强烈建议跑 vedic-rectifier
```

---

## 写作风格指引（输出到 dc4 时）

```
✅ 好的写法：
"2027 年是你三套时间体系都点亮的一年：
- Vimshottari 在 Saturn-Venus 小运（关系+财富主题）
- Chara Dasha 走到 Cancer (本盘 7 宫 = 关系)
- Yogini 进入 Siddha (Venus 主导 = 关系+艺术)

三套独立体系都指向'关系'这个主题，且都偏吉。
这意味着 2027 年大概率是你这十年里的'关系大年'——
单身的话可能遇到长期伴侣，已婚的话可能进入新阶段（生育/置业/共同事业）。
不需要刻意安排，让它发生。"

❌ 坏的写法：
"Vimshottari Saturn-Venus, Chara Cancer Dasha, Yogini Siddha period
indicates karmic activation of 7th house themes..."
（参数化、不解释，禁止）
```
