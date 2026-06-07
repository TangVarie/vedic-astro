# Varshaphala / Tajaka 规则参考

> 来源：Neelakantha《Tajaka Neelakanthi》原典 + KN Rao 教学修正
> 用途：vedic-timing Mode C (年盘) Step 0-2 引用

---

## Tajaka 体系背景

```
Tajaka 是 11-13 世纪从波斯-阿拉伯传入印度的占星体系。
"Tajaka" 一词源于波斯语 (Tazīq)。
与 Parashari 共存于印度，但保留独立算法和体系。

核心区别：
  Parashari：whole-sign aspects (整宫相位)、Vimshottari Dasha、12 宫体系
  Tajaka：orb-based aspects (容度相位)、年/月/日级 Dasha、相同 12 宫但解读不同

Tajaka 专门用于年盘/月盘/Prashna（卜卦），不用于本盘解读。
```

---

## 年盘起算

### 太阳回归本生位

```
出生时太阳的实际黄经 = X°
每年到达"太阳实际黄经 = X°"的那一刻 = 当年年盘起算时刻

例：出生时 Sun 在 Gemini 5°23'
   每年 Sun 再次到达 Gemini 5°23' 的精确时刻 = 起算时刻
   通常在公历生日前后 1 天内（误差源于年际差与岁差）

计算时考虑：
  - Ayanamsa（与本盘一致，标准 Lahiri）
  - True position vs Mean position（吠陀派默认 True）
  - 是否考虑章动（吠陀派一般不计）
```

### 出生地 vs 当前地

```
学派 1（KN Rao 推荐）：始终用出生地经纬度
  原因：出生地是"灵魂锚定"，灵魂"主场"不变

学派 2（部分现代派）：用当前居住地
  原因：年盘反映"当前生活环境"
  
本 skill 默认学派 1，除非用户明确说当前地。
若用户当前地与出生地差异极大（如海外定居），
可两套都跑做对照，但主结论用出生地。
```

### 年盘的 9 颗星位置

```
计算太阳回归本生位的那一刻：
  - 9 颗星（Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn/Rahu/Ketu）的精确位置
  - 该时刻的 Lagna（由出生地经纬度 + 起算时刻计算）

特别注意：
  - 年盘 Sun 必定在与本盘 Sun 相同的星座+度数（这就是"回归"的定义）
  - 其他 8 颗星位置每年不同
  - 年盘 Lagna 每年大约前进 87 度（≈ 2.9 个星座），所以每年年盘 Lagna 不同
```

---

## Muntha（进运 Lagna）

### 计算公式

```
出生时 Muntha = 本盘 Lagna 所在星座
每个生日（年盘起算时刻），Muntha 前进 1 个星座
   
⚠️ 安全的 1-index 公式（避免 Pisces=12 时回到 0 的边界 bug）：
  Muntha 星座号 = ((本盘 Lagna 星座号 - 1 + 年龄) % 12) + 1
  （星座号：Aries=1, Taurus=2, ..., Pisces=12）

⚠️ 不要用 (本盘 Lagna 星座号 + 年龄) % 12 — 这是旧版有 bug 的写法。
  例：本盘 Lagna = Pisces (12)，年龄 0
  旧公式：(12 + 0) % 12 = 0 ❌（星座号不存在 0）
  新公式：((12 - 1 + 0) % 12) + 1 = 11 + 1 = 12 ✓（Pisces）

例 1：本盘 Lagna 在 Aries (1)，年龄 28
  Muntha 星座号 = ((1 - 1 + 28) % 12) + 1 = (28 % 12) + 1 = 4 + 1 = 5
  → Muntha 在 Leo

例 2：本盘 Lagna 在 Pisces (12)，年龄 0
  Muntha 星座号 = ((12 - 1 + 0) % 12) + 1 = (11 % 12) + 1 = 11 + 1 = 12
  → Muntha 在 Pisces (与本盘 Lagna 一致 ✓)

例 3：本盘 Lagna 在 Pisces (12)，年龄 36
  Muntha 星座号 = ((12 - 1 + 36) % 12) + 1 = (47 % 12) + 1 = 11 + 1 = 12
  → Muntha 在 Pisces（36 年走完一圈，回到 Pisces ✓）

Muntha 在年盘的宫位：
  Muntha 星座是年盘 Lagna 星座的几宫？
  例：年盘 Lagna 在 Aries，Muntha 在 Leo → Muntha 在年盘的 5 宫
```

### Muntha 在 12 宫的本年主题

```
Muntha 在年盘 1 宫：
  自我重塑年。主题在"我是谁"。
  通常对应身份切换、性格成长、关键自我认识。
  Muntha 主强 → 健康、活力强。

Muntha 在年盘 2 宫：
  财富/家庭/言语年。
  收入变化、家庭事件、表达能力提升。
  Muntha 主强 + 在吉位 → 财运扩张。

Muntha 在年盘 3 宫：
  勇气/沟通/兄弟年。
  小突破、新技能、与同辈关系活跃。
  通常是"准备期"，为下一年大事铺路。

Muntha 在年盘 4 宫：
  家庭/不动产年。
  搬家、买房、与母亲深度互动、心理稳定调整。
  ⚠️ Muntha 主弱 → 家庭压力大。

Muntha 在年盘 5 宫：
  创造/恋爱/孩子/教育年。
  通常是"快乐之年"——艺术、生育、爱情、深造的高发期。
  Muntha 主强 → 此年极吉。

Muntha 在年盘 6 宫：⚠️ 经典凶位
  竞争/健康/工作压力年。
  对手出现、健康挑战、争议。
  Muntha 主强（尤其凶星强）→ VRY 反转，可能是大胜对手之年。
  Muntha 主弱 → 健康警示。

Muntha 在年盘 7 宫：
  伴侣/合伙/合作年。
  关系核心年——婚姻、商业合作、官司。
  Muntha 主强且 7 宫干净 → 关系突破。

Muntha 在年盘 8 宫：⚠️ 经典凶位
  转化/危机/遗产/隐藏事件年。
  健康挑战、隐性损失、深度心理转化。
  Muntha 主强且参与 VRY → 转化为收益。
  Muntha 主弱 + 8 宫多凶星 → 严重警示。

Muntha 在年盘 9 宫：
  导师/远方/运气/灵性年。
  出国、深造、贵人到来、信仰深化。
  Muntha 主强 → 极吉年。

Muntha 在年盘 10 宫：
  事业巅峰/责任年。
  古典视为"压力"，现代视为"机遇"。
  事业曝光、责任加重、地位变化。
  Muntha 主强 → 事业突破年。

Muntha 在年盘 11 宫：⚠️ 经典最吉
  收入/社交/目标实现年。
  所有领域的奖赏到来。
  财富、声誉、朋友、目标都可能在此年集中实现。
  几乎所有人在 Muntha in 11 时都有显著好事。

Muntha 在年盘 12 宫：⚠️ 经典凶位
  海外/灵性/损耗/隔离年。
  虽是凶位，但有灵性礼物。
  适合：闭关、海外项目、艺术创作、慈善。
  不适合：高调社交、大额投资、签长约。
```

---

## Year Lord（Varshesha）计算

### 5 候选行星

```
候选 1: 本盘 Lagna 主（D1 Lagna 主，不是年盘 Lagna 主）
候选 2: 年盘 Lagna 主
候选 3: 太阳所在 Triamsha 的主（生日时刻太阳的 Triamsha 位置）
候选 4: Muntha 主
候选 5: 月亮所在 Triamsha 的主（生日时刻月亮的 Triamsha 位置）

注：Triamsha 是 30 度分盘（每星座分 30 等份），主决定较复杂，
本 skill 简化为：直接查 JHora 输出的 Year Lord 候选表。
若用户提供完整年盘数据，可手动按下方 Pancha Vargiya Bala 排序。
```

### Pancha Vargiya Bala（5 重力量评分）

```
对每个候选行星计算 5 个维度的力量：

1) Kshetra Bala（领地力量）
   该星在年盘的尊贵度：
     入旺 = 5 / 入庙 = 4 / 友 = 3 / 中 = 2 / 敌 = 1 / 陷 = 0

2) Uchcha Bala（高位力量）
   该星距其入旺度数的距离：
     0° (精确入旺) = 5
     30° = 3
     90° = 2
     180° (精确入陷) = 0

3) Hadda Bala（土耳其分度力量）
   该星在年盘所处的 Hadda 是否由其本身主导：
     是其自身的 Hadda = 5
     是其友的 Hadda = 3
     是其敌的 Hadda = 1

4) Drekkana Bala（10 度分盘力量）
   该星在年盘 Drekkana 的位置：
     该星本身或友星主导该 Drekkana = 5
     敌星主导 = 1

5) Navamsa Bala（D9 力量）
   该星在年盘 Navamsa 的位置：
     旺/庙 = 5 / 友 = 3 / 敌 = 1

总分 = 5 项总和（max 25）

最高分者 = Year Lord (Varshesha)
```

### Year Lord 候选规则补充

```
注意：
  - Rahu/Ketu 不参与 Year Lord 竞争
  - 若多人并列最高分，按以下优先级取：
    Muntha 主 > 年盘 Lagna 主 > 本盘 Lagna 主 > Triamsha 主
  - 若所有候选都极弱（全部 < 10 分），本年"无强 Year Lord"，
    需结合 Muntha + Sahams 综合判断
```

---

## Year Lord 解读

```
Year Lord = 整年的"剧本主导者"。

Year Lord 强（≥ 18 分） + 在吉位 → 本年顺利且有方向
Year Lord 强 + 在凶位 → 本年压力大但有产出
Year Lord 弱 + 在吉位 → 本年潜力被压抑，需主动
Year Lord 弱 + 在凶位 → ⚠️本年困难，需防御策略

各行星作 Year Lord 的主题：

Sun Year Lord:
  权威、曝光、健康（尤其心脏/血压/视力）、与父亲/领导的互动
  适合：争取认可、考公、升职
  警惕：傲慢、对抗权威

Moon Year Lord:
  情感、家庭、母亲、公众情感连接、心理稳定
  适合：照料工作、艺术创作、家庭事务
  警惕：情绪波动、过度敏感

Mars Year Lord:
  行动、勇气、冲突、手术、技术工作、运动
  适合：行动派项目、运动训练、外科类工作
  警惕：冲突、事故、过劳

Mercury Year Lord:
  沟通、商业、写作、学习、短途、社交、商务交易
  适合：商业、咨询、写作出版、谈判
  警惕：神经系统紧张、决策困难

Jupiter Year Lord:  ⭐最吉
  智慧、扩张、教育、孩子、远方、贵人、信仰
  适合：深造、生育、出国、找导师、新项目
  几乎所有领域都可能突破

Venus Year Lord:  ⭐最吉
  爱、艺术、财富、享乐、女性、外交、美容
  适合：恋爱、婚姻、艺术创作、谈生意、奢侈消费
  警惕：感情纠葛、过度享乐

Saturn Year Lord:
  责任、长期建设、老人、土地、慢性事务
  适合：长期项目、置业、传统行业、与长辈合作
  警惕：抑郁、孤立、过劳
```

---

## Patya / Karyesha (月主)

```
Tajaka 的"月主"分配较复杂，主流派别有差异。
本 skill 采用简化版：

第 1 月 (生日起 28-30 天)：由 Year Lord 主导
第 2 月：按七曜顺序循环 (Sun→Moon→Mars→Mercury→Jupiter→Venus→Saturn→Sun...)

例：Year Lord = Jupiter
  第 1 月 = Jupiter
  第 2 月 = Venus (Jupiter 之后是 Venus 按七曜顺序)
  第 3 月 = Saturn
  第 4 月 = Sun
  ...
  第 12 月 = ...

每月主在年盘的状态决定该月主题：
  月主强 + 在吉位 → 该月顺利
  月主弱 + 在凶位 → 该月困难

更精确的 Patya 算法（见 Neelakantha 原典）涉及：
  - Patya 与 Year Lord 共享主导权
  - 不同生日时刻有不同的 Patya 起算
  - 涉及"hours of day" 分配

本 skill 在 Step 5 用上述简化版给月度概览，
若用户对精确月主有强需求，建议用 JHora 软件输出。
```

---

## Triamsha 表（简化版，用于 Year Lord 候选）

```
每星座分 30 度，按以下规则分为 5 个 Triamsha：

奇数星座 (Aries/Gemini/Leo/Libra/Sagittarius/Aquarius):
  0-5°    = Mars
  5-10°   = Saturn
  10-18°  = Jupiter
  18-25°  = Mercury
  25-30°  = Venus

偶数星座 (Taurus/Cancer/Virgo/Scorpio/Capricorn/Pisces):
  0-5°    = Venus
  5-12°   = Mercury
  12-20°  = Jupiter
  20-25°  = Saturn
  25-30°  = Mars
```

---

## Hadda 表（土耳其分度，用于 Pancha Vargiya Bala）

```
Hadda（也叫 Egyptian Terms）将每星座分 5 个不等长部分，
每个部分由一颗行星主导。

Aries:        Jupiter 6° | Venus 6° | Mercury 8° | Mars 5° | Saturn 5°
Taurus:       Venus 8° | Mercury 6° | Jupiter 8° | Saturn 5° | Mars 3°
Gemini:       Mercury 6° | Jupiter 6° | Venus 5° | Mars 7° | Saturn 6°
Cancer:       Mars 7° | Venus 6° | Mercury 6° | Jupiter 7° | Saturn 4°
Leo:          Jupiter 6° | Venus 5° | Saturn 7° | Mercury 6° | Mars 6°
Virgo:        Mercury 7° | Venus 10° | Jupiter 4° | Mars 7° | Saturn 2°
Libra:        Saturn 6° | Mercury 8° | Jupiter 7° | Venus 7° | Mars 2°
Scorpio:      Mars 7° | Venus 4° | Mercury 8° | Jupiter 5° | Saturn 6°
Sagittarius:  Jupiter 12° | Venus 5° | Mercury 4° | Saturn 5° | Mars 4°
Capricorn:    Mercury 7° | Jupiter 7° | Venus 8° | Saturn 4° | Mars 4°
Aquarius:     Mercury 7° | Venus 6° | Jupiter 7° | Mars 5° | Saturn 5°
Pisces:       Venus 12° | Jupiter 4° | Mercury 3° | Mars 9° | Saturn 2°

行星在该度数范围内 = 处于该 Hadda 主行星的领地。
```

---

## 与 Parashari/Vimshottari 的关系

```
重要原则：
  Varshaphala 不替代 Parashari，是叠加层。
  
  Parashari/Vimshottari 给"此生 10 年级主题"
  Varshaphala 给"本年度具体故事"
  
  两者一致 → 本年是该 10 年主题的"焦点年"，事件密度高
  两者冲突 → 本年可能与长期主题"暂时背离"，但不改变 10 年大方向
  
解读时务必先确认 Vimshottari 当前 MD/AD：
  Varshaphala 是"在 Vimshottari 框架内的本年具体表现"
  不是独立替代品
  
KN Rao 教学要点：
  "如果 Vimshottari 说本年应有大事但 Varshaphala 说平静——
   通常是 Vimshottari 对，Varshaphala 只是本年的'局部气候'。
   但若 Varshaphala 极强信号（如 Year Lord 完美 + Muntha 在 11 宫 + Vivaha Saham 激活），
   即使 Vimshottari 中性，该事件也大概率发生。"
```
