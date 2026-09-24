"""Automatic GitHub repository discovery for Nexus.

Discovery is read-only with respect to candidate code: results are stored as
untrusted metadata and are never installed or merged automatically.
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from integrations.github_pool import capabilities

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "integrations" / "discovery-config.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def _request(url: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "User-Agent": "Gungv-Nexus-repository-discovery",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def _queries(config: dict) -> list[str]:
    return [
        f'{term} in:name,description,readme is:public archived:false fork:false'
        for term in config["search_terms"]
    ]


def _score(item: dict) -> float:
    stars = max(item.get("stargazers_count", 0), 0)
    forks = max(item.get("forks_count", 0), 0)
    return (
        min(stars, 100_000) / 100_000
        + min(forks, 20_000) / 20_000 * 0.25
        + (0.15 if item.get("license") else 0)
        + (0.10 if item.get("has_issues") else 0)
    )


def discover(limit_per_query: int | None = None) -> list[dict]:
    config = load_config()
    limit = limit_per_query or int(config["results_per_query"])
    known = {item.get("repository") for item in capabilities()}
    seen: set[str] = set()
    candidates: list[dict] = []

    for query in _queries(config):
        params = urllib.parse.urlencode({"q": query, "sort": "stars", "order": "desc", "per_page": limit})
        payload = _request(f"https://api.github.com/search/repositories?{params}")
        for item in payload.get("items", []):
            full_name = item.get("full_name")
            if not full_name or full_name in known or full_name in seen:
                continue
            seen.add(full_name)
            candidates.append({
                "repository": full_name,
                "capability": "discovered",
                "description": item.get("description"),
                "stars": item.get("stargazers_count", 0),
                "forks": item.get("forks_count", 0),
                "language": item.get("language"),
                "license": (item.get("license") or {}).get("spdx_id"),
                "updated_at": item.get("updated_at"),
                "url": item.get("html_url"),
                "score": round(_score(item), 6),
                "trust": "untrusted",
                "requires_validation": True,
            })

    candidates.sort(key=lambda x: (-x["score"], -x["stars"], x["repository"]))
    return candidates[: int(config["max_candidates"])]


def write_snapshot(output: str | Path | None = None) -> Path:
    config = load_config()
    target = Path(output) if output else ROOT / config["output"]
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "GitHub Search API",
        "status": "untrusted-discovery",
        "candidates": discover(),
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return target


if __name__ == "__main__":
    write_snapshot()
