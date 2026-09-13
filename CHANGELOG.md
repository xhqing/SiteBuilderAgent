# Changelog

本项目所有重要变更均记录在此文件中。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

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
