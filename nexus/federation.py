from __future__ import annotations

from dataclasses import asdict, dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class ServiceTarget:
    name: str
    url: str
    role: str


def check_service(target: ServiceTarget, timeout: float = 5.0) -> dict:
    url = target.url.rstrip("/") + "/health"
    request = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return {
                "name": target.name,
                "role": target.role,
                "url": target.url,
                "status": "online",
                "http_status": response.status,
            }
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        return {
            "name": target.name,
            "role": target.role,
            "url": target.url,
            "status": "offline",
            "error": type(exc).__name__,
        }


def federation_snapshot(targets: list[ServiceTarget]) -> dict:
    services = [check_service(target) for target in targets]
    online = sum(item["status"] == "online" for item in services)
    return {
        "status": "ok" if online == len(services) else "degraded",
        "online": online,
        "total": len(services),
        "services": services,
    }
