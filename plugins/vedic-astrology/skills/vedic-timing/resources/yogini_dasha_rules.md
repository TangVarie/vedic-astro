# Yogini Dasha 规则参考

> 来源：Parashari + KN Rao 教学（北印度 Bhrigu 派传承）
> 用途：vedic-timing Mode B (多 Dasha) Step 0 计算 + Step 3 解读

---

## 什么是 Yogini Dasha

8 大运循环、总长 36 年的短周期 Dasha。
特点：
- 每个 Yogini 时长 1-8 年（变化）
- 与 Vimshottari 完全独立
- 因为周期短、循环快，对短期事件触发力强

---

## 8 大 Yogini

```
| Yogini  | 对应行星 | 时长 | 自然性质 |
|---------|---------|------|---------|
| Mangala | Moon    | 1年  | 吉      |
| Pingala | Sun     | 2年  | 凶      |
| Dhanya  | Jupiter | 3年  | 大吉    |
| Bhramari| Mars    | 4年  | 凶      |
| Bhadrika| Mercury | 5年  | 吉      |
| Ulka    | Saturn  | 6年  | 凶      |
| Siddha  | Venus   | 7年  | 大吉    |
| Sankata | Rahu    | 8年  | 凶      |

合计 = 1+2+3+4+5+6+7+8 = 36 年（一个完整循环）
```

---

## 起算规则

起算 Yogini 由 **Moon Nakshatra** 决定。
27 个 Nakshatra 按 8 个一循环映射到 Yogini。

### ⚠️ 派系立场（v3.3 修订，反馈核查后澄清）

```
本系统采用：KN Rao 传承中常用的 Yogini Dasha 映射
（与若干主流 BPHS 注释版本一致）

理由：
  1. 全系统底色对齐 KN Rao（vedic-core / Chara Dasha 均同源）
  2. KN Rao 在《Yogini Dasha》专著中明确给出此映射并配大量临床案例
  3. 该映射对 Purva Bhadrapada 不重复使用（清晰）

替代派系（约 15-20% 案例会得到不同结果）：
  - BV Raman 派：起算行星不同（细节因来源而异）
  - SJC (Sanjay Rath) 派：部分 Nakshatra 重复使用
  - 某些南印度本土传承 / 地方传承的 BPHS 版本：起算映射有偏差
  
  ⚠️ v3.3 澄清：v3.2 曾把"古典 BPHS"列为替代派系，
  与下面 Canonical 表"KN Rao 派 / 标准 BPHS"自相矛盾。
  实情是：KN Rao 使用的版本与多数主流 BPHS 注释一致，
  地方传承版本视为替代派系。

如何使用：
  - 默认使用 KN Rao 主映射（下表唯一 canonical 表）
  - 如果跑 Mode B 三 Dasha 交叉验证命中率 < 40% → 用 v3 加权 Jaccard
    判断是不是时间问题（先 rectifier）而不是流派问题
  - 在 dc0_dasha_tables.md 中记录所用派系（默认 "KN Rao"）

⚠️ v3.2 紧急修订记录：
  v3.1 改写时用了错误的公式 ((N-1)%8)+1，导致所有 27 个 Nakshatra
  对应的 Yogini 全部错位（错 4 位）。
  v3.2 改回标准公式 (N+3)%8，与 KN Rao《Yogini Dasha》原典对齐。
  关键验证：Ashwini → Bhramari (不是 Mangala)、Ardra → Mangala、
            Mrigashira → Sankata、Anuradha → Bhramari。
```

### Canonical 表：Nakshatra → Yogini (KN Rao 传承)

按 8 个 Yogini 分组（更易记忆）：

```
Mangala  (Moon, 1 年):     Ardra(6),  Chitra(14), Shravana(22)
Pingala  (Sun, 2 年):      Punarvasu(7), Swati(15), Dhanishta(23)
Dhanya   (Jupiter, 3 年):  Pushya(8), Vishakha(16), Shatabhisha(24)
Bhramari (Mars, 4 年):     Ashwini(1), Ashlesha(9), Anuradha(17), P.Bhadrapada(25)
Bhadrika (Mercury, 5 年):  Bharani(2), Magha(10), Jyeshtha(18), U.Bhadrapada(26)
Ulka     (Saturn, 6 年):   Krittika(3), P.Phalguni(11), Mula(19), Revati(27)
Siddha   (Venus, 7 年):    Rohini(4), U.Phalguni(12), P.Ashadha(20)
Sankata  (Rahu, 8 年):     Mrigashira(5), Hasta(13), U.Ashadha(21)
```

按 27 Nakshatra 顺序展开（用于查表）：

```
#   Nakshatra        Yogini      行星        时长
─────────────────────────────────────────────────
1   Ashwini          Bhramari    Mars         4 年
2   Bharani          Bhadrika    Mercury      5 年
3   Krittika         Ulka        Saturn       6 年
4   Rohini           Siddha      Venus        7 年
5   Mrigashira       Sankata     Rahu         8 年
6   Ardra            Mangala     Moon         1 年
7   Punarvasu        Pingala     Sun          2 年
8   Pushya           Dhanya      Jupiter      3 年
9   Ashlesha         Bhramari    Mars         4 年
10  Magha            Bhadrika    Mercury      5 年
11  P.Phalguni       Ulka        Saturn       6 年
12  U.Phalguni       Siddha      Venus        7 年
13  Hasta            Sankata     Rahu         8 年
14  Chitra           Mangala     Moon         1 年
15  Swati            Pingala     Sun          2 年
16  Vishakha         Dhanya      Jupiter      3 年
17  Anuradha         Bhramari    Mars         4 年
18  Jyeshtha         Bhadrika    Mercury      5 年
19  Mula             Ulka        Saturn       6 年
20  P.Ashadha        Siddha      Venus        7 年
21  U.Ashadha        Sankata     Rahu         8 年
22  Shravana         Mangala     Moon         1 年
23  Dhanishta        Pingala     Sun          2 年
24  Shatabhisha      Dhanya      Jupiter      3 年
25  P.Bhadrapada     Bhramari    Mars         4 年
26  U.Bhadrapada     Bhadrika    Mercury      5 年
27  Revati           Ulka        Saturn       6 年
```

计算公式（KN Rao 派 / BPHS 标准）：

```python
def get_starting_yogini(nakshatra_number):
    """
    输入: nakshatra_number (1-27, Ashwini=1)
    输出: 起算 Yogini 名称
    
    公式: remainder = (N + 3) % 8
    """
    remainder = (nakshatra_number + 3) % 8
    yogini_map = {
        0: 'Sankata',   # Rahu, 8 年
        1: 'Mangala',   # Moon, 1 年
        2: 'Pingala',   # Sun, 2 年
        3: 'Dhanya',    # Jupiter, 3 年
        4: 'Bhramari',  # Mars, 4 年
        5: 'Bhadrika',  # Mercury, 5 年
        6: 'Ulka',      # Saturn, 6 年
        7: 'Siddha',    # Venus, 7 年
    }
    return yogini_map[remainder]

# 等价的另一种写法：
# yogini_index = ((nakshatra_number + 2) % 8) + 1
# 其中 1=Mangala, 2=Pingala, 3=Dhanya, 4=Bhramari,
#      5=Bhadrika, 6=Ulka, 7=Siddha, 8=Sankata
```

### 验证关键案例

```
Ashwini  (#1):  (1+3) % 8 = 4 → Bhramari  ✅
Ardra    (#6):  (6+3) % 8 = 1 → Mangala   ✅
Mrigashira (#5): (5+3) % 8 = 0 → Sankata  ✅
Pushya   (#8):  (8+3) % 8 = 3 → Dhanya    ✅
Anuradha (#17): (17+3) % 8 = 20 % 8 = 4 → Bhramari ✅
Revati   (#27): (27+3) % 8 = 30 % 8 = 6 → Ulka     ✅
```

实践中：

```
如果发现该 Yogini Dasha 在已知事件年份上完全对不上，
不要先怀疑映射，而是先怀疑 Moon 经度（出生时间）。

Moon 移动速度参考：每天约 13.2°，每小时 ≈ 0.55°，每分钟 ≈ 0.0092° (≈ 0.55')

Moon Nakshatra 边界敏感度（v3.3 修订，反馈核查后）：
  - Moon 距 Nakshatra 边界 < 0.01° (≈ 0.6') → 1 分钟级时间误差可能跨边界，
    属于"分钟级临界区"，必须 rectifier
  - Moon 距边界 < 0.5° (≈ 1 小时内移动距离) → 时-级敏感区，
    应检查出生时间精度（医院记录/家人回忆）
  - Moon 距边界 ≥ 0.5° → 安全区

→ 边界敏感时先跑 vedic-rectifier 看 Moon Nakshatra 是否稳定。
```

---

## 起算时长修正（Nakshatra 完成度）

```
出生时 Moon 已经走完 Nakshatra 的一部分，所以起算 Yogini 不是完整时长，
而是按"剩余比例"截短。

计算：
  Nakshatra 完成比例 = Moon 在该 Nakshatra 中已走过的度数 / Nakshatra 总跨度 (13°20')
  起算 Yogini 剩余时长 = (1 - 完成比例) × 该 Yogini 标准时长

例：
  Moon 在 Pushya 第 2 pada
  Pushya 总跨度 13°20' (= 800')，每 pada 跨度 3°20' (= 200')
  Moon 在 Pushya 内的位置 = 假设 6°40' (= 第二 pada 末尾)
  完成比例 = 6°40' / 13°20' = 50%
  起算 Yogini = Dhanya (Jupiter)，标准 3 年
    (Pushya 编号 8, (8+3)%8=3 → Dhanya)
  剩余 = (1 - 0.5) × 3 = 1.5 年
  
  所以该人出生时正在 Dhanya Yogini 的中期，剩余 1.5 年。
  接下来按 Bhramari (4年) → Bhadrika (5年) → ... 依次循环。
```

---

## 顺序

Yogini 顺序固定循环：
```
Mangala → Pingala → Dhanya → Bhramari → Bhadrika → Ulka → Siddha → Sankata → Mangala → ...
```

无论起算是哪个 Yogini，下一个永远是序列中的下一个，循环不变。

---

## Antardasha（小运）

```
每个 Yogini MD 内有 8 个 AD。

⚠️ AD 顺序规则（v3.4 修正）：
  每个 Yogini MD 内的 AD 从该 MD 自身开始，再按自然顺序循环 8 个 Yogini。
  不是从 Mangala 开始；不是固定从 1 号位开始。

每个 AD 时长 = 该 MD 时长 × (AD Yogini 时长 / 36)

例：
  Dhanya MD = 3 年 = 36 个月
  其中（从 Dhanya 自己开始，按自然顺序循环）：
    Dhanya AD    = 36 × (3/36) = 3 个月    ← 从 MD 自身开始
    Bhramari AD  = 36 × (4/36) = 4 个月
    Bhadrika AD  = 36 × (5/36) = 5 个月
    Ulka AD      = 36 × (6/36) = 6 个月
    Siddha AD    = 36 × (7/36) = 7 个月
    Sankata AD   = 36 × (8/36) = 8 个月
    Mangala AD   = 36 × (1/36) = 1 个月    ← 循环回到序列开头
    Pingala AD   = 36 × (2/36) = 2 个月
  合计 = 36 个月 ✓

  对其他 MD 同理：
    Mangala MD（1 年）→ AD 顺序：Mangala, Pingala, Dhanya, ..., Sankata
    Sankata MD（8 年）→ AD 顺序：Sankata, Mangala, Pingala, ..., Siddha
    每个 MD 都从自己开始循环，不是固定顺序。

⚠️ 旧文档曾把例子写成"Mangala AD 开头"，那是错的——它会让模型
   在每一个 Yogini MD 里都从 Mangala 开始排 AD，是把 MD 起点和
   AD 起点弄混了。Yogini Dasha 的"起点"规则（从 Janma Nakshatra
   对应的 Yogini 开始）只决定第一个 MD 是哪个，不决定 AD 顺序。
```

---

## 解读规则（Step 3 用）

### 基本判定

```
对每个 Yogini MD，综合考虑：

1. Yogini 自然性质（吉/凶）
2. 该 Yogini 对应行星在本盘的状态：
   - P1 身份（功能性吉凶）
   - P7 尊贵度
   - P9 Shadbala 强度
   - 落宫
3. 该行星管的宫位

综合公式：
  Yogini 自然吉 + 行星本盘强 + 行星功能吉 = 大吉年
  Yogini 自然吉 + 行星本盘弱 = 吉但温吞
  Yogini 自然凶 + 行星本盘弱 + 行星功能凶 = 警示年
  Yogini 自然凶 + 行星本盘强 + 行星功能吉 = "高压有产出"年
```

### 具体 Yogini 主题

```
Mangala (Moon, 1年)：
  情绪/家庭/生育/居所主题
  通常是"小休整"或"小新生"
  Moon 强 → 内心宁静、母系顺利
  Moon 弱 → 情绪波动、家庭张力

Pingala (Sun, 2年)：
  权威冲突/父亲/事业曝光/健康主题
  通常是"对抗权威"或"被赏识"
  Sun 强 → 升职、立威、被认可
  Sun 弱 → 与领导/父亲冲突、健康问题（心脏/背）

Dhanya (Jupiter, 3年)：
  学习/扩张/智慧/子女/导师主题
  通常是"扩张窗口"
  Jupiter 强 → 教育突破、生育、得贵人
  Jupiter 弱 → 过度乐观、错过机会
  注意：3年期较长，往往涵盖人生里程碑

Bhramari (Mars, 4年)：
  冲突/行动/手术/兄弟/挑战主题
  通常是"高强度行动期"
  Mars 强 → 大胆突破、创业、立功
  Mars 弱 → 冲突频繁、事故、过劳

Bhadrika (Mercury, 5年)：
  沟通/学习/事务/写作/技能主题
  通常是"知识积累期"
  Mercury 强 → 学业/事业精进、关键技能习得
  Mercury 弱 → 决策困难、沟通误解、神经系统压力

Ulka (Saturn, 6年)：⚠️ 警示
  限制/责任/损失/老人/拖延主题
  通常是"清账期"或"漫长建设期"
  Saturn 强 → 高压但有重大成就（这是奠基期）
  Saturn 弱 → 抑郁、停滞、长辈过世
  注意：如果 Ulka 与 Sade Sati 叠加 → 双 Saturn，烈度最高

Siddha (Venus, 7年)：
  爱情/艺术/物质享受/优雅主题
  通常是"人生黄金期"（如出现在适当年龄段）
  Venus 强 → 婚姻、艺术成就、财富、享乐
  Venus 弱 → 感情纠葛、物质失衡、放纵
  注意：7年期最长（与 Sankata 并列），通常对应人生最快乐或最沉迷的时期

Sankata (Rahu, 8年)：⚠️ 警示
  野心/迷雾/突变/外缘/危机主题
  通常是"转折期"
  Rahu 强（与吉星合相、相位）→ 重大突破、移民、转行成功
  Rahu 弱（与凶星合相、空巢）→ 迷茫、错误决策、健康危机
  注意：8年期最长且通常对应人生重大转折点
```

---

## Yogini Dasha 的特长

```
Yogini 比 Vimshottari 强的地方：
  1. 周期短，对"具体某年发生什么"的精度更高
  2. Yogini 命名带有强烈主题色彩，更易解读
  3. 与 Vimshottari 完全独立（基于不同算法）
  
Yogini 不如 Vimshottari 的地方：
  1. 总长仅 36 年，要循环 2-3 次才能覆盖一生
  2. 不同循环的同一 Yogini 表达可能差异大（受当时 Vimshottari 和 Gochara 影响）
  3. 派系起算差异（如前述双值）需要回测校准

最佳使用方式：
  把 Yogini 看作 Vimshottari 的"主题强化器"
  当 Vimshottari MD 表达模糊时，Yogini 给出更鲜明的主题指向
```

---

## 历史回测示例

```
当 Vimshottari Saturn MD + Yogini Ulka (Saturn)：
  Vimshottari 给"长期主题：限制/责任"
  Yogini 给"具体 6 年内：损失/老人/拖延"
  双 Saturn 叠加 = 该 6 年极重的 Saturn 表达
  
当 Vimshottari Saturn MD + Yogini Siddha (Venus)：
  Vimshottari 给"长期主题：限制/责任"
  Yogini 给"具体 7 年内：爱情/艺术/享乐"
  混合主题 = "在压力中找到生活质感"，常对应"压力中谈恋爱/结婚"
  
当 Vimshottari Jupiter MD + Yogini Dhanya (Jupiter)：
  Vimshottari 给"长期主题：智慧/扩张"
  Yogini 给"具体 3 年内：学习/扩张/子女"
  双 Jupiter 叠加 = 该 3 年人生黄金窗口
```
