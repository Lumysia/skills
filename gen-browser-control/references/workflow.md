# Browser Control Workflow

## Scope

Control an existing Chrome, Edge, or Chromium-family browser through Playwright MCP extension mode. This workflow reuses the user's real browser tabs, cookies, logged-in sessions, and installed extensions.

Use extension mode when the task benefits from:

- Existing SSO, 2FA, cookies, or authenticated sessions.
- Browser extensions that affect the page.
- A page the user already has open.
- Manual handoff between user actions and agent automation.

Do not use extension mode for clean-room testing, isolated authentication, or reproducible browser state unless the user explicitly wants the real profile involved.

## Setup

1. Infer the user's intent to connect to an existing browser profile from the task; ask only if using the real profile is ambiguous or risky.
2. Infer the browser from the user's wording, active MCP tab list, existing MCP command flags, or the opened page. Ask only if it cannot be inferred or if host configuration must be changed.
3. Confirm the browser is Chrome, Edge, or Chromium-family; extension mode does not support Firefox or WebKit.
4. Ask the user to install or enable the Playwright MCP Bridge extension from the browser extension store when it is missing.
5. If the agent host already has a working Playwright MCP extension-mode entry, reuse it and do not duplicate or replace it.
6. If no working entry exists, add or verify an equivalent MCP server entry in the target agent host, adapting the object shape to that host:

```json
{
  "mcpServers": {
    "playwright-extension": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--extension"]
    }
  }
}
```

For Chromium-family browsers that are not found by default, add the executable and profile paths instead of assuming Chrome's profile directory. Example for Brave on macOS:

```json
{
  "mcpServers": {
    "playwright-extension": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--extension",
        "--executable-path",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "--user-data-dir",
        "/Users/example/Library/Application Support/BraveSoftware/Brave-Browser"
      ]
    }
  }
}
```

7. Reload or restart the agent host only when MCP configuration changed.
8. Ask the user to open the target page in the intended browser profile only when no suitable tab is already available.
9. On first interaction, have the user approve the extension connection and select the browser tab to control.
10. Run a read-only smoke test: list or select the tab, take an accessibility snapshot, and confirm the current URL or page title.

## Optional Token

The extension may show a `PLAYWRIGHT_MCP_EXTENSION_TOKEN` value on its status page. Use it only when the user explicitly wants to skip repeated connection approvals for this browser profile.

Configuration shape:

```json
{
  "mcpServers": {
    "playwright-extension": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--extension"],
      "env": {
        "PLAYWRIGHT_MCP_EXTENSION_TOKEN": "token-from-extension-ui"
      }
    }
  }
}
```

Treat the token as profile-local sensitive configuration. Do not paste it into chat transcripts, source files, shared repositories, or logs.

## Operating Loop

1. Start by identifying the selected tab, current URL, and user goal.
2. Prefer accessibility snapshots for page understanding; use screenshots only when visual layout or rendering must be checked.
3. Before each meaningful action, verify the target element by role, accessible name, and nearby text.
4. For navigation, form filling, clicking, keyboard input, tab switching, and dialogs, use Playwright MCP tools instead of shell scripts or ad hoc browser automation.
5. After actions, verify the result from page state, URL, visible text, network or console evidence when available, or a screenshot when visual proof matters.
6. If the page changes unexpectedly, take a fresh snapshot before continuing.
7. Summarize completed actions and remaining user-owned steps at the end.

## Safety

- Stop before submitting payment, purchases, orders, account deletion, public posts, production changes, permission grants, bulk messages, or irreversible operations.
- Stop before entering, revealing, copying, downloading, or exporting passwords, recovery codes, API keys, private keys, tokens, or personal documents.
- Ask the user to complete MFA, CAPTCHA, biometric prompts, password-manager prompts, and security challenges manually.
- Do not scrape or export more data than the task requires.
- Do not change browser settings, extension settings, saved passwords, cookies, or profile data unless the user explicitly asks.
- Treat visible authenticated pages as sensitive; report only task-relevant details.

## Troubleshooting

- If no browser connects, verify the extension is installed in the same browser profile the user opened.
- If the server looks in Chrome while the user uses another Chromium-family browser, configure `--executable-path` and `--user-data-dir` for that browser profile.
- If tab selection does not appear, reload the agent host and open the extension status page.
- If approvals repeat too often, offer the optional token flow without pressuring the user to use it.
- If the target site blocks automation, switch to user-guided steps rather than trying to bypass protections.
- If the task needs reproducibility or a fresh login state, use normal Playwright MCP profile modes instead of extension mode.
