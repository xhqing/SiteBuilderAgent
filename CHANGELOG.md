# Changelog

本项目所有重要变更均记录在此文件中。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增（接收第二个产品交接：Git 漫画书试读版 + 引流图卡）

- **为什么改**：Wright 完成 Scout 流水线第二件产品《Git: The Comic》英文试读版（`product_id: Git-Comic-v1`，20 页 PDF）+ 引流图卡包（`Git-Comic-Mini`，10 张 1080×1350），按「完成即交接」机制写入本项目被忽略目录的 `artifacts/handoff.md`（付费/引流产物不进公开仓库，本条目只记交接事实不展开产品细节）。
- **改了什么**（2026-09-18）：`artifacts/handoff.md` 追加「产品二」节：产物本机路径表（双 zip + 源目录 + 产品说明）、建设期待办（试读免费分发链路 + 图卡包上架，优先级可排在现有阵地工作之后）、渠道硬约束、交接核对清单。
- **边界**：试读验证策略下暂不为全本建任何东西（全本任务等验证结果另派）；产品内容与验收记录见 Wright 仓产品说明（本机路径在 handoff 内）。
### 新增（社交分享卡片：OG / Twitter meta + 1200×630 预览图）

- **为什么改**：Buzz 引流主战场是 X，帖子内链接卡片无图无描述会直接压点击率；落地页此前没有任何 OG / Twitter Card 标签（实测确认缺口），这是引流第一印象层面的硬缺口。
- **改了什么**（2026-09-18）：`site/og-image.svg` + `og-image.png`（1200×630，与落地页同风格：GitHub 深色系 + 蓝主色，视觉主体为 1 manager → 3 squads → 20 agents 的迷你组织图，按 icon-design 规范视觉资产文字用英文）；`index.html` 补齐 og:type / og:url / og:title / og:description / og:image + twitter:card（summary_large_image）全套；部署仓同步 push。
- **验证**：线上 og-image.png 200 可达、页面 og 标签 5 项在线；OCR 校验图内文字渲染正确。

### 新增（交付链路演习：Test Delivery 全链路实走 + 补录终验）

- **为什么改**：全链路此前只验证到「购买页正常」，买家付款后的真实路径（下载邮件 → 下载页 → 拿到文件 → GA4 成交记录）从未完整走过；等真实首单才发现交付问题就是差评事故，发引流前用官方 Test Delivery 功能演练。
- **改了什么**（2026-09-18）：无——纯验证性演习，未改任何线上配置（测试订单一笔：PL4AB57FA1E52449E，$0，英文版产品）。
- **验证结果（全过）**：① Test Delivery 发送成功（邮件送达卖家邮箱，后台给出下载 URL）；② 买家视角无登录态打开下载页：文案正常（产品名 / SKU / 订单摘要 / 支持邮箱），无残留乱码；③ 实际下载 zip：MD5 与源文件逐字节一致、解压完整无损（12 文件）；④ 批量补录工具抓到该订单（SKU 映射正确）并 dry-run 校验通过；⑤ 正式补录 204 收妥，状态文件去重落位（GA4 内新增一笔 $0 purchase 测试记录，可在 Realtime 查看）。

### 新增（T4 成交层落地：GA4 Measurement Protocol 补录制替代网页贴码）

- **为什么改**：T4 原方案（Payloadz「Download Page Text」字段贴 GA 转化码）实测不可行——该字段为纯文本，HTML 提交时被整体转义存储（`<script>` 存成 `&lt;script&gt;`，买家会看到乱码而非执行），且误存内容已当班清理恢复。备选的 Remote Download Page（远程下载页 + JS 变量注入）虽机制存在，但配置入口未公开、官方自述仅限罕见场景、直接改动买家付款后拿文件的交付链路，在无真实订单验证时风险大于收益，不采用（升级路径保留）。
- **改了什么**（2026-09-18）：改用 GA4 官方 Measurement Protocol 补录制：用户在 GA4 后台创建 API secret（存本机 `~/.ga/api-secret.txt`，600 权限，不入仓）；新建 `docs/ga4-purchase-log.py`（单笔补录：按 SKU 映射产品名与默认价，`--txn` 订单号生成标准 purchase 事件 POST 至 GA4，支持 `--dry-run` 走 debug 端点校验）。
- **验证**：debug 端点校验通过（validationMessages 为空）；正式端点 204 收妥；脚本 dry-run 自测通过；测试事件 `test_mp_link` 发送成功。

### 新增（成交补录批量工具：对账一条命令自动补录全部新订单）

- **为什么改**：单笔补录需 Vendy 逐单敲命令，订单量起来后是重复劳动；且早鸟期价格变化需人工传 `--value`，易错。
- **改了什么**（2026-09-18）：新建 `docs/ga4-purchase-batch.py`：Playwright 复用 Payloadz 登录态自动抓 Sales History（日期窗口可调）→ 过滤 Team-Playbook 订单 → 状态文件 `~/.ga/backfilled-orders.json` 去重（已录跳过）→ 逐笔 POST purchase，**金额取订单表实际价格**（早鸟 $35 自动正确）。Vendy 交接文件同步更新（`DigiVendAgent/docs/handoff.md` 成交补录段改以批量工具为主）。
- **验证**：宽窗口实测——RAW 抓取 1 行（6 月测试订单）且被产品过滤器正确排除（输出 0 待补录）；流程零异常退出。踩坑沉淀：Sales History 表格为 div 模拟（`selling-summary__table-row`，非 `<table>`）；cell 内 `<strong>` 标签为 display:none，`innerText` 即裸值，不可再做切行处理；Python 三引号内嵌 JS 的 `\n` 需写双反斜杠（运行时转义后才是 JS 合法字面量）。真实订单补录待首单发生后自然验证。

### 新增（T5 交接 Buzz：引流链接与 UTM 约定交付）

- **为什么改**：流水线接力③→④——成交阵地全就绪，Buzz 引流开工前需要正式接收。
- **改了什么**（2026-09-18）：新建 Buzz 仓 `artifacts/handoff.md`（其 .gitignore 已忽略）：资产清单（落地页主推 / EN·ZH 购买直链 / GA4 看板）、UTM 逐项约定、引流纪律（open-core 边界、早鸟码未配置前禁提早鸟价、渠道硬约束、product_id+campaign_id 双归因）、purchase 补录延迟说明；同步记 Buzz 仓 CHANGELOG 一条。

### 新增（T5b 交接 Vendy：阵地运营移交）

- **为什么改**：流水线接力③→⑤——阵地建好后运营期（定价执行 / 履约 / 售后 / 对账）归 Vendy，需正式移交后台入口与工具。
- **改了什么**（2026-09-18）：新建 Vendy 仓 `docs/handoff.md`（其运行时目录，被 gitignore）：阵地资产与后台入口、早鸟双开关机制说明（Payloadz 限时直降价 ≠ 折扣码，两处同步、与 Buzz 首发对齐）、成交补录工具用法与时机、运营 SOP（订单监控 / Send a Download 售后补发 / 三方对账 / 首周后收尾）；同步记 Vendy 仓 CHANGELOG 一条。建设期交接至此全部完成（Buzz + Vendy 双下游就位）。

### 新增（GA4 埋点上线：Measurement ID 回填 + 生产环境事件验证）

- **为什么改**：建设期 T2 尾巴 + T3——落地页上线时 GA4 property 尚未创建（需 Google 登录，本机无登录态），ga4Id 置空上线；漏斗数据的浏览层 / 意向层依赖 GA4 就位后才能采数。
- **改了什么**（2026-09-17）：
  - 用户在专用持久化浏览器 profile（`~/.ga/browser-profile`，以后 GA 相关操作复用）人工登录创建 GA4 property（Account xhqing / Property agent-team-playbook / Web 数据流指向落地页，Measurement ID `G-FRE2DZS751`）。
  - 回填 `site/config.js` 的 `ga4Id` 并同步部署仓 push，Pages 自动重建后线上 config 生效。
- **验证**（生产环境实测）：GA 脚本加载（`gtag/js?id=G-FRE2DZS751`）；page_view 上报（collect 请求 tid 实证）；click_buy_cta 事件在 CTA 点击时产生（dataLayer 实证，携带 cta_label / product_id=Team-Playbook-v3）；CTA→Payloadz 跳转正常（跳转后页面为 Payloadz 自己的 GA 埋点 tid，与本项目无冲突）。outbound click 为 Enhanced Measurement 自动项，仅真实跳转场景触发，未单独拦截验证。
- **验证方法备注**：CTA 点击后 120ms 即跳转，beacon 请求在 Playwright request 监听里与页面卸载竞态不可靠；改用「buyUrl 置为页内锚点使页面存活 + 直接读 dataLayer」验证事件产生，加上 page_view 的 collect 实证发送链路，闭环成立。

### 新增（落地页部署上线：GitHub Pages 独立仓库 agent-team-playbook）

- **为什么改**：建设期主线 T2——购买链接就位后（T1 完成），落地页必须上线才能成为 CTA 的承接阵地与漏斗数据层，下游 Buzz 引流才有链接可发。
- **改了什么**（2026-09-17）：
  - 选型：GitHub Pages（gh 已登录、零新依赖；wrangler 未装故 Cloudflare Pages 弃选）；独立部署仓 `xhqing/agent-team-playbook`（公开）而非挂在 SiteBuilderAgent 下——销售 URL `https://xhqing.github.io/agent-team-playbook/` 带品牌词、不暴露 agent 仓库名，后续可绑自定义域名。
  - 部署内容：`site/` 六文件（index / style / analytics / config / config.example / README）组装至本机 `tmp/deploy/` 后推 main，Pages 从 main 根目录部署。部署仓含真实 `config.js`：其值（buyUrl、GA4 ID、newsletterUrl）全部为设计上浏览器端公开可见的运行时配置，不构成敏感信息泄露；主仓 `.gitignore` 规则不变。
  - 预防性修正：`config.js` 的 `ga4Id` 占位符置空——analytics.js 对 ga4Id 只判真值不验格式，占位符会被当真 ID 注入错误脚本源；待拿到真实 Measurement ID 后回填再 push。
- **验证**（生产环境 headless 实测）：HTTPS 200、build status built；标题正确；buyUrl 加载；三个 CTA（nav / hero / pricing）全部激活；点击 hero CTA 实际跳转 Payloadz 购买页（store.payloadz.com/details/2722311-…）；无 JS 错误。
- **待办衔接**：GA4 property 创建需用户登录 Google（本机无登录态），不阻塞销售链路；T2 剩余部分、T3 GA4 验证、T5 向 Buzz 交接的素材均已就绪。

### 新增（Payloadz 上架完成：双语言版本产品 + 交付文件 + 购买链接就绪）

- **为什么改**：建设期主线 T1——把 Wright 交接的成品数字产品（The Agent Team Playbook，分中英两版独立包）真正变成可成交阵地：产品上架、交付文件上传、购买链接就绪，下游 Buzz 才有链接可发。
- **改了什么**（2026-09-17）：
  - 打包交付实物：两版分语言 zip（英文版 / 中文版各 12 文件，与《产品说明》文件清单一一对应，`unzip -t` 完整性校验通过），存 Wright 侧被忽略的 artifacts 目录。
  - 调研结论：Payloadz 官方 seller API 已退役（帮助中心 2026-09 确认：产品创建、文件上传等 legacy 方法全部不可用，仅剩需人工审批的 TransactionCreation），程序化上架只能走网页后台自动化。
  - 网页自动化上架（Playwright + payloadz-login skill 的持久化登录态，脚本在本机 `tmp/`）：英文版产品 `TEAMPLAYBOOK-EN-001`（购买链接 `https://store.payloadz.com/go?id=2722311`）、中文版产品 `TEAMPLAYBOOK-ZH-001`（`https://store.payloadz.com/go?id=2722313`），均 eBooks → Computers 分类、定价 $49（按建议价，最终定价权在 Vendy），描述与致谢文案按《产品说明》要点撰写。
  - 交付文件上传并关联：两版 zip 分别经后台文件页上传至 Payloadz 服务器，ProductDetail 的 File Location 均指向对应 zip（上传即自动关联，无需手动勾选）。
  - 本机 `site/config.js`（被 .gitignore 忽略）的 `buyUrl` 填入英文版购买链接——落地页主 CTA 激活条件就位。
- **关键经验（供后续维护 / 上新复用）**：① ProductSetup 页的 `FileUpload_1..6` 是商品图片位（仅 JPG/PNG/GIF），交付文件走 ProductFile 页（保存产品后自动跳转）；② 分类虽标 Optional 但客户端验证器强制必选（选完主分类会触发整页 postback，之后不能重新 goto 否则选择丢失）；③ 描述编辑器为 Quill，需先 `scroll_into_view_if_needed` 再 click 聚焦后物理输入，自动同步至隐藏 textarea；④ Payloadz 存储层不支持非 ASCII 字符（中文存成 `?`），中文版产品名 / 描述改纯英文（中文信息由落地页承载）；⑤ ASP.NET WebForms 提交后 URL 不变，成败判定看表单重置或页面跳转，勿用 URL 变化作唯一判据。
- **验证**：未登录 curl 实测两个 store 购买页（标题、$49 价格、Checkout、PayPal 字样均在位）；ProductDetail 实测两产品 File Location 指向对应 zip；产品列表双 SKU 在列。上架脚本与探测脚本存本机 `tmp/`（git 忽略）。

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
