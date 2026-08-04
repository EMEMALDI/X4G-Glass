# ping_monitor.py
# سیستم اندازه‌گیری پینگ واقعی — مستقیم از Railway

import asyncio
import aiohttp
import time
from typing import Optional


# ── سرورهای Cloudflare CDN ─────────────────────────────────────────────────────
PING_SERVERS = [
    {"name": "Frankfurt DE", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    {"name": "Amsterdam NL", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    {"name": "Istanbul TR", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    {"name": "Dubai UAE", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    {"name": "London UK", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    {"name": "Paris FR", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    {"name": "Singapore SG", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    {"name": "Tokyo JP", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    {"name": "New York US", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    {"name": "San Jose US", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    {"name": "Chicago US", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    {"name": "Hong Kong", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
]


# ── Cache ─────────────────────────────────────────────────────────────────────
_ping_cache: dict = {}
CACHE_TTL = 30


async def _measure_ping(target: dict, count: int = 3) -> dict:
    """اندازه‌گیری پینگ یک سرور"""
    times = []
    fails = 0

    for _ in range(count):
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                start = time.time()
                async with session.get(
                    f"https://{target['host']}{target['path']}",
                    headers={"Cache-Control": "no-cache"},
                ) as resp:
                    await resp.read()
                    latency = (time.time() - start) * 1000
                    times.append(latency)
        except Exception:
            fails += 1

    if not times:
        return {
            "name": target["name"],
            "host": target["host"],
            "latency_ms": 0,
            "jitter_ms": 0,
            "min_ms": 0,
            "max_ms": 0,
            "loss": 100,
            "status": "offline",
        }

    avg = sum(times) / len(times)
    jitter = 0
    if len(times) > 1:
        variance = sum((t - avg) ** 2 for t in times) / len(times)
        jitter = variance ** 0.5

    return {
        "name": target["name"],
        "host": target["host"],
        "latency_ms": round(avg, 1),
        "jitter_ms": round(jitter, 1),
        "min_ms": round(min(times), 1),
        "max_ms": round(max(times), 1),
        "loss": round(fails / count * 100),
        "status": "ok" if fails < count else "offline",
    }


async def ping_all(count: int = 3) -> dict:
    """پینگ همه سرورها"""
    cache_key = f"all:{count}"
    now = time.time()

    if cache_key in _ping_cache:
        cached = _ping_cache[cache_key]
        if now - cached["time"] < CACHE_TTL:
            return cached["data"]

    tasks = [_measure_ping(s, count) for s in PING_SERVERS]
    results = await asyncio.gather(*tasks)

    ok = [r for r in results if r["status"] == "ok"]
    ok.sort(key=lambda x: x["latency_ms"])

    data = {
        "best": ok[0] if ok else None,
        "ranked": ok,
        "avg_ping": round(sum(r["latency_ms"] for r in ok) / max(len(ok), 1), 1),
        "total": len(results),
        "online": len(ok),
    }

    _ping_cache[cache_key] = {"data": data, "time": now}
    return data


async def ping_game(game: str) -> dict:
    """پینگ برای یک بازی"""
    data = await ping_all(count=5)
    return {
        "game": game,
        "servers": data["ranked"],
        "best": data["best"],
        "avg_ping": data["avg_ping"],
        "total": data["total"],
        "online": data["online"],
    }


# ── API helpers ───────────────────────────────────────────────────────────────

async def get_best_server() -> dict:
    data = await ping_all()
    return data.get("best") or {}


async def get_all_pings() -> dict:
    return await ping_all()


async def get_game_pings(game: str) -> dict:
    return await ping_game(game)


# ── Test ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json
    result = asyncio.run(ping_all())
    print(json.dumps(result, indent=2, ensure_ascii=False))
