---
name: "payloadz-login"
description: 用 Playwright 脚本从本地凭证文件读取 Payloadz 账号密码并自动登录，密码全程不进入对话上下文（脚本进程直读直填）。当用户说「登录 Payloadz」「打开 Payloadz 后台」「进 Payloadz 卖家账户」「payloadz login / sign in」「需要一个已登录的 Payloadz 浏览器会话」或任何需要进入 Payloadz 账户的场景时必须使用本 skill。登录态通过持久化浏览器配置保存，二次调用可直接复用会话。NOT for：其他平台的登录（各平台有自己的流程）；登录之后在 Payloadz 上的具体业务操作（上传产品、配置支付等，那些建立在登录会话之上，但不是本 skill 的职责）。
---

# Payloadz Login

## 这个 skill 解决什么问题

把「登录 Payloadz」做成一条命令：脚本自己从本地凭证文件读取账号密码、启动浏览器、填表、提交。**密码只在本机文件 → 脚本进程 → 浏览器之间流动，绝不经由对话上下文**（不要用 read 工具去读凭证文件，这是本 skill 存在的核心原因）。

## 凭证文件

默认路径：`~/.payloadz/credentials.json`（权限应为 600）

```json
{
  "username": "登录邮箱",
  "password": "密码"
}
```

- 首次使用先创建该文件并让用户填写（字段留空时脚本会报错并提示）
- `--creds <path>` 可指定其他凭证文件路径
- 该文件在用户主目录下，不会被任何 git 仓库跟踪

## 用法

```bash
python3 <skill-dir>/scripts/login.py [--creds ~/.payloadz/credentials.json] [--hold] [--headless]
```

脚本位置：本 skill 目录下 `scripts/login.py`。

依赖：Python 包 `playwright`（`pip3 install playwright`）、系统 Google Chrome（脚本用 `channel='chrome'` 启动，无需额外下载浏览器）。

## 脚本行为

1. 读凭证文件（缺失或字段为空 → 退出码 3，报错提示填写）
2. 启动持久化浏览器（数据目录 `~/.payloadz/browser-profile/`，**登录 cookie 保存在这里**）
3. 先探测是否已是登录态（已登录则访问登录页会被直接跳走）→ 是则输出「已登录」（退出码 2）
4. 未登录则打开 `https://www.payloadz.com/login.aspx`，填 `#loginUsername` / `#loginPassword`，勾选记住我，点击 "Login To Your Account"
5. 等待跳转：URL 离开 `login.aspx` 即登录成功（退出码 0）；默认完成即退出浏览器，**登录态已存进 profile，后续任务用同一 profile 再开浏览器即是已登录状态**
6. 超时未跳转 → 大概率是 reCAPTCHA 人机验证拦截，自动转入保持模式：浏览器保持打开，等人工在窗口里完成验证（脚本检测到跳转后按成功退出）；Ctrl+C 关闭则退出码 4

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 登录成功（含 CAPTCHA 场景下人工接管后成功） |
| 2 | 本来就已登录（会话复用） |
| 3 | 凭证缺失 / 未填写 |
| 4 | 疑似 CAPTCHA 或登录被拒，且人工未完成接管 |

## 参数

- `--hold`：登录后保持浏览器打开，直到 Ctrl+C（适合用户想亲自接管窗口时用；默认完成即退，登录态已存 profile）
- `--headless`：无头模式运行（默认有头；遇到 CAPTCHA 时有头模式才能人工接管，一般别用这个）
- `--creds <path>`：自定义凭证文件路径

## 安全纪律

- **绝不用 read / cat 把凭证文件内容带进对话上下文**——检查凭证一律靠脚本的退出码和状态输出（输出中不含密码）
- 凭证文件、浏览器数据目录都在 `~/.payloadz/` 下，属本机私有数据，不得复制进任何 git 仓库或 skill 正文
- 截图、日志输出不得包含密码框内容

## 维护备注

- 登录页字段（`#loginUsername` / `#loginPassword` / "Login To Your Account" 按钮）为 2026-09 实测值；Payloadz 改版导致选择器失效时，用浏览器探测页面结构后更新脚本里的常量区即可（脚本顶部集中定义了选择器，方便改）。
