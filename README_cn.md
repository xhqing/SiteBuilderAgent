<div align="center">

<img src="assets/logo.svg" width="640" alt="Mason logo" />

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-0.1.0-blue)
![AI Agent](https://img.shields.io/badge/Type-AI%20Agent-FF1493)

</div>

# SiteBuilderAgent

> **拟人化名字：Mason** —— 团队里的建站 / 成交基础设施智能体。
>
> 「Site（站点）+ Builder（建设）+ Agent（智能体）」—— Mason 是六智能体流水线的第 ③ 步：拿到成品数字产品，把它落成一个能收钱的成交阵地——独立站、落地页、支付链路。建好后把可成交的购买链接交给 **Buzz**（引流）去发，让链接有处可指。（研判 = Scout，生产 = Wright，引流 = Buzz，成交 = Vendy，复盘 = Echo。）

Mason 负责**成交闭环里的「基础设施」**。他不生产产品、不引流、不接单履约——他只把站点建起来、把支付接通，直到购买链接能真正收到钱。建好阵地，交钥匙。

[English](README.md)

---

## 🎯 定位

| 维度 | 说明 |
|------|------|
| **做什么** | 搭建成交基础设施——独立站、落地页、支付接入（团队第 ③ 步：建设期）|
| **不做什么** | 不生产产品（Wright）；不引流（Buzz）；不接单 / 履约 / 售后 / 对账（Vendy 运营期）|
| **技术栈** | 静态站 / 建站工具（Astro · Hugo · Next.js · Carrd · Webflow · Shopify）+ 支付（Stripe · PayPal · 支付宝 · Lemon Squeezy · Paddle），按产品形态选型 |
| **交接** | 购买链接 → Buzz；可运行的站点 → Vendy（运营期）|
| **运行模式** | 建到「可成交」，然后交钥匙 |

---

## 🧠 核心能力

### 建站引擎 · `/site-builder`（建站循环）

Mason 的「手脚」。读取 **Wright** 的成品和 **Scout** 的机会研判后，跑**建站循环**：选平台 → 搭站点骨架 → 做落地页 → 接支付 → 验收下单链路 → 把购买链接交给 **Buzz**。生产成品是 Wright（[ProductProducerAgent](https://github.com/xhqing/ProductProducerAgent)）的活，引流是 Buzz（[GrowthMarketerAgent](https://github.com/xhqing/GrowthMarketerAgent)）的活，接单运营是 Vendy（[DigiVendAgent](https://github.com/xhqing/DigiVendAgent)）的活。**Mason 只建站点、接支付，然后交钥匙。**

- 触发：`/site-builder`、`建站`、`搭独立站`、`做落地页`、`接支付`
- 建站：静态生成器 / 建站工具 + 部署（Netlify · Vercel · Cloudflare Pages · GitHub Pages）
- 支付：Stripe / PayPal / 支付宝 / 微信支付 / Lemon Squeezy / Paddle——至少打通一条并端到端实测
- 3 种必须停下来问用户的特殊情况：要花钱（域名 / 托管 / SSL）、要注册账号、要输入密钥 / 凭证

---

## 🔁 典型工作流

Mason 是六智能体团队的第 **③** 步：

```
① Scout（研判）→ ② Wright（生产）→ ③ Mason（建阵地）→ ④ Buzz（引流）→ ⑤ Vendy（成交运营）→ ⑥ Echo（复盘）
```

跑建站循环：

```
/site-builder  →  选平台 → 搭骨架 → 做落地页 → 接支付 → 验收下单 → 把购买链接交给 Buzz
```

> **为什么 Mason 在 Buzz 之前**：Buzz 的带货链接必须指向一个已经能收钱的页面，所以阵地必须先建好。Mason = 建设期；Vendy = 运营期（在 Mason 建好的站点上做生意）。

---

## 📦 本仓库包含什么

本开源仓库发布的是 **Agent 的设计与技能**，不含运行时数据。

```
SiteBuilderAgent/
├── README.md                 ← 英文 README
├── README_cn.md              ← 本文件（中文）
├── LICENSE.md                ← MIT
├── CLAUDE.md                 ← 项目级 Agent 指令
├── .claude/
│   └── skills/
│       └── site-builder/     ← 建站引擎 Skill（建站循环）
└── .pi/
    └── skills → ../.claude/skills   ← 软链接：pi harness 与 Claude Code 共用同一份 Skill
```

> 运行时数据（站点源码快照、部署记录、含凭证的 `config.json`）位于 `docs/` 目录，**已 gitignore，不随仓库分发**，每个用户本地自备。

---

## ⚙️ 配置（运行时，仅本地）

所有运行时数据集中在 `docs/` 目录。核心配置文件：`docs/config.json`。

> ⚠️ `docs/config.json` 含明文支付密钥 / API Token，已在 `.gitignore` 中排除，**不会提交到仓库**。下面只列结构（值为占位）：

```json
{
  "site":     { "platform": "", "framework": "", "domain": "", "hosting": "" },
  "payment":  { "providers": [], "default_currency": "HKD", "webhook_url": "" },
  "handoff":  { "product_dir": "docs/product", "buy_links": [] },
  "budget":   { "amount": 100, "currency": "HKD", "require_roi_before_spend": true },
  "llm_api_keys": {}
}
```

- `site`：站点选型（平台 / 框架 / 域名 / 托管）
- `payment`：支付链路（渠道、默认货币、回调地址）
- `handoff`：入站产品目录 + 出站购买链接（交 Buzz）
- `budget`：可用预算（花钱前要求预估 ROI）
- `llm_api_keys`：大模型 API Key

---

## 🚀 快速开始

1. 本地创建 `docs/config.json`，填好建站平台、支付渠道、预算（不提交）。
2. 从 **Wright** —— [ProductProducerAgent](https://github.com/xhqing/ProductProducerAgent) —— 拿到一个成品数字产品，或自行准备好产品。
3. 让 Mason 开始建站循环：
   ```
   /site-builder
   ```
4. 期间 Mason 只在三种情况下停下来找你：要花钱、要注册账号、要输密钥。其余时间自主推进到「可成交」，然后把购买链接交给 Buzz。

---

## 🛡️ 安全与边界

- 只建合法合规的站点，不搬运受版权 / 商标保护的素材。
- 支付密钥 / 凭证**只存本地** `config.json`，绝不写回 SKILL 或日志。
- 未经用户明确同意，不花一分钱；花钱必附 ROI 预估。
- 不蹭涉政、灾害、悲剧、严重争议类流量。
- 收益描述一律给区间并标注不确定性，不写「保证收益」。

---

## 📝 设计原则

- **只建不营**：建到「可成交」即交钥匙，运营归 Vendy，不越界。
- **最小可成交优先**：先用最快路径打通一条「页面 + 支付 + 下单」链路，再迭代增强；不为完美拖延交钥匙。
- **可移植 / 可复用**：站点模板、支付接入脚本沉淀进 `docs/`，供后续产品复用。
- **零凭证泄露**：敏感信息只存本地 `config.json`，公开仓库零泄露。
- **能用现成 Skill 就不重造**：遇难题优先找现成 Skill，不自己重造。

---

## 📄 协议

版权所有 (c) 2026 All Contributors。MIT，详见 [LICENSE.md](LICENSE.md)。

## 🏷️ 署名

使用、二次开发本项目时，请署名 **SiteBuilderAgent (Mason)** 并引用项目地址：`https://github.com/xhqing/SiteBuilderAgent`。

*Mason 负责建好阵地；Vendy 在阵地上做生意。*
