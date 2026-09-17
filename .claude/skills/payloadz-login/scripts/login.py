#!/usr/bin/env python3
"""Payloadz auto-login via Playwright.

Reads credentials from a local JSON file and fills the Payloadz login form.
The password stays inside this process — it is never printed, logged, or
returned to the caller. Check outcomes via exit codes and status lines only.

Exit codes:
  0  login successful
  2  already logged in (session reused from persistent profile)
  3  credentials missing / not filled in
  4  likely CAPTCHA or rejected login — browser kept open for manual takeover
"""

import argparse
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

# --- Page constants (measured 2026-09; update here if Payloadz redesigns) ---
LOGIN_URL = "https://www.payloadz.com/login.aspx"
SEL_USER = "#loginUsername"
SEL_PASS = "#loginPassword"
SEL_REMEMBER = "#remember"
SEL_SUBMIT_TEXT = "Login To Your Account"
NAV_TIMEOUT_MS = 45_000  # generous: invisible reCAPTCHA scoring takes time

CREDS_DEFAULT = Path.home() / ".payloadz" / "credentials.json"
PROFILE_DIR = Path.home() / ".payloadz" / "browser-profile"

ERROR_KEYWORDS = ("error", "invalid", "wrong", "incorrect", "failed", "locked")


def die(code: int, msg: str) -> None:
    print(f"[payloadz-login] {msg}", file=sys.stderr)
    sys.exit(code)


def load_creds(path: Path):
    """Return (username, password). Password never leaves this function's caller."""
    if not path.exists():
        die(3, f"credentials file not found: {path} — create it with "
               '{"username": "...", "password": "..."} (chmod 600)')
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        die(3, f"credentials file is not valid JSON: {path} ({e})")
    user = (data.get("username") or "").strip()
    pwd = data.get("password") or ""
    if not user or not pwd:
        die(3, f"username/password not filled in: {path}")
    return user, pwd


def page_error_hint(page) -> str:
    """Best-effort: surface a visible error line from the page (no secrets)."""
    try:
        text = page.locator("body").inner_text(timeout=3000)
        for line in text.splitlines():
            low = line.strip().lower()
            if low and any(k in low for k in ERROR_KEYWORDS):
                return line.strip()[:120]
    except Exception:
        pass
    return ""


def hold_open(page, reason: str) -> bool:
    """Keep the browser open until Ctrl+C; watch for a successful redirect.
    Returns True if a redirect off the login page was detected, False on Ctrl+C."""
    print(f"[payloadz-login] {reason}")
    print("[payloadz-login] browser stays open — finish manually if needed, "
          "then press Ctrl+C here to close.")
    try:
        while True:
            time.sleep(2)
            url = page.url or ""
            if "login.aspx" not in url:
                print(f"[payloadz-login] success detected: {url}")
                return True
    except KeyboardInterrupt:
        print("\n[payloadz-login] closed by user.")
        return False


def main() -> None:
    ap = argparse.ArgumentParser(description="Payloadz auto-login (credentials stay local)")
    ap.add_argument("--creds", type=Path, default=CREDS_DEFAULT,
                    help=f"credentials JSON path (default: {CREDS_DEFAULT})")
    ap.add_argument("--headless", action="store_true",
                    help="run headless (CAPTCHA cannot be solved manually — avoid)")
    ap.add_argument("--hold", action="store_true",
                    help="keep browser open after login until Ctrl+C")
    args = ap.parse_args()

    user, pwd = load_creds(args.creds)  # secret stays in-process from here on
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE_DIR),
            channel="chrome",  # system Google Chrome
            headless=args.headless,
            viewport={"width": 1280, "height": 800},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # 1) Probe existing session: an authenticated visit redirects away.
        page.goto(LOGIN_URL, timeout=NAV_TIMEOUT_MS, wait_until="domcontentloaded")
        try:
            page.wait_for_load_state("networkidle", timeout=15_000)
        except Exception:
            pass
        if "login.aspx" not in (page.url or ""):
            print(f"[payloadz-login] already logged in (session reused): {page.url}")
            if args.hold:
                hold_open(page, "session active.")
            ctx.close()
            sys.exit(2)

        # 2) Fill the form.
        try:
            page.wait_for_selector(SEL_PASS, timeout=20_000)
        except Exception:
            ctx.close()
            die(4, "login form not found on page — Payloadz may have redesigned; "
                   "inspect the page and update the constants at the top of this script.")
        page.fill(SEL_USER, user)
        page.fill(SEL_PASS, pwd)
        try:
            cb = page.locator(SEL_REMEMBER)
            if cb.count() and not cb.is_checked():
                cb.check()
        except Exception:
            pass  # remember-me is optional
        print(f"[payloadz-login] form filled for {user[:3]}*** — submitting…")

        # 3) Submit and wait for redirect off the login page.
        page.get_by_role("button", name=SEL_SUBMIT_TEXT).click()
        start = time.time()
        try:
            while time.time() - start < NAV_TIMEOUT_MS / 1000:
                if "login.aspx" not in (page.url or ""):
                    break
                time.sleep(1)
            else:
                hint = page_error_hint(page)
                if not args.headless:
                    ok = hold_open(page, f"no redirect after submit "
                                         f"({'page error: ' + hint if hint else 'likely CAPTCHA'}) — "
                                         "solve it in the browser window if shown.")
                    ctx.close()
                    sys.exit(0 if ok else 4)
                ctx.close()
                die(4, f"no redirect after submit "
                       f"({'page error: ' + hint if hint else 'likely CAPTCHA'}); "
                       "rerun without --headless to take over manually.")
        except KeyboardInterrupt:
            ctx.close()
            die(4, "interrupted before login completed.")

        print(f"[payloadz-login] login OK: {page.url}")
        if args.hold:
            hold_open(page, "logged in.")
        ctx.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
