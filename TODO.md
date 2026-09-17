# TODO — SiteBuilderAgent (Mason)

> 记录未完成待办，按紧急度分节。做完移入 `TODO-archive.md`。
> 个人隐私类待办分流至 `TODO.local.md`（不入公开仓库）。

## 🟠 橙色（主线任务：阻塞下游 Buzz 引流）

- [ ] **T1** Payloadz 上架 + PayPal 收款链路配置：上传交付实物 zip、按建议定价配置、拿到购买 GoLink 填入 `site/config.js` 的 `buyUrl`。（记录：2026-09-17 11:05）
- [ ] **T2** 部署落地页：选定托管（GitHub Pages 或 Cloudflare Pages，免费档够用），创建 GA4 property 拿 Measurement ID 填入 `site/config.js`。（记录：2026-09-17 11:05）

## 🟡 黄色（部署后验证）

- [ ] **T3** 部署后端到端验证：线上页面 CTA 按钮激活、GA4 DebugView 收到 page_view、点击 CTA 收到 outbound click 与 click_buy_cta 事件。（记录：2026-09-17 11:05）

## 🟢 绿色（计划类，不阻塞）

- [ ] **T4** Payloadz「Download Page Text」字段贴 GA 转化码，补齐漏斗成交层（purchase 事件）。（记录：2026-09-17 11:05）
- [ ] **T5** 购买链接就绪后交 Buzz（GrowthMarketerAgent）：GoLink + 落地页 URL + UTM 约定（utm_content 区分引流内容）。（记录：2026-09-17 11:05）
- [ ] **T6** 若 Buzz 启动 Meta 广告：创建 Pixel 填入 `site/config.js` 的 `pixelId`；首周早鸟开关交 Vendy 决定（`earlyBird` 配置）。（记录：2026-09-17 11:05）
