# ping_monitor.py
# سیستم اندازه‌گیری پینگ از طریق Cloudflare Worker
# نتایج از Edge های Cloudflare میاد، نه از Railway

import asyncio
import aiohttp
import time
import statistics
from typing import Optional


# ── Worker URL ────────────────────────────────────────────────────────────────
WORKER_URL = "https://shiny-cell-e342.emem-32281.workers.dev"


# ── Cache ─────────────────────────────────────────────────────────────────────
_ping_cache: dict = {}
CACHE_TTL = 30  # ۳۰ ثانیه کش


async def fetch_ping_from_worker(game: str = "all", count: int = 3) -> dict:
    """
    پینگ از Cloudflare Worker می‌گیره.
    نتایج از Edge های سراسر دنیا میاد.
    """
    cache_key = f"{game}:{count}"
    now = time.time()

    # چک کش
    if cache_key in _ping_cache:
        cached = _ping_cache[cache_key]
        if now - cached["time"] < CACHE_TTL:
            return cached["data"]

    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                f"{WORKER_URL}/ping",
                params={"game": game, "count": str(count)},
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    _ping_cache[cache_key] = {"data": data, "time": now}
                    return data
    except Exception as e:
        pass

    # fallback: پینگ محلی
    return await local_ping_fallback()


async def local_ping_fallback() -> dict:
    """پینگ محلی از Railway (fallback اگه Worker نبود)"""
    targets = [
        {"name": "Frankfurt DE", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "Amsterdam NL", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "Dubai UAE", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
        {"name": "Istanbul TR", "host": "speed.cloudflare.com", "path": "/cdn-cgi/trace"},
    ]

    servers = []
    for t in targets:
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                start = time.time()
                async with session.get(
                    f"https://{t['host']}{t['path']}",
                    headers={"Cache-Control": "no-cache"},
                ) as resp:
                    latency = (time.time() - start) * 1000
                    servers.append({
                        "name": t["name"],
                        "latency": round(latency, 1),
                        "status": "ok",
                        "jitter": 0,
                    })
        except Exception:
            pass

    servers.sort(key=lambda x: x["latency"])
    return {
        "game": "local",
        "edge": "Railway Amsterdam (fallback)",
        "servers": servers,
        "best": servers[0] if servers else None,
        "avg_ping": round(sum(s["latency"] for s in servers) / max(len(servers), 1), 1),
        "total": len(targets),
        "online": len(servers),
    }


# ── API functions ─────────────────────────────────────────────────────────────

async def get_best_server(game: str = "all") -> dict:
    """بهترین سرور"""
    data = await fetch_ping_from_worker(game)
    return data.get("best") or {}


async def get_all_pings(game: str = "all") -> dict:
    """پینگ همه سرورها"""
    return await fetch_ping_from_worker(game)


async def get_game_pings(game: str) -> dict:
    """پینگ برای یک بازی خاص"""
    return await fetch_ping_from_worker(game)


# ── Standalone test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json
    result = asyncio.run(get_all_pings())
    print(json.dumps(result, indent=2, ensure_ascii=False))
