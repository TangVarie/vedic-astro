# vedic-astro · Claude Code 插件市场

一个 Claude Code marketplace,当前收录 **vedic-astrology**(吠陀占星全流程分析,十 skill 协同,v1.2.0)。别人加一次市场、装一次插件即可使用。

```
vedic-astro-market/
├── .claude-plugin/
│   └── marketplace.json        # 市场清单(name=vedic-astro)
├── plugins/
│   └── vedic-astrology/        # 插件本体(10 skill, v1.2.0)
│       ├── .claude-plugin/plugin.json
│       ├── skills/ …
│       ├── requirements.txt
│       ├── README.md           # 插件自己的说明(架构/使用流程)
│       └── CHANGELOG.md
└── README.md                   # 本文件
```

> 这里有两个名字,别混:
> - **市场名 `vedic-astro`** — 来自 `marketplace.json` 的 `name`,用在 `install ...@vedic-astro`。
> - **仓库路径 `<你的用户名>/<仓库>`** — 用在 `marketplace add`。两者不必相同。

---

## 一、你(发布者):push 到 GitHub

把整个 `vedic-astro-market/` 目录作为一个仓库 push。新建仓库或复用现有仓库都行。

```bash
cd vedic-astro-market
git init
git add .
git commit -m "vedic-astro marketplace + vedic-astrology v1.2.0"
git branch -M main
git remote add origin git@github.com:TangVarie/vedic-astro.git   # ← 换成你的仓库
git push -u origin main
```

> ⚠️ 相对路径的 `source` **只在通过 Git 添加市场时有效**(GitHub/GitLab/git URL)。所以必须 push 到 git 仓库,不能让别人靠直链 JSON 安装。

---

## 二、别人:两条命令安装

```bash
# 1) 添加市场(参数是你的仓库路径 owner/repo)
claude plugin marketplace add TangVarie/vedic-astro     # ← 换成你 push 的仓库

# 2) 安装插件(参数是 插件名@市场名)
claude plugin install vedic-astrology@vedic-astro
```

也可在 Claude Code 会话里用斜杠命令:`/plugin marketplace add TangVarie/vedic-astro` 然后 `/plugin install vedic-astrology@vedic-astro`,或直接 `/plugin` 打开图形选择器。

安装后插件自动加载,10 个 skill 可触发,也可手动 `/vedic-core`、`/vedic-reader` 等调用。日后你 push 新版本(记得在 `plugin.json` 里 bump `version`),用户 `/plugin update vedic-astrology` 即可升级。

---

## 三、依赖(必看,否则计算基座起不来)

`vedic-calculator` 需要外部库,**Python 必须 3.8~3.13**(3.14 装不上 pysweph)。Marketplace 安装会把插件复制进缓存目录,最稳的做法是直接装这组:

```bash
pip install pysweph dashaflow PyJHora pytz markdown ephem python-pptx
# 系统 Python 报 externally-managed 就加 --break-system-packages
```

(Claude 首次运行 calculator 时通常也会自动检测并安装;不装的话,reader 读已有星盘仍可用,但原生排盘和精度全废。)详见插件内 `plugins/vedic-astrology/README.md`。

---

## 四、改名(如果你想换)

**换市场名**(影响 `install ...@新名`):改 `.claude-plugin/marketplace.json` 的 `name` 一处即可。

**换插件名**(影响 `install 新名@...`):要同步改三处 + 一个文件夹名——
1. `plugins/vedic-astrology/.claude-plugin/plugin.json` 的 `name`
2. `.claude-plugin/marketplace.json` 里 `plugins[0].name`
3. `.claude-plugin/marketplace.json` 里 `plugins[0].source`(用了 `pluginRoot` 简写,值=文件夹名)
4. 把文件夹 `plugins/vedic-astrology/` 重命名为新名

改完跑一下 `claude plugin validate .`(若装了 Claude Code)确认无误。

> ⚠️ 保留名不可用:`claude-code-marketplace`、`claude-code-plugins`、`claude-plugins-official`、`anthropic-marketplace`、`anthropic-plugins`。

---

## 版本

- 市场:v1.0.0(首发,收录 vedic-astrology v1.2.0)
- 插件变更见 `plugins/vedic-astrology/CHANGELOG.md`
