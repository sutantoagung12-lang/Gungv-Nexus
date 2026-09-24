"""Instagram Business Login connector for Gungv-Nexus.

Uses the current Instagram API with Instagram Login for professional
(Business/Creator) accounts. Secrets are read only from environment variables.
No credentials are persisted by this module.
"""
from __future__ import annotations

import json
import os
import secrets
import urllib.parse
import urllib.request
from dataclasses import dataclass


AUTH_URL = "https://www.instagram.com/oauth/authorize"
TOKEN_URL = "https://api.instagram.com/oauth/access_token"
GRAPH_URL = "https://graph.instagram.com"


class InstagramConnectorError(RuntimeError):
    pass


@dataclass(frozen=True)
class InstagramConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    api_version: str
    scopes: tuple[str, ...] = (
        "instagram_business_basic",
        "instagram_business_content_publish",
    )

    @classmethod
    def from_env(cls) -> "InstagramConfig":
        missing = [
            name for name in ("INSTAGRAM_CLIENT_ID", "INSTAGRAM_CLIENT_SECRET", "INSTAGRAM_REDIRECT_URI")
            if not os.getenv(name)
        ]
        if missing:
            raise InstagramConnectorError("Missing Instagram configuration: " + ", ".join(missing))
        return cls(
            client_id=os.environ["INSTAGRAM_CLIENT_ID"],
            client_secret=os.environ["INSTAGRAM_CLIENT_SECRET"],
            redirect_uri=os.environ["INSTAGRAM_REDIRECT_URI"],
            api_version=os.getenv("INSTAGRAM_API_VERSION", "").strip(),
        )


def authorization_url(config: InstagramConfig, state: str | None = None) -> tuple[str, str]:
    state = state or secrets.token_urlsafe(32)
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": ",".join(config.scopes),
        "state": state,
        "enable_fb_login": "0",
        "force_authentication": "1",
    }
    return AUTH_URL + "?" + urllib.parse.urlencode(params), state


def _request(url: str, *, method: str = "GET", data: dict | None = None, token: str | None = None) -> dict:
    encoded = urllib.parse.urlencode(data or {}).encode()
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=encoded if method != "GET" else None, headers=headers, method=method)
    if method == "GET" and data:
        req.full_url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(data)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise InstagramConnectorError(f"Instagram API request failed: {exc}") from exc


def exchange_code(config: InstagramConfig, code: str) -> dict:
    return _request(
        TOKEN_URL,
        method="POST",
        data={
            "client_id": config.client_id,
            "client_secret": config.client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": config.redirect_uri,
            "code": code,
        },
    )


def exchange_long_lived(config: InstagramConfig, short_lived_token: str) -> dict:
    return _request(
        f"{GRAPH_URL}/access_token",
        data={
            "grant_type": "ig_exchange_token",
            "client_secret": config.client_secret,
            "access_token": short_lived_token,
        },
    )


def refresh_long_lived(token: str) -> dict:
    return _request(
        f"{GRAPH_URL}/refresh_access_token",
        data={"grant_type": "ig_refresh_token", "access_token": token},
    )


def profile(config: InstagramConfig, token: str) -> dict:
    if not config.api_version:
        raise InstagramConnectorError("INSTAGRAM_API_VERSION is required for Graph API calls")
    return _request(
        f"{GRAPH_URL}/{config.api_version}/me",
        data={"fields": "id,user_id,username,name,account_type,media_count"},
        token=token,
    )


def create_image(config: InstagramConfig, token: str, image_url: str, caption: str = "") -> dict:
    return _media_container(config, token, {"image_url": image_url, "caption": caption})


def create_reel(config: InstagramConfig, token: str, video_url: str, caption: str = "") -> dict:
    return _media_container(
        config, token, {"media_type": "REELS", "video_url": video_url, "caption": caption}
    )


def _media_container(config: InstagramConfig, token: str, payload: dict) -> dict:
    if not config.api_version:
        raise InstagramConnectorError("INSTAGRAM_API_VERSION is required for publishing")
    return _request(
        f"{GRAPH_URL}/{config.api_version}/me/media",
        method="POST",
        data=payload,
        token=token,
    )


def publish(config: InstagramConfig, token: str, creation_id: str) -> dict:
    if not config.api_version:
        raise InstagramConnectorError("INSTAGRAM_API_VERSION is required for publishing")
    return _request(
        f"{GRAPH_URL}/{config.api_version}/me/media_publish",
        method="POST",
        data={"creation_id": creation_id},
        token=token,
    )


def container_status(config: InstagramConfig, token: str, container_id: str) -> dict:
    if not config.api_version:
        raise InstagramConnectorError("INSTAGRAM_API_VERSION is required")
    return _request(
        f"{GRAPH_URL}/{config.api_version}/{container_id}",
        data={"fields": "status_code,status"},
        token=token,
    )
