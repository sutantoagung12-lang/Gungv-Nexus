#!/usr/bin/env python3
"""Generate a standalone mobile-friendly Nexus health dashboard."""

from __future__ import annotations

import html
import sys
from pathlib import Path

from scripts.nexus_health import build_report


def render(report: dict) -> str:
    overall = html.escape(report["overall"])
    summary = report["summary"]
    cards = []
    for item in report["checks"]:
        status = html.escape(item["status"])
        name = html.escape(item["name"].replace("_", " ").title())
        detail = html.escape(item["detail"])
        diagnostic = item.get("diagnostic")
        extra = ""
        if diagnostic:
            extra = (
                f'<p><b>Action:</b> {html.escape(diagnostic["action"])}</p>'
                f'<p><b>Next:</b> {html.escape(diagnostic["next_step"])}</p>'
            )
        cards.append(
            f'<section class="card"><div class="row"><strong>{name}</strong>'
            f'<span class="status {status.lower()}">{status}</span></div>'
            f'<p>{detail}</p>{extra}</section>'
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#111827">
<title>Gungv-Nexus Health</title>
<style>
:root{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:#f3f4f6;color:#111827}}
body{{margin:0;padding:20px;max-width:720px;margin-inline:auto}}
header{{background:#111827;color:white;border-radius:18px;padding:20px;margin-bottom:14px}}
h1{{margin:0 0 6px;font-size:1.45rem}} .muted{{opacity:.75;font-size:.9rem}}
.card{{background:white;border-radius:14px;padding:16px;margin:10px 0;box-shadow:0 1px 5px #0001}}
.row{{display:flex;justify-content:space-between;gap:12px;align-items:center}}
.status{{font-size:.76rem;font-weight:700;border-radius:999px;padding:5px 9px}}
.pass{{background:#dcfce7;color:#166534}} .blocked{{background:#fef3c7;color:#92400e}}
.ready{{background:#dbeafe;color:#1e40af}} .fail{{background:#fee2e2;color:#991b1b}}
p{{margin:8px 0 0;color:#4b5563;word-break:break-word;line-height:1.4}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:14px}}
.metric{{background:#ffffff22;border-radius:12px;padding:10px;text-align:center}}
.metric b{{display:block;font-size:1.25rem}}
footer{{color:#6b7280;font-size:.8rem;margin-top:16px;text-align:center}}
</style>
</head>
<body>
<header>
<h1>Gungv-Nexus Health</h1>
<div class="muted">Contract, diagnostics and activation safety</div>
<div class="grid">
<div class="metric"><b>{summary["pass"]}</b>PASS</div>
<div class="metric"><b>{summary["blocked"]}</b>BLOCKED</div>
<div class="metric"><b>{summary["fail"]}</b>FAIL</div>
</div>
</header>
{''.join(cards)}
<footer>Overall: {overall} · external execution remains disabled by default</footer>
</body>
</html>
"""


def main() -> int:
    report = build_report()
    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("health/nexus-health.html")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render(report), encoding="utf-8")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
