# Vedic Astrology Suite (`vedic-astrology`)

吠陀占星(Jyotish)全流程分析套件,打包为单个 Claude Code 插件,**十个 Skill 协同**——从原生排盘到完整人生审计。所有 skill 收进一个 `skills/` 目录,相对引用与脚本调用全部保留,一次安装即可全局使用。

上游来源:<https://github.com/CNWU16/vedic-astro-skills> (MIT)。本插件 = 该仓库 v6.0 的 reader/calculator + 你本地扩展的 core/career/love/rectifier + 你新增的 soul/timing + 两套 eval。

---

## 架构:双入口 → 统一契约 → 六引擎

```
  星盘材料 (PDF/截图/文本)          出生信息 (日期+时间+地点)
        │                                  │
        ▼                                  ▼
 ┌──────────────┐                 ┌──────────────────┐
 │ vedic-reader │                 │ vedic-calculator │  ★计算基座
 │ 提取+校验     │                 │ 原生排盘(pysweph) │
 └──────┬───────┘                 └────────┬─────────┘
        │         structured_data.md        │  (formatter 输出,两者格式兼容)
        └───────────────┬───────────────────┘
                        ▼
        ┌───────────────────────────────────────────┐
        │  六大解读引擎(都读 structured_data.md)        │
        │  core(P1-P12+十大板块) · career(D10)         │
        │  love(5/7宫) · soul(Jaimini/SJC)             │
        │  timing(行运/Dasha/年盘) · rectifier(校时)    │
        └───────────────────────────────────────────┘

  开发期回归(改 skill 时用,不被普通分析触发):
    reader-eval(读盘准确率 vs JHora) · consistency-eval(跨 skill 事实一致性)
```

### 十个 Skill

| Skill | 角色 | 流派 |
|---|---|---|
| **vedic-calculator** | 原生排盘引擎,出生信息→structured_data.md。全系统计算基座 | pysweph + dashaflow + PyJHora |
| **vedic-reader** | 从 PDF/截图/文本提取,南北印图识别+16条数学校验 | 数据契约 data_contract.md |
| **vedic-core** | 核心审计 P1-P12 / 十大板块 / Q&A。枢纽 | KN Rao Parashari |
| vedic-career | 职业方向 D10 / L10 / AmK | KN Rao Parashari |
| vedic-love | 感情桃花 5/7 宫 · PK/DK · Upapada | Jaimini DK/UL + Parashari L7 |
| vedic-soul | 灵魂层 Karakamsa / Ishta Devata / 前世 | Jaimini Karaka + SJC |
| vedic-timing | 行运 Gochara / 多 Dasha 交叉 / Varshaphala 年盘(自带计算脚本) | Parashari + Tajaka |
| vedic-rectifier | 出生时间校准(5 大事件 + 天文扫描) | ephem 天文 |
| vedic-reader-eval | 评 reader 读盘准确率(对标 JHora 真值) | 开发工具 |
| vedic-consistency-eval | 查 core/career/love/soul 确定性事实是否打架 | 开发工具 |

---

## 安装

### 方式 A:Skills-directory 插件(推荐,零命令)

放在 skills 目录下、带 `.claude-plugin/plugin.json` 的文件夹,会在下次启动 Claude Code 时**自动就地加载**,无需 marketplace、无需 install。

```bash
# 个人级:所有项目可用
cp -r vedic-astrology ~/.claude/skills/

# 或项目级:仅该仓库(需接受目录 trust 对话框)
cp -r vedic-astrology <你的项目>/.claude/skills/
```

重启 Claude Code 或 `/reload-plugins`。加载后显示为 `vedic-astrology@skills-dir`,10 个 skill 自动可触发,也可手动 `/vedic-core`、`/vedic-reader` 等调用。

> 改 `SKILL.md` 当场生效;改 `plugin.json`、脚本等需 `/reload-plugins` 或重启。

### 方式 B:marketplace 分发(可选,团队共享时)

加 marketplace 描述文件走 `claude plugin install`。单机个人用方式 A 即可。文档:`code.claude.com/docs/en/plugin-marketplaces`。

---

## 依赖安装

```bash
cd ~/.claude/skills/vedic-astrology
pip install -r requirements.txt
# 系统 Python 报 externally-managed 时:
pip install -r requirements.txt --break-system-packages
```

⚠️ **vedic-calculator 是计算基座,所有 skill 的精度都依赖它。** 它需要 `pysweph + dashaflow + PyJHora + pytz`,且 **Python 必须 3.8~3.13**(3.14 暂无 pysweph 预编译 wheel)。其余:`markdown`(core 出报告)、`ephem`(rectifier 校时,缺它启动即失败)、`python-pptx`(可选导出)。

---

## 典型使用流程

```
排盘  → 二选一:
        · 有出生信息 → vedic-calculator 原生计算 → structured_data.md
        · 有星盘文件 → vedic-reader 提取+校验 → structured_data.md
分析  → "帮我分析这张盘" → vedic-core 跑 P1-P12 + 十大板块 → 主报告
深挖  → "看事业 / 感情 / 灵魂功课 / 近三年运势" → career/love/soul/timing 专题
校时  → "出生时间不准" → vedic-rectifier 用 5 个大事件校准
回归  → 改完某个 skill,用 *-eval 两套确认没退步(开发期)
```

---

## ✅ 集成注记:契约对齐(v1.2.0 已修复)

本插件把上游 reader/calculator 与你本地扩展过的解读引擎放在一起。曾有一处**版本错位**:你本地 6 个引擎期待 reader 在 meta 段写两个正交维度(**时间可信度** + **信号解释置信度**)外加**信号修正日志**(约 47 处依赖),而上游 v6.0 reader 只写单轴时间精度。

**v1.2.0 已闭环**:`data_contract.md` 元信息段补齐三字段,reader 的 WRITE 3 由「有效精度」「验前事校准率」派生回填这两维度。你的"验前事复盘归因"不再空转。详见随附《审计报告》与 `CHANGELOG.md`。

---

## 版本

- 插件:**v1.2.0**(soul 反锚定收紧 + PAC 原则植入 soul/timing + P0 契约闭环)
- v1.1.0:补齐 reader + calculator,十 skill 完整
- v1.0.0:首次打包(8 skill,缺数据入口)
- 完整打包变更见 `CHANGELOG.md`。各 skill 内部保留自身版本(core/soul/timing 多为 v3.x;reader/calculator 来自上游 v6.0)。
