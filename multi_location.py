# multi_location.py
# اتصال X4G-Glass به Cloudflare Worker
# Worker: https://restless-heart-cb0d.emem-32281.workers.dev

import httpx
import time

WORKER_URL = "https://shiny-cell-e342.emem-32281.workers.dev"

# ── اتصال به Worker ──────────────────────────────────────────────────────────
_client: httpx.AsyncClient | None = None


async def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=httpx.Timeout(15.0))
    return _client


async def worker_request(path: str, method: str = "GET", data: dict = None) -> dict:
    """درخواست به Worker"""
    client = await _get_client()
    url = f"{WORKER_URL}{path}"

    try:
        if method == "GET":
            resp = await client.get(url)
        elif method == "POST":
            resp = await client.post(url, json=data)
        else:
            return {"error": f"method {method} not supported"}

        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"HTTP {resp.status_code}"}

    except Exception as e:
        return {"error": str(e)}


# ── توابع آماده ───────────────────────────────────────────────────────────────
async def check_tor(ip: str = None) -> dict:
    """بررسی Tor/Proxy"""
    if ip:
        return await worker_request("/tor-check", "POST", {"ip": ip})
    return await worker_request("/tor-check")


async def scan_ips(ips: list, ports: list = None) -> dict:
    """اسکن آی‌پی‌ها"""
    return await worker_request("/scan", "POST", {"ips": ips, "ports": ports or [80, 443]})


async def lookup_ip(ip: str) -> dict:
    """اطلاعات آی‌پی"""
    return await worker_request(f"/lookup?ip={ip}")


async def detect_ip(ip: str) -> dict:
    """تشخیص VPN/Proxy/Tor"""
    return await worker_request(f"/detect?ip={ip}")


async def get_exit_nodes() -> dict:
    """لیست Exit Node های Tor"""
    return await worker_request("/exit-nodes")


async def get_countries() -> dict:
    """لیست کشورها"""
    return await worker_request("/countries")


async def get_worker_stats() -> dict:
    """آمار Worker"""
    return await worker_request("/stats")


async def health_check() -> dict:
    """سلامت Worker"""
    return await worker_request("/stats")


# ── بستن اتصال ───────────────────────────────────────────────────────────────
async def close():
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
