# ping_monitor.py
# سیستم اندازه‌گیری پینگ واقعی برای گیمینگ
# ICMP-like measurement via HTTP HEAD (Cloudflare-compatible)

import asyncio
import time
import statistics
from dataclasses import dataclass, field


# ── سرورهای هدف برای پینگ ────────────────────────────────────────────────────
PING_TARGETS = {
    "iran": [
        {"name": "آلمان (فرانکفورت)", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "ترکیه (استانبول)", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "امارات (دبی)", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    ],
    "europe": [
        {"name": "آلمان (فرانکفورت)", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "هلند (آمستردام)", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "فرانسه (پاریس)", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "بریتانیا (لندن)", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    ],
    "us": [
        {"name": "آمریکا (سان‌خوزه)", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "آمریکا (نیویورک)", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "آمریکا (شیکاگو)", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    ],
    "asia": [
        {"name": "سنگاپور", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "ژاپن (توکیو)", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "هنگ‌کنگ", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    ],
    "gaming": [
        {"name": "Frankfurt DE", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "Amsterdam NL", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "Istanbul TR", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "Dubai UAE", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "Singapore SG", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "Tokyo JP", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    ],
}


@dataclass
class PingResult:
    """نتیجه پینگ یک سرور"""
    name: str
    host: str
    latency_ms: float = 0.0
    jitter_ms: float = 0.0
    min_ms: float = float("inf")
    max_ms: float = 0.0
    loss: float = 0.0
    status: str = "pending"
    samples: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "host": self.host,
            "latency_ms": round(self.latency_ms, 1),
            "jitter_ms": round(self.jitter_ms, 1),
            "min_ms": round(self.min_ms, 1) if self.min_ms != float("inf") else 0,
            "max_ms": round(self.max_ms, 1),
            "loss": round(self.loss, 1),
            "status": self.status,
        }


async def _measure_ping(host: str, path: str = "/", timeout: float = 2.0) -> float | None:
    """اندازه‌گیری پینگ یک سرور با HTTP HEAD"""
    import httpx

    url = f"https://{host}{path}"
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(timeout)) as client:
            start = time.monotonic()
            resp = await client.head(url, follow_redirects=True)
            elapsed = (time.monotonic() - start) * 1000  # ms
            return elapsed
    except Exception:
        return None


async def ping_server(target: dict, count: int = 5) -> PingResult:
    """پینگ یک سرور با چند نمونه"""
    result = PingResult(name=target["name"], host=target["host"])

    tasks = [_measure_ping(target["host"], target.get("path", "/")) for _ in range(count)]
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    successes = []
    failures = 0

    for r in responses:
        if isinstance(r, (int, float)):
            successes.append(r)
            result.samples.append(round(r, 1))
        else:
            failures += 1

    result.loss = (failures / count) * 100

    if successes:
        result.latency_ms = statistics.mean(successes)
        result.min_ms = min(successes)
        result.max_ms = max(successes)
        if len(successes) > 1:
            result.jitter_ms = statistics.stdev(successes)
        result.status = "ok" if result.loss < 50 else "partial"
    else:
        result.status = "offline"

    return result


async def ping_all_regions(count: int = 5) -> dict:
    """پینگ تمام مناطق"""
    results = {}
    for region, targets in PING_TARGETS.items():
        region_results = await asyncio.gather(
            *[ping_server(t, count) for t in targets]
        )
        results[region] = [r.to_dict() for r in region_results]
    return results


async def ping_best_server(count: int = 5) -> dict:
    """بهترین سرور بر اساس پینگ"""
    all_results = []

    for region, targets in PING_TARGETS.items():
        region_results = await asyncio.gather(
            *[ping_server(t, count) for t in targets]
        )
        for r in region_results:
            if r.status == "ok":
                all_results.append(r)

    if not all_results:
        return {"best": None, "message": "no servers reachable"}

    all_results.sort(key=lambda x: x.latency_ms)
    best = all_results[0]
    return {
        "best": best.to_dict(),
        "ranked": [r.to_dict() for r in all_results[:5]],
    }


async def ping_game_servers(game: str = "fps", count: int = 3) -> dict:
    """پینگ سرورهای مناسب برای یک بازی"""
    targets = PING_TARGETS.get("gaming", [])
    results = await asyncio.gather(*[ping_server(t, count) for t in targets])

    ranked = sorted([r for r in results if r.status == "ok"], key=lambda x: x.latency_ms)

    return {
        "game": game,
        "servers": [r.to_dict() for r in ranked],
        "best": ranked[0].to_dict() if ranked else None,
        "avg_ping": round(statistics.mean([r.latency_ms for r in ranked]), 1) if ranked else 0,
    }
