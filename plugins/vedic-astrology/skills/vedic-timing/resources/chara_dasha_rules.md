# Chara Dasha 规则参考

> 来源：Jaimini Maharshi 原典 + KN Rao《Predicting Through Jaimini's Chara Dasha》
> 用途：vedic-timing Mode B (多 Dasha) Step 0 计算 + Step 2 解读

---

## 什么是 Chara Dasha

Jaimini 体系的核心 Dasha。基于**Lagna 星座**（而非 Moon Nakshatra）起算。
特点：
- 大运是"星座"而非"行星"
- 每个大运时长 1-12 年（变化）
- 与 Vimshottari 完全独立，是 KN Rao 推荐的最佳"第二意见"

---

## 起算规则

```
起算大运 = Lagna 所在星座

方向判定（本系统采用 KN Rao 简化 odd/even Lagna 规则）：
  Lagna 在奇数星座 (Aries=1, Gemini=3, Leo=5, Libra=7, Sagittarius=9, Aquarius=11)
    → 顺行（按星座顺序 1→2→3→...→12→1...）
  
  Lagna 在偶数星座 (Taurus=2, Cancer=4, Virgo=6, Scorpio=8, Capricorn=10, Pisces=12)
    → 逆行（按星座顺序 1→12→11→...）

每大运时长 = 从该大运星座数到其星座主所在星座的距离
            （含终点不含起点；同宫 = 12）

  ⚠️ 方向说明：
    "从 sign 数到 lord"——sign 是起点，lord 所在星座是终点。
    不要读成"从主反数回到星座"。
  
  顺行时：
    从该大运星座数到星座主所在的星座（同方向 = 顺序)
    含终点不含起点
    如果主在该星座本身 = 12 年
    
  逆行时：
    从该大运星座反向数到星座主所在的星座
    
  例：
    Aries Lagna，顺行。
    Aries 大运 → Aries 主是 Mars，Mars 在 Leo
    从 Aries 顺数到 Leo: Taurus(1) → Gemini(2) → Cancer(3) → Leo(4)
    含终点不含起点 = 4 步
    所以 Aries 大运 = 4 年
```

### ⚠️ Chara Dasha 方向变体声明（v3.4 新增）

```
Jaimini Chara Dasha 的方向规则在不同流派之间差异显著。
本系统默认采用 KN Rao 的"简化 odd/even Lagna"规则，
但这不是唯一标准。其他权威流派的方向规则包括：

  Savya / Apasavya 派（部分 Jaimini 原典派）：
    Savya 星座组（顺行）：Aries, Taurus, Gemini, Libra, Scorpio, Sagittarius
    Apasavya 星座组（逆行）：Cancer, Leo, Virgo, Capricorn, Aquarius, Pisces
    → 与本系统的 odd/even 规则不一致（如 Taurus 本系统逆行，Savya 派顺行）
  
  Iranganti Rangacharya 派：
    复合规则，考虑 Lagna 的 Movable/Fixed/Dual 性质
  
  Sanjay Rath (SJC) 派：
    Karakamsa 位置 + Lagna 性质的复合规则
  
  PVR Narasimha Rao 派：
    与 KN Rao 派接近但 Scorpio/Aquarius 双主处理细节不同

软件对照协议：
  如果用户软件（JHora / Parashara's Light / Kala / etc.）输出的 Chara Dasha
  与本系统计算结果不一致：
  
  1. 不直接判为错误。
  2. 必须记录用户软件采用的：
     - Chara Dasha 变体名称（Savya/Apasavya / Rangacharya / SJC / PVR / KN Rao / 其他）
     - 起运星座（与本系统是否一致）
     - 顺行/逆行方向（与本系统是否一致）
     - Scorpio / Aquarius 双主处理规则
  3. 在 dc1 主题审计报告中标注：
     "本盘 Chara Dasha 采用 [流派名] 算法，与用户软件 [软件名] 输出一致 / 不一致"
  4. 在 cross_verification 三 Dasha 验证中，Chara Dasha 命中率偏差
     可能受流派差异影响，不一定是算法错误。
  
默认策略：先用本系统的 KN Rao 简化规则，
         如与软件不一致 → 切换到软件流派重算，
         不强行用本系统规则去对抗软件。
```

---

## 星座主表（含 Rahu/Ketu 副主）

```
| 星座 | 主 | 副主（若适用） |
|------|----|------------|
| Aries | Mars | — |
| Taurus | Venus | — |
| Gemini | Mercury | — |
| Cancer | Moon | — |
| Leo | Sun | — |
| Virgo | Mercury | — |
| Libra | Venus | — |
| Scorpio | Mars | Ketu（副主） |
| Sagittarius | Jupiter | — |
| Capricorn | Saturn | — |
| Aquarius | Saturn | Rahu（副主） |
| Pisces | Jupiter | — |
```

### 副主处理立场（v3 显式标注）

```
本系统默认：KN Rao "先到优先" 原则
  Scorpio 时长 = min(到 Mars 的距离, 到 Ketu 的距离) 
  Aquarius 时长 = min(到 Saturn 的距离, 到 Rahu 的距离)
  
  原理：取较短距离 = 较早"激活"的副主，对应较短的大运时长。

⚠️ 其他流派的副主处理（约 5-10% 案例会得到不同时长）：

  Iranganti Rangacharya 派："力量优先" 原则
    取 Mars vs Ketu / Saturn vs Rahu 中力量较强者（按 Shadbala 或 Avastha）
    适用：用户希望强调"主导能量"的预测
    
  Sanjay Rath (SJC) 派："复合规则"
    考虑副主与主星的角度关系、各自的 Karaka 角色等
    最复杂但据称对印度本土用户最准
    
  PVR Narasimha Rao 派："对宫优先"
    优先考虑副主与该星座对宫的关系
    适用：考虑业力轴线主题时

实操判定：
  - 默认用本系统的 KN Rao "先到优先"
  - 如用户的 Scorpio/Aquarius 大运预测与实际偏差大（命中率<50%）
    → 可切换"力量优先"重算这两个大运的时长
    → 但其他大运的判定不变
    → 在 dc1（Chara Dasha 主题审计）报告中标注：
      "本盘 Scorpio/Aquarius 大运采用 [Rangacharya 力量优先 / SJC 复合 / ...] 算法"
  - 在 cross_verification 收敛度评分中，这两个大运的时长不一致
    可作为 Mode B 命中率偏差的解释之一
```

---

## 完整算例

```
案例：Aries Lagna，顺行

Mars 在 Leo (5)         → Aries MD = 5-1 = 4 年
Venus 在 Capricorn (10) → Taurus MD = 10-2 = 8 年
Mercury 在 Pisces (12)  → Gemini MD = 12-3 = 9 年
Moon 在 Gemini (3)      → Cancer MD = 3-4 (负) → 加 12 = 11 年
Sun 在 Aries (1)        → Leo MD = 1-5 (负) → 加 12 = 8 年
Mercury 在 Pisces (12)  → Virgo MD = 12-6 = 6 年
Venus 在 Capricorn (10) → Libra MD = 10-7 = 3 年
Mars 在 Leo (5)         → Scorpio MD = 5-8 (负) → 加 12 = 9 年
                          也看 Ketu 位置取较近者
Jupiter 在 Sagittarius (9) → Sagittarius MD = 9-9 = 0 → 取 12 年
Saturn 在 Aquarius (11) → Capricorn MD = 11-10 = 1 年
Saturn 在 Aquarius (11) → Aquarius MD = 11-11 = 0 → 取 12 年
                          也看 Rahu 位置取较近者
Jupiter 在 Sagittarius (9) → Pisces MD = 9-12 (负) → 加 12 = 9 年

累计 = 4+8+9+11+8+6+3+9+12+1+12+9 ≈ 92 年（典型寿命覆盖）
```

---

## 解读规则（Step 2 用）

### 三层结构

```
第 1 层：大运星座本身
  Chara MD = 该星座 → 该星座在本盘是几宫？该宫位主题被激活。
  
  例：Cancer Chara MD，Cancer 在本盘是 7 宫 → 该期主题：婚姻/合作

第 2 层：大运星座中的行星
  该星座中有哪些行星？它们的 P1 身份 + 状态 = 给该 MD 染色。
  
  例：Cancer 中有 Moon 和 Jupiter
      Moon 是 L4 (Trader)，Jupiter 是 L9+L12 (Faithful)
      → 该期：合作主题 + 母性/情绪 + 智慧/导师 + 隐性损耗

第 3 层：大运星座的对冲位
  对冲位 = 第 7 宫位置 → 该期的"外部对照"。
  
  例：Cancer 的对冲是 Capricorn，Capricorn 在本盘是 1 宫
      → 该期：婚姻主题被激活时，"自我"也被对照（典型婚姻定位期）
```

### Karaka 联动

```
当 Chara MD = AK (Atmakaraka) 所在的星座或其对冲位
  → "灵魂主题年"：人生主线方向出现重大调整
  → 此期事件具有"灵魂层级"的重要性

Chara MD = AmK (Amatyakaraka) 所在的星座或其对冲位
  → "事业主题年"：事业重大转折

Chara MD = DK (Darakaraka) 所在的星座或其对冲位
  → "配偶主题年"：婚姻/伴侣相关重大事件

Chara MD = GK (Gnatikaraka) 所在的星座或其对冲位
  → "障碍主题年"：需面对长期回避的问题、健康议题

Chara MD = PK (Putrakaraka) 所在的星座或其对冲位
  → "创造/子女主题年"：生育、创业、艺术作品发布

Chara MD = MK (Matrukaraka) 所在的星座或其对冲位
  → "母亲/根源主题年"：母系亲属、心理根源、家乡

Chara MD = BK (Bhratrukaraka) 所在的星座或其对冲位
  → "兄弟/同盟主题年"：兄弟姐妹、合作伙伴、武功层面（勇气、努力）
```

### Atmakaraka 一般规则

```
KN Rao 强调：
  Chara MD 中如果出现 AK 或 AK 在该 MD 的星座得到激活，
  此 MD 是该人生命中最重要的阶段之一。
  
  Atmakaraka 的"角色"（它本身的 P1 身份）决定主题颜色。
```

---

## Antardasha（小运）算法（简化）

```
Chara Antardasha 的算法比 MD 更复杂，主流派别有差异。
最常用的方式（KN Rao 体系）：

在某个 Chara MD（如 Cancer MD = 11 年）内：
  AD 顺序按 Chara MD 同方向继续
  AD1 = 该 MD 星座本身（Cancer）
  AD2 = 下一个星座（Leo）
  AD3 = Virgo
  ...
  AD12 = Gemini（回到起点前）

每个 AD 时长 = MD 时长 / 12（粗略）
  Cancer MD = 11 年 → 每 AD ≈ 11/12 ≈ 11 个月

更精确的算法：
  每个 AD 时长按其星座主的距离比例分配（与 MD 算法同源）
  这部分实现复杂，本 skill 在 Step 0 计算时用简化版（均分 12 等份），
  仅在 Step 4 交汇矩阵中标注"AD 精度 ±2 个月"。
```

---

## 与 Vimshottari 的协同 vs 矛盾

```
协同（应当一致的信号）：
  Vim Jupiter MD + Chara MD 在 5/9 宫 → 双重智慧/教育/扩张主题
  Vim Venus MD + Chara MD 在 DK 所在或 7 宫 → 双重感情/婚姻主题
  Vim Saturn MD + Chara MD 在 6 或 8 宫 → 双重压力/转化主题

矛盾（信号分歧）：
  Vim Rahu MD（迷雾/野心） + Chara MD = 9 宫（导师/远方）
    → 同时存在"灵性追求"和"野心扩张"两条平行线索
    → 不冲突，而是"双轨人生"
  
  Vim Saturn MD（限制） + Chara MD = 11 宫（收入/目标）
    → 同时存在"承担责任"和"目标达成"
    → 通常是"高压力高产出"窗口
  
处理冲突的原则：
  Vimshottari = 心理感受
  Chara Dasha = 外在事件
  两者不一致时常常是"外在丰收但心累"或"外在艰难但内在成长"
  这不是冲突，是真实人生的双层结构
```

---

## 临床速查表（KN Rao 教学常用）

```
"灵魂大年"信号：
  Chara MD = AK 所在星座本身
  Chara MD = AK 所在星座的对冲位
  Chara MD = AK 自然年龄段对应（AK Sun → 中年；AK Moon → 童年/晚年；等）

"婚姻大年"信号：
  Chara MD = DK 所在星座本身
  Chara MD = 本盘 7 宫
  Chara MD = 本盘 2 宫（家庭扩张）
  Chara MD = Venus 所在星座（自然婚姻 Karaka）

"事业大年"信号：
  Chara MD = AmK 所在星座
  Chara MD = 本盘 10 宫
  Chara MD = 10 宫主所在星座
  Chara MD = 本盘 11 宫（收入实现）

"健康警示年"信号：
  Chara MD = 本盘 6 宫
  Chara MD = 本盘 8 宫
  Chara MD = GK 所在星座
  Chara MD = 6/8/12 宫主所在星座

"灵性突破年"信号：
  Chara MD = 本盘 12 宫
  Chara MD = 本盘 9 宫
  Chara MD = AK 所在星座对冲位
  Chara MD = Ketu 所在星座
```

---

# Argala（干预力）— Jaimini 体系的精细化工具（v2 新增）

> Argala = "干预" / "影响"，用于细化 Chara Dasha 期间事件的方向和品质。
> 来源：Jaimini Sutras 1.1.45-1.1.50 + KN Rao 临床注释 + SJC 体系深化
> 用途：Chara Dasha 主题判定后，用 Argala 进一步看"这个主题会顺着展开还是受阻"

## Argala 的核心概念

```
基础原则：
  当 Chara Dasha 走到一个星座（= 一个宫位）时，
  该宫位的"主题"是否能顺利兑现，由从该宫位起的特定其他宫位行星决定。
  
  这些"干预者"叫 Argala（正向加持）
  阻止 Argala 的叫 Virodha Argala（反向阻挡）

逻辑结构：
  Chara MD 星座 = 主题宫
  ↓
  Argala 宫位 = 提供"加持/阻挡"的干预力
  ↓  
  Virodha Argala 宫位 = 决定 Argala 是否能真正生效
  
最终判定：
  Argala > Virodha Argala → 主题顺利展开（带 Argala 行星的色彩）
  Argala = Virodha Argala → 主题中性（按 Chara MD 主题展开，无特殊增减）
  Argala < Virodha Argala → 主题受阻（带 Virodha Argala 行星的色彩）
```

## 主要 Argala 位（按强度排序）

```
从 Chara MD 星座起算，以下宫位的行星形成 Argala：

1. 4 宫 Argala (Shubha Argala，主要 Argala)
   → 该宫位行星 = 主要干预者
   → 吉星在此 = 强力加持
   → 凶星在此 = 强力阻挡
   被 10 宫的行星制约 (Virodha)

2. 2 宫 Argala (Dhana Argala，财富 Argala)
   → 影响该主题的"资源/财务"维度
   被 12 宫的行星制约 (Virodha)

3. 11 宫 Argala (Labha Argala，收益 Argala)
   → 影响该主题的"实现/收获"维度
   被 3 宫的行星制约 (Virodha)

4. 5 宫 Argala (Putra Argala，创造 Argala)
   → 影响该主题的"创造/智慧/趣味"维度
   被 9 宫的行星制约 (Virodha)
   ⚠️ 注意：这一对的 Argala/Virodha 关系在某些流派中颠倒，
      本系统采用 SJC 派：5宫 = Argala，9宫 = Virodha
```

## Argala 评分算法

```
对当前 Chara MD 的每个 Argala 位：

  Step 1：查该宫位是否有行星
    无行星 → Argala 力 = 0（中性）
    有行星 → 继续 Step 2
    
  Step 2：查行星的自然属性
    吉星（Jupiter / Venus / Mercury / 强 Moon）= +1（加持）
    凶星（Saturn / Mars / Sun / Rahu / Ketu）= -1（阻挡）
    
  Step 3：查行星的状态
    入旺/入庙/Vargottama → ×1.5
    燃烧/落陷 → ×0.5
    
  Step 4：查 Virodha Argala 位是否有制约
    Virodha 位有吉星 → 削弱原 Argala 的吉力
    Virodha 位有凶星 → 削弱原 Argala 的凶力
    
  最终 Argala 净分 = Σ(Argala) - Σ(Virodha Argala)

判定：
  净分 ≥ +1.5  → 强加持（主题大顺，可大胆推进）
  净分 +0.5 ~ +1.5 → 中等加持（主题顺利但需努力）
  净分 -0.5 ~ +0.5 → 中性（按基础主题展开）
  净分 -0.5 ~ -1.5 → 中等阻挡（主题受阻，需绕路）
  净分 ≤ -1.5  → 强阻挡（主题大幅打折或转向反面）
```

## 实战示例

```
示例 1：Chara MD = 本盘 7 宫（关系主题）
  Lagna = Cancer，所以 7 宫 = Capricorn

  查 Argala 位（从 Capricorn 起算）：
    4 宫从 Cap = Aries → 该宫行星：无 → Argala = 0
    2 宫从 Cap = Aquarius → 该宫行星：Jupiter 入庙 → Argala = +1.5
    11 宫从 Cap = Sagittarius → 该宫行星：Mercury 中性 → Argala = +1
    5 宫从 Cap = Taurus → 该宫行星：Venus 入庙 → Argala = +1.5
  
  查 Virodha 位：
    10 宫从 Cap = Libra → 该宫行星：无 → Virodha = 0
    12 宫从 Cap = Sagittarius → ... (与 11 宫共宫，已计入)
    3 宫从 Cap = Pisces → 该宫行星：无 → Virodha = 0
    9 宫从 Cap = Virgo → 该宫行星：Saturn 中性 → Virodha = -1
  
  净分 = (0 + 1.5 + 1 + 1.5) - (-1) = 5（注：Virodha 是减负数 = 加正数）
  
  判定：强加持
  
  解读：
  "这段 Chara MD 是关系大年，而且各方面的'干预力'都是吉星——
   Jupiter 提供智慧+扩张，Venus 提供美感+亲密，Mercury 提供沟通。
   只有从 Capricorn 起的 9 宫有 Saturn 提供一些'必须严肃以对'的克制力，
   但这不是阻挡，而是把关系从'热闹'锚定到'承诺'。
   翻译成人话：这是一个能从'恋爱'升级到'婚姻'的窗口。"

示例 2：Chara MD = 本盘 10 宫（事业主题）
  ...同样的算法 → 净分 -1.8 → 强阻挡
  
  解读：
  "虽然这段 Chara 走到事业宫，看起来是事业大年，
   但所有 Argala 位的行星都在制约——
   翻译成人话：事业有机会但绊脚石很多，'卡点年'。
   不是不要做事业，而是要预料每一步都会有阻力，做好心理准备。"
```

## Argala 与 Vimshottari 的交叉

```
Argala 是 Chara Dasha 专属工具，但可以与 Vimshottari 交叉验证：

  Chara MD 强加持 + Vimshottari 当前 MD/AD 也是吉星 → 双重确认
  Chara MD 强加持 + Vimshottari 当前 MD/AD 是凶星 → 矛盾，按"心理外在分层"
    （Vim 是心理：可能心累；Chara 是外在：但事顺）
  Chara MD 强阻挡 + Vimshottari 吉星 → 同上反向（心情好但事情卡）
  Chara MD 强阻挡 + Vimshottari 凶星 → 双重确认（这段时间最难，做好准备）
```

## 何时在 timing 中启用 Argala

```
启用条件：
  - Mode B Chara Dasha 主题已判定后，希望细化"是顺是逆"
  - 用户问"这段时间我做 X 会成吗"——给 X 涉及的宫位做 Argala 评分
  - 三 Dasha 交叉验证（cross_verification.md）中 Chara Dasha 的吉凶判定
    
默认 timing Mode B Step 2 中可启用，作为 Chara Dasha 主题判定后的"细化层"。

写作风格示例：
  ✅ "Chara 走到关系宫确实是关系大年，
      但配套的 4 宫 Argala（家人意见）有 Saturn 在制约——
      你可能心动到位但家里会有一关要过。"
  
  ❌ "Argala 净分 +3.5，Virodha -1.2，故关系主题强加持。"
      （参数化、不解释、堆术语，禁止）
```
