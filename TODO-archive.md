# TODO Archive — SiteBuilderAgent (Mason)

> 已处理待办归档。条目格式与 TODO.md 一致，编号永不复用。

## 🟠 橙色（主线任务：阻塞下游 Buzz 引流）

- [ ] **T1** Payloadz 上架 + PayPal 收款链路配置：上传交付实物 zip、按建议定价配置、拿到购买 GoLink 填入 `site/config.js` 的 `buyUrl`。（记录：2026-09-17 11:05）
  ✅**已完成**（完成：2026-09-17 18:43）——两版产品上架成功（英文版 TEAMPLAYBOOK-EN-001 / store.payloadz.com/go?id=2722311；中文版 TEAMPLAYBOOK-ZH-001 / go?id=2722313，均 $49，交付 zip 已上传关联，结账页 PayPal 在位）；buyUrl 已填入本机 `site/config.js`。细节见 CHANGELOG 当日条目。

- [ ] **T2** 部署落地页：选定托管（GitHub Pages 或 Cloudflare Pages，免费档够用），创建 GA4 property 拿 Measurement ID 填入 `site/config.js`。（记录：2026-09-17 11:05；2026-09-17 21:35 更新：部署部分已完成——GitHub Pages 上线 + 端到端验证通过，仅剩 GA4 ID）
  ✅**已完成**（完成：2026-09-17 22:40）——GitHub Pages 独立仓 agent-team-playbook 上线；GA4 property 创建（Measurement ID G-FRE2DZS751，用户人工登录创建、专用浏览器 profile `~/.ga/` 复用），回填 config.js 并已部署。

- [ ] **T3** 部署后端到端验证：线上页面 CTA 按钮激活、GA4 DebugView 收到 page_view、点击 CTA 收到 outbound click 与 click_buy_cta 事件。（记录：2026-09-17 11:05）
  ✅**已完成**（完成：2026-09-17 22:40）——生产环境实测：CTA 激活与 CTA→Payloadz 跳转通过；GA4 脚本加载（gtag/js?id=G-FRE2DZS751）与 page_view 上报（collect 请求 tid 实证）通过；click_buy_cta 事件 dataLayer 实证（含 cta_label / product_id 参数）。outbound click 为 Enhanced Measurement 自动项、仅在真实跳转场景触发，未单独拦截验证。

## 🟢 绿色（计划类）

- [ ] **T4** Payloadz「Download Page Text」字段贴 GA 转化码，补齐漏斗成交层（purchase 事件）。（记录：2026-09-17 11:05；2026-09-17 22:40 更新：GA4 已就位，可直接做）
  ✅**已更新**（2026-09-18 10:55）——原方案实测不可行（字段纯文本、HTML 整体转义，误存内容已清理），改用 GA4 Measurement Protocol 补录制完成成交层（工具 `docs/ga4-purchase-log.py`，Vendy 对账逐单补录）；同日新起 T7 保留 Remote Download Page 升级路径。

- [ ] **T5** 购买链接就绪后交 Buzz（GrowthMarketerAgent）：GoLink + 落地页 URL + UTM 约定（utm_content 区分引流内容）。（记录：2026-09-17 11:05；2026-09-17 21:35 更新：购买链接与落地页 URL 均已就绪，随时可交接）
  ✅**已完成**（完成：2026-09-18 10:55）——交接文件写入 Buzz 仓 `artifacts/handoff.md`（资产清单 + UTM 约定 + 引流纪律含早鸟码禁提约束 + 数据自查路径），Buzz 仓 CHANGELOG 已记。
