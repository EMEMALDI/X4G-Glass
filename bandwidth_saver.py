# bandwidth_saver.py
# سیستم کاهش مصرف پهنای باند (Bandwidth Optimization)
# هدف: کاهش سربار ترافیک برای رسیدن به ضریب ۲.۷ همراه اول
# روش: فشرده‌سازی هدرها، بهینه‌سازی اتصالات، کاهش حجم پکت‌ها

import gzip
import zlib
import brotli
import asyncio
import time
from collections import defaultdict

# ── آمار مصرف ────────────────────────────────────────────────────────────────
bandwidth_stats = defaultdict(lambda: {
    "original_bytes": 0,
    "compressed_bytes": 0,
    "saved_bytes": 0,
    "compression_ratio": 0.0,
    "requests": 0,
})

# ── سطوح فشرده‌سازی ──────────────────────────────────────────────────────────
COMPRESSION_LEVELS = {
    "off": {"enabled": False, "method": None},
    "gzip": {"enabled": True, "method": "gzip", "level": 6},
    "brotli": {"enabled": True, "method": "brotli", "level": 4},
    "aggressive": {"enabled": True, "method": "brotli", "level": 11},
}

# ── کش فشرده‌سازی ────────────────────────────────────────────────────────────
_compression_cache: dict = {}
CACHE_TTL = 300  # ۵ دقیقه
MAX_CACHE_SIZE = 500


def _cleanup_cache():
    """پاکسازی کش منقضی‌شده"""
    now = time.time()
    expired = [k for k, v in _compression_cache.items() if now - v["time"] > CACHE_TTL]
    for k in expired:
        del _compression_cache[k]
    # اگه کش خیلی بزرگ شد، قدیمی‌ها رو حذف کن
    if len(_compression_cache) > MAX_CACHE_SIZE:
        sorted_items = sorted(_compression_cache.items(), key=lambda x: x[1]["time"])
        for k, _ in sorted_items[:len(sorted_items) - MAX_CACHE_SIZE]:
            del _compression_cache[k]


def compress_data(data: bytes, method: str = "brotli", level: int = 4) -> tuple[bytes, str]:
    """
    فشرده‌سازی داده با روش مشخص
    برمی‌گردونه: (داده فشرده‌شده, نام روش)
    """
    if not data or len(data) < 100:  # داده‌های کوچیک ارزش فشرده‌سازی ندارن
        return data, "none"

    cache_key = f"{hash(data)}_{method}_{level}"
    if cache_key in _compression_cache:
        return _compression_cache[cache_key]["data"], method

    try:
        if method == "gzip":
            compressed = gzip.compress(data, compresslevel=min(level, 9))
        elif method == "brotli":
            compressed = brotli.compress(data, quality=min(level, 11))
        else:
            return data, "none"

        # فقط اگه فشرده‌سازی واقعاً مفید بود استفاده کن
        if len(compressed) < len(data) * 0.85:  # حداقل ۱۵٪ کاهش
            result = compressed, method
        else:
            result = data, "none"

        # ذخیره در کش
        _cleanup_cache()
        _compression_cache[cache_key] = {
            "data": result,
            "time": time.time(),
        }
        return result
    except Exception:
        return data, "none"


def decompress_data(data: bytes, method: str) -> bytes:
    """بازیابی داده فشرده‌شده"""
    if method == "none" or not data:
        return data
    try:
        if method == "gzip":
            return gzip.decompress(data)
        elif method == "brotli":
            return brotli.decompress(data)
    except Exception:
        return data
    return data


def optimize_headers(headers: dict) -> dict:
    """
    بهینه‌سازی هدرهای HTTP برای کاهش سربار
    - حذف هدرهای غیرضروری
    - کوتاه‌کردن مقادیر
    - فشرده‌سازی هدرها
    """
    # هدرهایی که می‌تونیم حذف کنیم
    removable = {
        "x-requested-with",
        "x-forwarded-for",
        "x-forwarded-proto",
        "x-real-ip",
        "cf-connecting-ip",
        "cf-ipcountry",
        "cf-ray",
        "cf-visitor",
        "x-forwarded-host",
        "x-forwarded-port",
        "x-forwarded-scheme",
    }

    optimized = {}
    for key, value in headers.items():
        key_lower = key.lower()
        if key_lower in removable:
            continue
        # کوتاه‌کردن User-Agent اگه خیلی بلند باشه
        if key_lower == "user-agent" and len(value) > 100:
            value = value[:100]
        optimized[key] = value

    return optimized


def calculate_bandwidth_saving(original: int, compressed: int) -> dict:
    """محاسبه میزان صرفه‌جویی"""
    if original <= 0:
        return {"saved": 0, "ratio": 0, "percent": 0}
    saved = original - compressed
    ratio = original / max(compressed, 1)
    percent = (saved / original) * 100
    return {
        "saved": saved,
        "ratio": round(ratio, 2),
        "percent": round(percent, 1),
    }


async def throttle_bandwidth(uuid: str, data: bytes, link: dict) -> bytes:
    """
    پردازش داده بر اساس تنظیمات کانفیگ
    اگه bandwidth_saver فعال باشه، داده رو فشرده می‌کنه
    """
    if not link.get("bandwidth_saver", False):
        return data

    # فشرده‌سازی با brotli (بهترین نسبت فشرده‌سازی)
    compressed, method = compress_data(data, "brotli", 6)

    # آپدیت آمار
    stats = bandwidth_stats[uuid]
    stats["original_bytes"] += len(data)
    stats["compressed_bytes"] += len(compressed)
    stats["saved_bytes"] += max(0, len(data) - len(compressed))
    stats["requests"] += 1
    if stats["original_bytes"] > 0:
        stats["compression_ratio"] = stats["original_bytes"] / max(stats["compressed_bytes"], 1)

    return compressed


def get_bandwidth_report(uuid: str) -> dict:
    """گزارش مصرف پهنای باند برای یک کانفیگ"""
    stats = bandwidth_stats.get(uuid, {})
    return {
        "original_bytes": stats.get("original_bytes", 0),
        "compressed_bytes": stats.get("compressed_bytes", 0),
        "saved_bytes": stats.get("saved_bytes", 0),
        "compression_ratio": round(stats.get("compression_ratio", 0), 2),
        "requests": stats.get("requests", 0),
        "savings_percent": round(
            (stats.get("saved_bytes", 0) / max(stats.get("original_bytes", 1), 1)) * 100, 1
        ),
    }


def get_global_bandwidth_report() -> dict:
    """گزارش جهانی مصرف پهنای باند"""
    total_original = sum(s["original_bytes"] for s in bandwidth_stats.values())
    total_compressed = sum(s["compressed_bytes"] for s in bandwidth_stats.values())
    total_saved = sum(s["saved_bytes"] for s in bandwidth_stats.values())
    total_requests = sum(s["requests"] for s in bandwidth_stats.values())

    return {
        "total_original": total_original,
        "total_compressed": total_compressed,
        "total_saved": total_saved,
        "total_requests": total_requests,
        "overall_ratio": round(total_original / max(total_compressed, 1), 2),
        "overall_savings_percent": round(
            (total_saved / max(total_original, 1)) * 100, 1
        ),
        "configs_count": len(bandwidth_stats),
    }
