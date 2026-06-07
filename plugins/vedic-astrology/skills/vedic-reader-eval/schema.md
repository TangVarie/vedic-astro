# schema · ground_truth.json / reader_output.json 字段定义

两个文件**用同一套结构**，这样 `score_extraction.py` 能逐字段比对。
真值(ground_truth)从 JHora 填；reader 输出(reader_output)从 reader 的 `structured_data.md` 归一化而来。

```jsonc
{
  "chart_id": "string",                 // 唯一标识，建议和 fixtures/<id>/ 目录名一致

  "meta": {
    "ayanamsa": "Lahiri",               // ⚠️ 必须和你 JHora 的设置一致
    "node_type": "mean",                // "mean" 或 "true"，照你 JHora 的设置
    "birth": "可选，仅备注用"
  },

  "d1": {                               // 9 行星 + Lagna
    "Sun":  { "sign": 2, "deg_in_sign": 29.13, "retrograde": false, "nakshatra": 5, "pada": 4 },
    "Moon": { "sign": 11, "deg_in_sign": 12.4, "retrograde": false, "nakshatra": 24, "pada": 2 },
    // ... Mars / Mercury / Jupiter / Venus / Saturn / Rahu / Ketu 同上 ...
    "Lagna":{ "sign": 4, "deg_in_sign": 16.9 } // Lagna 无 retrograde / nakshatra 字段
  },

  "d9":  { "Sun": 7, "Moon": 8, /* ... 9 行星 ... */ "Lagna": 3 },  // 值 = 星座 1..12

  "chara_karaka": {
    "scheme": "8K",                     // "7K" 或 "8K"
    "ak": "Sun",                        // 度数最高那颗（红线层会查）
    "order": ["Sun","Venus","Jupiter","Mars","Moon","Rahu","Mercury","Saturn"]
                                        // 按 karaka 度数降序的完整排列（覆盖层会查）
  },

  "sav": [28,25,30,32,22,31,24,27,29,30,31,28],  // 12 宫 SAV，总和必须 = 337

  "vimshottari": [                      // 大运(Mahadasha)边界，至少几段
    { "lord": "Venus", "start": "1989-01-01", "years": 20 },
    { "lord": "Sun",   "start": "2009-01-01", "years": 6  }
    // years 必须等于 Vimshottari 常数：Ke7 Ve20 Su6 Mo10 Ma7 Ra18 Ju16 Sa19 Me17
  ]
}
```

## 字段约定

| 字段 | 取值 | 谁会检查 |
|---|---|---|
| `d1[planet].sign` | 整数 1..12（Ar=1 … Pi=12） | A:范围 / B:红线 |
| `d1[planet].deg_in_sign` | 0 ≤ x < 30 | B:覆盖(±1°) |
| `d1[planet].retrograde` | bool；日/月恒 false，Rahu/Ketu 恒 true | A:铁律 / B:红线 |
| `d1[planet].nakshatra` / `pada` | 1..27 / 1..4 | A:与度数一致 / B:覆盖 |
| `d9[planet]` | 1..12 | A:与 D1 度数一致 / B:覆盖 |
| `chara_karaka.ak` | 行星名 | A:=排序首 / B:红线 |
| `chara_karaka.order` | 行星名数组 | A:与度数一致 / B:覆盖 |
| `sav` | 12 个非负整数，∑=337 | A:总和 |
| `vimshottari[].years` | 等于 Vimshottari 常数 | A:周期 |

## 行星名（固定拼写，区分大小写）

`Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu`，外加 `Lagna`。

## 可选 / 扩展字段

`d10` / `d4` / `d5`（结构同 `d9`）、`shadbala`、`bav` 等可加入。
当前两个检查器只比对上面列出的字段；要纳入分盘 D10/D4/D5 的覆盖评分，
在 `score_extraction.py` 里仿照 `d9` 那段加即可（结构完全一样）。

> 偷懒做法：把 JHora 的行星表/Dasha 文字粘给 Claude，说"按 vedic-reader-eval 的 schema 吐
> ground_truth.json"，让它做归一化。同样地，reader 的 `structured_data.md` 也可以这样转成
> `reader_output.json`。
