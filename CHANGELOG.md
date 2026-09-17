# Changelog

本项目所有重要变更均记录在此文件中。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 变更（接收 Wright 交接更新：Team Playbook 交付拆分为中英两版独立包）

- **为什么改**：Wright 侧按用户新规把产品交付由双语混装单 zip 物理拆分为英文版、中文版两个独立版本（源目录两棵同构树 + 分语言双 zip 口径），旧混装包废止仅存档；本仓 `handoff.md` 仍指向旧源目录与旧 zip，不同步则建设期会拿错交付物。
- **改了什么**（2026-09-17，由 Wright 侧更新）：`artifacts/handoff.md` 产物路径表改为一棵英文版源树 + 一棵中文版源树 + 分语言双 zip 口径（截至当日 zip 打包待执行，完成前勿上架任何 zip），旧混装单包标注废止存档；「交接了什么」、任务清单与核对清单同步。Payloadz 上架按英文版、中文版两包处理（可各自 SKU）。
- **边界**：仅更新交接输入文件；产品内容零改动（拆分只动文件组织、文件名与链接层）；定价等付费层细节仍见被忽略的 handoff 与 Wright 侧《产品说明》，不入公开明文。

### 新增（payloadz-login skill：凭证不进对话上下文的自动登录）

- **为什么改**：建设期任务清单里的 Payloadz 支付链路配置需要登录卖家账户；用户明确提出隐私顾虑——不能用 read 工具直接读凭证文件，否则密码明文进入对话上下文随请求发给模型服务商。解法是把登录动作打包成 skill：脚本进程自己读本地凭证、自己操作浏览器填表，对话上下文从头到尾只有文件路径。
- **改了什么**（2026-09-17）：新建 `.claude/skills/payloadz-login/`（经 `.pi/skills` 软链接对 pi 可见）：`SKILL.md`（触发场景 / 用法 / 退出码表 / 安全纪律：绝不用 read 读凭证）+ `scripts/login.py`（Python Playwright：读 `~/.payloadz/credentials.json` → 系统 Chrome（`channel='chrome'`，实测 agent-browser 自带 chromium 与 Python playwright 版本不匹配故弃用）持久化 profile 打开 `login.aspx` → 填 `#loginUsername` / `#loginPassword` / 勾选记住我 → 点 "Login To Your Account" → 等 URL 离开登录页判成功；reCAPTCHA 拦截时自动保持浏览器窗口供人工接管；登录态存 `~/.payloadz/browser-profile/`，二次调用直接复用会话）。配套：`~/.payloadz/credentials.json` 凭证文件（600 权限，用户主目录、不入仓）；`.gitignore` 追加 `__pycache__/`（py_compile 缓存实测会被跟踪）。
- **验证**：登录页结构为 2026-09-17 真实浏览器实测（主页链接指向 `/login.aspx`，表单字段见上）；脚本语法检查、空凭证分支（退出码 3 + 填写提示）、`--help` 实测通过；真实登录待用户填完凭证后跑通。

### 新增（接收 Wright→Mason 建设期交接：artifacts/handoff.md）

- **为什么改**：Mason 反馈未收到 Wright 最新成品数字产品的交接——核实属实：Wright 侧成品与《产品说明》早已就绪，但从未向本仓做交接动作，且付费产物只存在于 Wright 仓被 .gitignore 忽略的本机目录中，本会话无从得知其位置与用途，建设期（流水线第 ③ 步）无法开工。
- **改了什么**（2026-09-16，由 Wright 侧写入）：新建 `artifacts/handoff.md` 交接输入（放在本仓既有的产物接力忽略目录内，勿公开勿提交），含：产物本机路径表（《产品说明》/ 成品源目录 / 交付实物 zip）、建设期任务清单（Payloadz + PayPal 支付链路配置、落地页、建好购买链接交 Buzz）、渠道硬约束（Gumroad 不可用）、付费产物严禁推公开仓库警示、交接核对清单。定价等付费层细节不写入本条目（CHANGELOG 会公开），见被忽略的 handoff 与 Wright 侧《产品说明》。
- **边界**：仅新增交接输入文件，未动本仓任何既有文件；handoff.md 已确认被 `.gitignore` 的 `artifacts/` 规则忽略（`git check-ignore` 实测通过）。

### 新增（落地页第一版：site/ 静态单页 + 无后端统计架构）

- **为什么建**：Wright 交接的建设期任务清单第 2 项「落地页部署（可选）」，经查证 Payloadz 自带页面只提供累计浏览计数、不允许在销售页埋自定义统计代码（官方帮助中心全量 227 篇确认），拿不到 landing_page_view 级别的漏斗数据，判定「自带页面不够用」——自建落地页以补齐数据层（浏览 → 出站点击 → 成交的完整漏斗，供 Echo 复盘）。
- **改了什么**（2026-09-17）：新建 `site/` 目录：`index.html`（英文单页，文案取自《产品说明》：人群 / 7 模块 / open-core 边界第一屏明示 / 定价）、`style.css`（深色主题、无外部依赖）、`analytics.js`（GA4 + Meta Pixel + Cloudflare Web Analytics 动态注入，均按配置存在与否开关；CTA 点击手动事件 + beacon transport 兜底，防导航前丢失）、`config.example.js`（配置占位符模板）、`README.md`（配置与部署说明）；`.gitignore` 追加 `site/config.js`（运行时真实值仅存本机）。
- **架构决策**：纯静态、无后端、无数据库——浏览与点击数据全部由第三方统计服务托管，成交层由 Payloadz「Download Page Text」字段贴转化码补齐；CTA 在购买链接未配置时保持禁用态（URL 格式校验防止占位符误激活）。
- **验证**（headless Chrome 实测）：占位符配置下三个 CTA 按钮全部正确禁用；合法配置下按钮激活、早鸟横条显隐与兑换码填充正确、GA4 / CF beacon 脚本正确注入。

### 变更（落地页 What's inside 副标修正：「you clone and run」→「clone-ready」）

- **为什么改**：用户核对文案与交付实物发现失实——副标「a bundle you clone and run」中 "run" 一词为落地页写作时自行引入，《产品说明》原话是「clone-ready bundle」；交付 zip 实测 20 文件全为 Markdown 手册 + 空白模板 + SVG 图表，无 .git、无任何可执行内容，买家按 README Quick Start 自建仓库（`git init`），bundle 是动手原料而非可运行物。目标买家为跑 agent harness 的技术人群，"clone and run" 会造成「解压即得可跑仓库」的预期落空（退款 / 争议风险），且与 open-core 定位（代码免费、付费层卖的是组织方法）自相矛盾。
- **改了什么**（2026-09-17）：`site/index.html` What's inside 副标「a bundle you clone and run.」→「a clone-ready bundle.」，回归 spec 原话口径；页面其余 clone 表述（hero 副标 / 数据条 / How it works 第 1 步 / 定价区）本就与 spec 一致，未动；hero 角标「clone & go」经用户确认保留。
- **溯源核查**：纯文案措辞修正，不动页面结构、价格与 CTA 行为，无回归风险。

## [0.1.0] - 2026-09-13

### 变更（CLAUDE.md 角色定位明确"建站工程师"本质是搭成交基础设施）

- **为什么改**：团队讨论指出岗位名 SiteBuilder 字面偏窄——Mason 不一定建站，phase-1 是 Payloadz 上架 + PayPal 配置（不写站点代码），建站只是成交基础设施的一种形态；但建站是他最具辨识度的招牌活，故保留名字、只统一描述口径。
- **改了什么**（2026-09-14）：`CLAUDE.md` 角色定位行「建站工程师」补为「建站工程师 / 成交基础设施工程师」，并加注本质=搭成交基础设施：独立站 / 落地页 / 支付配置。

### 变更（删除 site-builder skill 里的「主动调用 find-skill」执行原则）

- **为什么改**：全局 find-skill skill 已删除（2026-09-12 清理），`/find-skill`、`/install-skill` 命令已不存在，且实际使用中遇到建站 / 支付 / SEO 等难题时走网络搜索（anysearch / agent-reach）自然会把 skill 方案涵盖在搜索结果里，不会特地去只考虑 skill 方案，2026-09-13 用户指出后清理。溯源核查：该行是 2026-09-12 find-skill 清理的漏网残留，非任何修复逻辑的一部分，删除无回归风险。
- **改了什么**（2026-09-13）：`.claude/skills/site-builder/SKILL.md` 执行原则列表删除「主动调用 find-skill」一条，其余四条不变。

### 变更（清理已废止的「项目内置通用 skill 并与全局同步」规则：CLAUDE.md + README 中英双语）

- **为什么改**：通用能力开源模式已改为「单一出口」——只有 Prometheus（CapabilityManagerAgent）镜像全局 `~/.claude/` 的通用 skills / CLAUDE.md / docs 对外开源，其余 agent 项目不再内置通用 skill 副本、也不再与全局双向同步（团队注册表与 capability-sync.md 已先行更新）。本项目 `.claude/skills/` 下实际只剩 site-builder，CLAUDE.md 尾部「anysearch skill 同步」与「为什么开源项目要内置通用核心 skill」两节描述的同步义务与入仓标准均已废止，2026-09-13 用户指出后清理。
- **改了什么**（2026-09-13）：① `CLAUDE.md` 删除「## anysearch skill 同步（全局为权威副本）」与「## 为什么开源项目要内置通用核心 skill」两节；② `README.md` / `README_cn.md` 同步清理（中英两版对齐）：目录结构图删去实际不存在的 `anysearch/`、`find-skill/`、`rules/` 三行、补画 `.pi/skills` 软链接，设计原则句去掉已全局删除的 `/find-skill` 命令提及，License 节删去第三方 skill 声明句（仓库内已无第三方 skill）。溯源核查：anysearch 同步节无来历条目、非修复逻辑；README 树中那三行本就指向不存在的目录（2026-09-12 find-skill 清理的漏网），本次删除无回归风险。

### 变更（.claude/rules 内容并入 CLAUDE.md 正文）

- **为什么改**：`.claude/rules/` 没有自动加载机制，规则要生效必须进入某个 CLAUDE.md；pi 等 harness 也没有 Claude Code 的 `@` 引用语法，引用方式无法跨环境生效，2026-09-13 用户要求把规则内容全部并入正文。
- **改了什么**（2026-09-13）：`.claude/rules/passive-income-only.md`（聚焦被动收入）的完整内容作为新章节「## 聚焦被动收入」并入 `CLAUDE.md`，位置在「流水线位置」之后、「语言与排版」之前；标题相应降级（原文一级 / 二级 → 正文二级 / 三级）。原 rule 文件保留未动（内容现与 CLAUDE.md 重复，待用户决定去留）。

### 新增（.pi/skills 软链接指向 .claude/skills）

- **为什么建**：pi（coding agent harness）从项目 `.pi/skills/` 目录加载项目级 skill，与 Claude Code 的 `.claude/skills/` 是两套入口、同一份内容；为避免双目录重复维护导致漂移，2026-09-13 用户要求用软链接复用同一份源文件。
- **改了什么**（2026-09-13）：新建 `.pi/` 目录，并在其中建立软链接 `.pi/skills → ../.claude/skills`（相对路径，clone 后只要仓库结构不变链接即有效）。skill 的唯一维护源仍是 `.claude/skills/`，`.pi/skills/` 只是其别名入口。

### 变更（CLAUDE.md 删去「经验提炼」整节）

- **为什么改**：Claude 的 Auto Memory 功能已关闭，`.claude/memory/` 不复存在，「把 Auto Memory 的教训固化为项目规则」的整套工作流（识别 → 提炼 → 留针）失去前提，2026-09-13 用户指出后清理。
- **改了什么**（2026-09-13）：`CLAUDE.md` 删除「## 经验提炼：把 Auto Memory 的教训固化为项目规则」整节（含触发条件、为什么、怎么做、不必提炼的情况四个小节）。溯源核查：该节为早期同步的模板内容，CHANGELOG 无专门来历记录，不承担任何修复逻辑，删除无回归风险。

### 变更（CLAUDE.md 删去「由 Claude Code 自动加载」说明句）

- **为什么改**：用户 2026-09-12 要求 CLAUDE.md 不再强调本文由 Claude Code 加载，团队全部项目的 CLAUDE.md 统一清理此类语句。
- **改了什么**（2026-09-12）：`CLAUDE.md` 开头角色定位行删去句尾「本文件由 Claude Code 在每次会话开头自动加载。」，角色描述本身保留。

### 变更（find-skill 相关内容清理）

- **为什么改**：全局 find-skill skill 已被用户删除（实际使用中从未用到），项目内「find-skill skill 同步」专节与相关提及全部失效，2026-09-12 联动清理。
- **改了什么**：`CLAUDE.md`：①「像 anysearch、find-skill 这类通用 skill」→「像 anysearch 这类通用 skill」；②删除「## find-skill skill 同步（全局为权威副本）」整节（项目内 `.claude/skills/find-skill/` 副本此前已随全局删除，无目录残留；判断标准句「按上方规则双向同步」仍指上方 anysearch 同步节，无需改）。

### 变更（assets/logo.svg 副标题去中文）

- **为什么改**：全局规则新增「Logo / 图标资产文字一律用英文」（2026-09-12 用户立，起因 Swing 仓库 logo 副标题混入中文被指出）：logo 是面向全球读者的视觉标识，中文受众已有 README_cn.md 双语通道；且 SVG 中文依赖查看环境的字体回退，渲染不可控。本次为按新规批量清理存量。
- **改了什么**：`assets/logo.svg` 副标题「Site Builder · 建站工程师」→「Site Builder」。

### 变更（措辞统一 fleet → team / 舰队 → 团队：README 中英双语 + CLAUDE.md + site-builder skill）

- **为什么改**：用户 2026-08-16 已把 xhqing 主页 README 的自称从「舰队 / fleet」改为「团队 / team」，但本仓 README 中英两版、根 `CLAUDE.md` 与 site-builder skill 仍是 fleet 旧措辞——外部读者沿「主页 → 各 agent 仓库」浏览会看到两种自称并存；2026-08-21 用户裁定全量存量一次清零、统一为团队 / team。
- **改了什么**：`README.md` 3 处 fleet → team（Mason 引言、定位表 fleet step、six-agent fleet → team）；`README_cn.md` 对应 3 处舰队 → 团队；根 `CLAUDE.md`「舰队里的建站工程师」→「团队里的」；`.claude/skills/site-builder/SKILL.md`——description「agent of the fleet」→「of the team」、「角色范围（舰队分工）」→「（团队分工）」。职责、流水线结构（六步不变）、徽章均不变。

### 新增（项目立项：建站工程师 Agent Mason）

- **为什么建**：全局注册表已登记 Mason / SiteBuilderAgent（建设：搭成交基础设施——独立站建设 + 落地页技术与部署 + 支付渠道与接口配置；建设期位于 Wright 之后、Buzz 之前），本次按团队脚手架规范（2026-07-13 立）正式立项建仓。
- **改了什么**：建立角色化 `CLAUDE.md`（Mason 身份、产物契约、流水线位置）、中英双语 `README.md` / `README_cn.md`、`assets/logo.svg`、`LICENSE.md`（MIT）、`.gitignore`、`.claude/`（site-builder 专属 skill 等）。本 CHANGELOG 为立项后补建（2026-08-21），立项时间以仓库文件创建为准（2026-07-17 前后）。
