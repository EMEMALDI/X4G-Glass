# multi_location.py
# سیستم مسیریابی چندمکانی برای X4G-Glass
# استفاده از Cloudflare Workers به عنوان edge nodes

import asyncio
import time
import httpx
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

# ── لوکیشن‌های پشتیبانی‌شده ───────────────────────────────────────────────────
LOCATIONS = {
    "us-east": {
        "name": "🇺🇸 آمریکا شرقی",
        "region": "wnam",
        "worker_url": "",
        "flag": "🇺🇸",
        "latency": 0,
        "status": "inactive",
    },
    "us-west": {
        "name": "🇺🇸 آمریکا غربی",
        "region": "wnam",
        "worker_url": "",
        "flag": "🇺🇸",
        "latency": 0,
        "status": "inactive",
    },
    "eu-west": {
        "name": "🇪🇺 اروپا غربی",
        "region": "weur",
        "worker_url": "",
        "flag": "🇪🇺",
        "latency": 0,
        "status": "inactive",
    },
    "eu-east": {
        "name": "🇪🇺 اروپا شرقی",
        "region": "eeur",
        "worker_url": "",
        "flag": "🇪🇺",
        "latency": 0,
        "status": "inactive",
    },
    "asia": {
        "name": "🌏 آسیا",
        "region": "apac",
        "worker_url": "",
        "flag": "🌏",
        "latency": 0,
        "status": "inactive",
    },
    "turkey": {
        "name": "🇹🇷 ترکیه",
        "region": "eeur",
        "worker_url": "",
        "flag": "🇹🇷",
        "latency": 0,
        "status": "inactive",
    },
    "germany": {
        "name": "🇩🇪 آلمان",
        "region": "weur",
        "worker_url": "",
        "flag": "🇩🇪",
        "latency": 0,
        "status": "inactive",
    },
    "france": {
        "name": "🇫🇷 فرانسه",
        "region": "weur",
        "worker_url": "",
        "flag": "🇫🇷",
        "latency": 0,
        "status": "inactive",
    },
    "singapore": {
        "name": "🇸🇬 سنگاپور",
        "region": "apac",
        "worker_url": "",
        "flag": "🇸🇬",
        "latency": 0,
        "status": "inactive",
    },
    "japan": {
        "name": "🇯🇵 ژاپن",
        "region": "apac",
        "worker_url": "",
        "flag": "🇯🇵",
        "latency": 0,
        "status": "inactive",
    },
}

# ── کلاس مدیریت لوکیشن ──────────────────────────────────────────────────────
@dataclass
class LocationManager:
    """مدیریت لوکیشن‌های Cloudflare Worker"""
    
    locations: dict = field(default_factory=lambda: dict(LOCATIONS))
    health_check_interval: int = 60  # ثانیه
    _last_health_check: float = 0
    _http_client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(10.0),
                follow_redirects=True,
            )
        return self._http_client
    
    async def check_location_health(self, location_id: str) -> dict:
        """بررسی سلامت یک لوکیشن"""
        loc = self.locations.get(location_id)
        if not loc or not loc.get("worker_url"):
            return {"status": "inactive", "latency": 0}
        
        client = await self._get_client()
        start_time = time.time()
        
        try:
            response = await client.get(f"{loc['worker_url']}/health")
            latency = (time.time() - start_time) * 1000  # میلی‌ثانیه
            
            if response.status_code == 200:
                loc["status"] = "active"
                loc["latency"] = round(latency, 2)
                loc["last_check"] = datetime.now().isoformat()
                return {"status": "active", "latency": loc["latency"]}
            else:
                loc["status"] = "error"
                loc["latency"] = 0
                return {"status": "error", "latency": 0}
                
        except Exception as e:
            loc["status"] = "error"
            loc["latency"] = 0
            return {"status": "error", "latency": 0, "error": str(e)}
    
    async def health_check_all(self) -> dict:
        """بررسی سلامت تمام لوکیشن‌ها"""
        results = {}
        for loc_id in self.locations:
            results[loc_id] = await self.check_location_health(loc_id)
        self._last_health_check = time.time()
        return results
    
    def get_active_locations(self) -> dict:
        """لیست لوکیشن‌های فعال"""
        return {
            k: v for k, v in self.locations.items()
            if v.get("status") == "active" and v.get("worker_url")
        }
    
    def get_best_location(self) -> Optional[str]:
        """بهترین لوکیشن بر اساس لیتنسی"""
        active = self.get_active_locations()
        if not active:
            return None
        return min(active.keys(), key=lambda k: active[k].get("latency", float('inf')))
    
    def get_location_by_region(self, region: str) -> Optional[str]:
        """پیدا کردن لوکیشن بر اساس منطقه"""
        for loc_id, loc in self.locations.items():
            if loc.get("region") == region and loc.get("status") == "active":
                return loc_id
        return None
    
    def update_location(self, location_id: str, data: dict) -> bool:
        """آپدیت اطلاعات یک لوکیشن"""
        if location_id not in self.locations:
            return False
        self.locations[location_id].update(data)
        return True
    
    def add_location(self, location_id: str, data: dict) -> bool:
        """افزودن لوکیشن جدید"""
        if location_id in self.locations:
            return False
        self.locations[location_id] = {
            "name": data.get("name", location_id),
            "region": data.get("region", "auto"),
            "worker_url": data.get("worker_url", ""),
            "flag": data.get("flag", "🌐"),
            "latency": 0,
            "status": "inactive",
        }
        return True
    
    def remove_location(self, location_id: str) -> bool:
        """حذف یک لوکیشن"""
        if location_id not in self.locations:
            return False
        del self.locations[location_id]
        return True
    
    def get_stats(self) -> dict:
        """آمار کلی"""
        active = self.get_active_locations()
        return {
            "total_locations": len(self.locations),
            "active_locations": len(active),
            "inactive_locations": len(self.locations) - len(active),
            "locations": {
                k: {
                    "name": v["name"],
                    "status": v["status"],
                    "latency": v.get("latency", 0),
                    "worker_url": v.get("worker_url", ""),
                }
                for k, v in self.locations.items()
            },
            "last_health_check": self._last_health_check,
        }
    
    async def close(self):
        """بستن اتصال HTTP"""
        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()


# ── نمونه سراسری ─────────────────────────────────────────────────────────────
location_manager = LocationManager()


# ── توابع کمکی ───────────────────────────────────────────────────────────────
def get_worker_url_for_location(location_id: str) -> str:
    """دریافت آدرس Worker برای یک لوکیشن"""
    loc = location_manager.locations.get(location_id)
    if loc and loc.get("worker_url"):
        return loc["worker_url"]
    return ""


def generate_worker_config(location_id: str, origin_url: str) -> dict:
    """تولید پیکربندی Worker برای یک لوکیشن"""
    loc = location_manager.locations.get(location_id)
    if not loc:
        return {}
    
    return {
        "name": f"x4g-{location_id}",
        "main": "x4g-worker.js",
        "compatibility_date": "2024-01-01",
        "vars": {
            "ORIGIN_URL": origin_url,
            "REGION": loc.get("region", "auto"),
            "GAMING_MODE": "false",
            "COMPRESS_RESPONSE": "true",
        },
    }


def generate_wrangler_commands(location_id: str, origin_url: str) -> list:
    """تولید دستورات wrangler برای دیپلوی"""
    config = generate_worker_config(location_id, origin_url)
    if not config:
        return []
    
    return [
        f"# دیپلوی Worker برای {location_id}",
        f"wrangler deploy --name {config['name']}",
        f"# یا با پیکربندی سفارشی:",
        f"wrangler deploy --name {config['name']} --compatibility-date 2024-01-01",
    ]
