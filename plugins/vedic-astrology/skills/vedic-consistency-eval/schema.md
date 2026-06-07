# schema · canonical_facts.json / skill_claims_*.json

两者字段同构；`canonical_facts` 是完整的源数据真相，`skill_claims` 是各 skill 断言的**子集**。

## canonical_facts.json （从 structured_data.md 蒸馏）

```jsonc
{
  "chart_id": "string",
  "ak": "Sun",                          // Atmakaraka（度数最高，无争议）
  "d9_lagna": 9,                        // D9 上升星座 1..12
  "house_lords": {                      // 12 宫主，键 '1'..'12'，值=行星名
    "1": "Moon", "2": "Sun", "3": "Mercury", "4": "Venus",
    "5": "Mars", "6": "Jupiter", "7": "Saturn", "8": "Saturn",
    "9": "Jupiter", "10": "Mars", "11": "Venus", "12": "Mercury"
  },
  "planet_sign": {                      // 7 行星落座 1..12（可含 Rahu/Ketu）
    "Sun": 2, "Moon": 11, "Mars": 12, "Mercury": 2,
    "Jupiter": 3, "Venus": 1, "Saturn": 10
  },
  "planet_dignity": {                   // Exalted / Debilitated / Own / Other
    "Sun": "Other", "Saturn": "Own", "...": "..."
  },
  "dasha": [                            // 大运边界
    { "lord": "Venus", "start": "1989-01-01", "years": 20 },
    { "lord": "Sun",   "start": "2009-01-01", "years": 6 }
  ]
}
```

## skill_claims_<skill>.json （从某 skill 的输出抽取）

只放该 skill **明确陈述为事实**的项；没断言的字段直接省略。

```jsonc
{
  "skill": "career",                    // core | career | love | soul
  "ak": "Sun",                          // 可选
  "d9_lagna": 9,                        // 可选
  "house_lords": { "1": "Moon", "10": "Mars" },   // 可选，部分
  "planet_sign": { "Venus": 1 },        // 可选，部分
  "planet_dignity": { "Saturn": "Own" },// 可选，部分
  "dasha": [ { "lord": "Venus", "start": "1989-01-01", "years": 20 } ]  // 可选
}
```

## 比对规则（check_consistency.py）

| 字段 | 类型 | 保真度 | 跨 skill |
|---|---|---|---|
| `ak` / `d9_lagna` | 单值 | 与 canonical 相等 | 各 skill 之间相等 |
| `house_lords` / `planet_sign` / `planet_dignity` | 字典逐键 | 每键值与 canonical 相等 | 同键被多 skill 断言时彼此相等 |
| `dasha` | 列表(按 lord) | lord+起点(±31天)+周期一致 | — |

## 行星名 / 星座编号

行星：`Sun Moon Mars Mercury Jupiter Venus Saturn Rahu Ketu`。
星座：1=Ar … 12=Pi（`cutil.SIGN_NAMES`）。

> 抽取省事做法：把某 skill 的输出粘给 Claude，说"按 vedic-consistency-eval 的 schema
> 抽 skill_claims_<skill>.json，只抽它陈述为事实的确定性项"。
> 同样把 structured_data.md 粘给 Claude 让它吐 canonical_facts.json。
