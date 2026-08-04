# multi_location.py
# سیستم مسیریابی چندمکانی برای X4G-Glass
# Cloudflare Worker: https://restless-heart-cb0d.emem-32281.workers.dev

import asyncio
import time
import httpx
from datetime import datetime

# ── Worker فعال ───────────────────────────────────────────────────────────────
ACTIVE_WORKERS = {
    "default": {
        "id": "default",
        "name": "🌐 Cloudflare Edge",
        "worker_url": "https://restless-heart-cb0d.emem-32281.workers.dev",
        "region": "auto",
        "flag": "🌍",
        "status": "unknown",
        "latency": 0,
        "last_check": None,
        "colo": "",
        "country": "",
    },
}

# ── لوکیشن‌های پیشنهادی برای دیپلوی بعدی ─────────────────────────────────────
SUGGESTED_LOCATIONS = [
    {"id": "us", "name": "🇺🇸 آمریکا", "flag": "🇺🇸", "region": "wnam"},
    {"id": "eu", "name": "🇪🇺 اروپا", "flag": "🇪🇺", "region": "weur"},
    {"id": "asia", "name": "🌏 آسیا", "flag": "🌏", "region": "apac"},
    {"id": "turkey", "name": "🇹🇷 ترکیه", "flag": "🇹🇷", "region": "eeur"},
    {"id": "germany", "name": "🇩🇪 آلمان", "flag": "🇩🇪", "region": "weur"},
]

# ── HTTP Client ───────────────────────────────────────────────────────────────
_http_client: httpx.AsyncClient | None = None


async def _get_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))
    return _http_client


# ── Health Check ──────────────────────────────────────────────────────────────
async def check_worker_health(worker_id: str = "default") -> dict:
    """بررسی سلامت یک Worker"""
    worker = ACTIVE_WORKERS.get(worker_id)
    if not worker:
        return {"status": "not_found"}

    client = await _get_client()
    start = time.time()

    try:
        resp = await client.get(f"{worker['worker_url']}/health")
        latency = round((time.time() - start) * 1000, 1)

        if resp.status_code == 200:
            data = resp.json()
            worker["status"] = "active"
            worker["latency"] = latency
            worker["colo"] = data.get("colo", "")
            worker["country"] = data.get("country", "")
            worker["last_check"] = datetime.now().isoformat()
            worker["origin_status"] = data.get("origin", "unknown")
            return {"status": "active", "latency": latency, **data}
        else:
            worker["status"] = "error"
            worker["latency"] = 0
            return {"status": "error"}

    except Exception as e:
        worker["status"] = "unreachable"
        worker["latency"] = 0
        return {"status": "unreachable", "error": str(e)}


async def check_all_workers() -> dict:
    """بررسی سلامت تمام Worker ها"""
    results = {}
    for wid in ACTIVE_WORKERS:
        results[wid] = await check_worker_health(wid)
    return results


# ── Manager ───────────────────────────────────────────────────────────────────
def get_workers() -> dict:
    """لیست تمام Worker ها"""
    return {
        "active": ACTIVE_WORKERS,
        "suggested": SUGGESTED_LOCATIONS,
    }


def get_worker_url(worker_id: str = "default") -> str:
    """آدرس یک Worker"""
    w = ACTIVE_WORKERS.get(worker_id)
    return w["worker_url"] if w else ""


def get_best_worker() -> str | None:
    """بهترین Worker بر اساس لیتنسی"""
    active = {k: v for k, v in ACTIVE_WORKERS.items() if v["status"] == "active"}
    if not active:
        return None
    return min(active, key=lambda k: active[k]["latency"])


def add_worker(worker_id: str, name: str, worker_url: str, region: str = "auto", flag: str = "🌐") -> bool:
    """افزودن Worker جدید"""
    if worker_id in ACTIVE_WORKERS:
        return False
    ACTIVE_WORKERS[worker_id] = {
        "id": worker_id,
        "name": name,
        "worker_url": worker_url,
        "region": region,
        "flag": flag,
        "status": "unknown",
        "latency": 0,
        "last_check": None,
    }
    return True


def remove_worker(worker_id: str) -> bool:
    """حذف Worker"""
    if worker_id == "default":
        return False  # پیش‌فرض رو نمی‌شه حذف کرد
    return ACTIVE_WORKERS.pop(worker_id, None) is not None


async def close():
    global _http_client
    if _http_client and not _http_client.is_closed:
        await _http_client.aclose()
