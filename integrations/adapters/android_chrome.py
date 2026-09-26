"""Android Chrome CDP worker adapter.

This is the Nexus-side connection to a Chrome/Chromium-compatible CDP
endpoint. It does not install software or discover credentials.

For an Android handset, the CDP endpoint must be exposed by an authorized
bridge/debugging setup. Nexus cannot directly control the installed Chrome UI
without such an endpoint.

Environment:
    NEXUS_ANDROID_CHROME_CDP_URL=http://127.0.0.1:9222
"""

from __future__ import annotations

import os
from typing import Any


class AndroidChromeWorker:
    name = "android-chrome-cdp"

    def __init__(self, endpoint_url: str | None = None):
        self.endpoint_url = (
            endpoint_url or os.getenv("NEXUS_ANDROID_CHROME_CDP_URL", "")
        ).rstrip("/")

    def status(self) -> dict[str, Any]:
        configured = bool(self.endpoint_url)
        return {
            "name": self.name,
            "configured": configured,
            "endpoint_url": self.endpoint_url if configured else None,
            "execution_owner": "Gungv-Nexus-worker",
            "requires_authorization": True,
        }

    def execute(self, action: dict[str, Any], *, approved: bool = False) -> dict[str, Any]:
        if not approved:
            raise PermissionError("Android Chrome action requires explicit approval")
        if not self.endpoint_url:
            raise RuntimeError("NEXUS_ANDROID_CHROME_CDP_URL is not configured")

        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError("playwright is required for Android Chrome CDP execution") from exc

        action_type = action.get("type")
        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(self.endpoint_url)
            try:
                contexts = browser.contexts
                if not contexts:
                    raise RuntimeError("no browser context exposed by CDP endpoint")
                context = contexts[0]
                pages = context.pages
                page = pages[0] if pages else context.new_page()

                if action_type == "open":
                    page.goto(str(action["url"]), wait_until="domcontentloaded")
                    result = {"url": page.url, "title": page.title()}
                elif action_type == "click":
                    page.locator(str(action["selector"])).first.click()
                    result = {"url": page.url}
                elif action_type == "type":
                    page.locator(str(action["selector"])).first.fill(str(action["text"]))
                    result = {"url": page.url}
                elif action_type == "press":
                    page.locator(str(action["selector"])).first.press(str(action["key"]))
                    result = {"url": page.url}
                elif action_type == "snapshot":
                    result = {
                        "url": page.url,
                        "title": page.title(),
                        "text": page.locator("body").inner_text()[:12000],
                    }
                else:
                    raise ValueError(f"unsupported Android Chrome action: {action_type}")

                return {
                    "adapter": self.name,
                    "executed": True,
                    "action": action,
                    "result": result,
                }
            finally:
                # The Playwright context is stopped by sync_playwright(); do
                # not call browser.close() because this endpoint may represent
                # the user's existing Android Chrome session.
                pass
