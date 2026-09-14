<div align="center">

<img src="assets/logo.svg" width="640" alt="Mason logo" />

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-0.1.0-blue)
![AI Agent](https://img.shields.io/badge/Type-AI%20Agent-FF1493)

</div>

# SiteBuilderAgent

> **Codename: Mason** — the site-builder / conversion-infrastructure agent of the team.
>
> "Site + Builder + Agent" — Mason is step ③ of a six-agent pipeline. He takes a finished digital product and builds the place where it gets sold: an independent website, landing pages, and payment integration. He then hands ready-to-sell buy links to **Buzz** (traffic), so the links have somewhere to point. (Research = Scout, production = Wright, traffic = Buzz, sales = Vendy, analysis = Echo.)

Mason owns the **infrastructure side of conversion**. He doesn't produce the product, drive traffic, or run order ops — he builds the storefront and wires up payment until a buy link can actually take money. Build the site, then hand off the keys.

[简体中文](README_cn.md)

---

## 🎯 Positioning

| Dimension | Detail |
|-----------|--------|
| **What** | Build the conversion infrastructure — independent site, landing pages, payment integration (team step ③, build phase) |
| **What not** | No product production (Wright); no traffic driving (Buzz); no order fulfillment / after-sales / bookkeeping (Vendy ops phase) |
| **Stack** | Static / site builders (Astro · Hugo · Next.js · Carrd · Webflow · Shopify) + payment (Stripe · PayPal · Alipay · Lemon Squeezy · Paddle) — chosen per product |
| **Handoff** | Buy links → Buzz; running site → Vendy (ops phase) |
| **Mode** | Build to "ready to sell", then hand off the keys |

---

## 🧠 Core Capabilities

### Site Builder Engine · `/site-builder` (the build loop)

Mason's "hands". Reads the product from **Wright** and the opportunity from **Scout**, then runs the **build loop**: pick platform → scaffold site → landing page → wire payment → verify checkout → hand buy links to **Buzz**. Producing the product is Wright's job ([ProductProducerAgent](https://github.com/xhqing/ProductProducerAgent)); driving traffic is Buzz's ([GrowthMarketerAgent](https://github.com/xhqing/GrowthMarketerAgent)); running orders is Vendy's ([DigiVendAgent](https://github.com/xhqing/DigiVendAgent)). **Mason only builds the storefront and wires up payment, then hands off.**

- Trigger: `/site-builder`, `建站`, `搭独立站`, `做落地页`, `接支付`
- Site: static generators / site builders + deploy (Netlify · Vercel · Cloudflare Pages · GitHub Pages)
- Payment: Stripe / PayPal / Alipay / WeChat Pay / Lemon Squeezy / Paddle — at least one wired & tested end-to-end
- Three cases that require stopping to ask: spending money (domain / hosting / SSL), account registration, key / credential input

---

## 🔁 Typical Workflow

Mason is step **③** of a six-agent team:

```
① Scout (research) → ② Wright (produce) → ③ Mason (build site) → ④ Buzz (traffic) → ⑤ Vendy (sell / ops) → ⑥ Echo (analyze)
```

Run the build loop:

```
/site-builder  →  pick platform → scaffold → landing page → wire payment → verify checkout → hand buy links to Buzz
```

> **Why Mason sits before Buzz**: Buzz's buy links must point to a page that can already take money. So the storefront has to be built first. Mason = build phase; Vendy = ops phase (takes orders on the site Mason built).

---

## 📦 What's in This Repo

This open-source repo ships **the agent's design and skills** — not runtime data.

```
SiteBuilderAgent/
├── README.md                 ← this file (English)
├── README_cn.md              ← Chinese README
├── LICENSE.md                ← MIT
├── CLAUDE.md                 ← project-level agent instructions
├── .claude/
│   └── skills/
│       └── site-builder/     ← Site Builder Engine skill (build loop)
└── .pi/
    └── skills → ../.claude/skills   ← symlink: the pi harness shares the same skills
```

> Runtime data (site source snapshots, deploy records, `config.json` with credentials) lives in `docs/`, which is **gitignored and not distributed**. Each user keeps their own locally.

---

## ⚙️ Configuration (runtime, local only)

Runtime data is centralized under `docs/`. Core config: `docs/config.json`.

> ⚠️ `docs/config.json` contains plaintext payment keys / API tokens. It is excluded by `.gitignore` and **never committed**. Structure only (values placeholder):

```json
{
  "site":     { "platform": "", "framework": "", "domain": "", "hosting": "" },
  "payment":  { "providers": [], "default_currency": "HKD", "webhook_url": "" },
  "handoff":  { "product_dir": "docs/product", "buy_links": [] },
  "budget":   { "amount": 100, "currency": "HKD", "require_roi_before_spend": true },
  "llm_api_keys": {}
}
```

- `site`: site selection (platform / framework / domain / hosting)
- `payment`: payment rail (providers, default currency, webhook)
- `handoff`: inbound product dir + outbound buy links handed to Buzz
- `budget`: spend budget (require ROI estimate before spending)
- `llm_api_keys`: LLM API keys

---

## 🚀 Quick Start

1. Create `docs/config.json` locally with your site platform, payment providers, and budget (never committed).
2. Get a finished product from **Wright** — [ProductProducerAgent](https://github.com/xhqing/ProductProducerAgent) — or supply your own.
3. Start the build loop:
   ```
   /site-builder
   ```
4. Mason only stops for three reasons: spending money, account registration, or key input. Otherwise he builds autonomously to "ready to sell" and hands buy links to Buzz.

---

## 🛡️ Safety & Boundaries

- Only build lawful, compliant storefronts; no copyrighted / trademarked material.
- Payment keys / credentials live **only** in local `config.json`; never written back to skills or logs.
- Never spends money without explicit user consent; every spend carries an ROI estimate.
- No traffic from politics, disasters, tragedies, or heavy controversy.
- Earnings claims are always ranges with uncertainty noted; never "guaranteed X".

---

## 📝 Design Principles

- **Build, don't operate**: build to "ready to sell" and hand off the keys; running the business is Vendy's job.
- **Minimum viable checkout first**: ship one working page + payment + order path, then iterate; don't delay handoff for perfection.
- **Portable & reusable**: site templates and payment scripts are banked in `docs/` for reuse.
- **Zero credential leakage**: sensitive info stays in local `config.json`; the public repo leaks nothing.
- **Reuse skills, don't reinvent**: reach for an existing skill before building your own.

---

## 📄 License

Copyright (c) 2026 All Contributors. MIT — see [LICENSE.md](LICENSE.md).

## 🏷️ Attribution

If you use, fork, or build on this project, please credit **SiteBuilderAgent (Mason)** and link back to the project repository: `https://github.com/xhqing/SiteBuilderAgent`.

*Mason builds the storefront; Vendy runs the business on it.*
