# Changelog — vedic-astrology 插件打包

> 记录的是「打包/集成」层面的变更。各 skill 自身的内部版本(core/soul v3.x、reader/calculator 上游 v6.0)见各自 SKILL.md。

## [1.2.0] — 方法论收紧 + P0 契约闭环
- **soul 核心态度**补两条盲审纪律:`禁止反向推导`(与 core 统一)、`双向陈述`(与 timing 统一)——补上灵魂层这个最易谄媚领域缺失的护栏。
- **PAC 原则轻量植入** soul(Step 6 合成段)与 timing(写作风格段):结论先合成一句"做什么+怎么做+在哪"的人话再展开,不照搬 core 的逐星 PAC 步骤。
- **P0 契约闭环**:`data_contract.md` 元信息段补 `时间可信度 / 信号解释置信度 / 信号修正日志` 三字段;reader 的 WRITE 3 增 item 11,由「有效精度」「验前事校准率」派生回填这两维度。下游 6 引擎(约 47 处依赖)的"验前事复盘"不再空转。

## [1.1.0] — 补齐数据入口,十 skill 完整
- 从上游 v6.0 纳入 **vedic-reader**(提取入口)+ **vedic-calculator**(原生排盘计算基座,pysweph/PyJHora)。
- requirements 并入 calculator 重依赖;标注 Python 必须 3.8~3.13;纳入 MIT LICENSE。

## [1.0.0] — 首次打包
- 把本地 8 skill(core/career/love/soul/timing/rectifier + 2 eval)收入单插件;扁平 skills/ 布局保留全部跨 skill 相对引用。缺数据入口(见 1.1.0 补齐)。
