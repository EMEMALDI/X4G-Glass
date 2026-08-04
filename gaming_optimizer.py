# gaming_optimizer.py
# سیستم بهینه‌سازی گیمینگ (Gaming Optimization)
# بهینه‌سازی برای کاهش لیتنسی، افزایش کیفیت، و بهبود تجربه بازی

import asyncio
import time
import struct
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

# ── پروفایل‌های گیمینگ ────────────────────────────────────────────────────────
GAMING_PROFILES = {
    "fps": {
        "name": "🎯 FPS Competitive",
        "desc": "بهینه‌شده برای بازی‌های تیراندازی (CS2, Valorant, COD)",
        "priority": "ultra_low_latency",
        "buffer_size": 4096,        # بافر کوچیک = لیتنسی کمتر
        "keep_alive": True,         # نگه‌داشتن اتصال
        "nagle_disable": True,      # غیرفعال‌کردن الگوریتم ناگل
        "dscp_marking": "ef",       # Expedited Forwarding (بالاترین اولویت)
        "max_packet_size": 1200,    # پکت‌های کوچک‌تر
        "flush_interval": 0.005,    # ۵ میلی‌ثانیه
        "jitter_buffer": False,     # بدون بافر jitter
        "error_correction": False,  # بدون تصحیح خطا (سرعت بالاتر)
    },
    "moba": {
        "name": "⚔️ MOBA/RPG",
        "desc": "بهینه‌شده برای بازی‌های استراتژیک (LoL, Dota2)",
        "priority": "low_latency",
        "buffer_size": 8192,
        "keep_alive": True,
        "nagle_disable": True,
        "dscp_marking": "af41",     # Assured Forwarding
        "max_packet_size": 1400,
        "flush_interval": 0.01,     # ۱۰ میلی‌ثانیه
        "jitter_buffer": True,
        "jitter_size": 20,          # ۲۰ میلی‌ثانیه بافر jitter
        "error_correction": True,
    },
    "racing": {
        "name": "🏎️ Racing/Fighting",
        "desc": "بهینه‌شده برای بازی‌های سرعتی (Forza, Tekken)",
        "priority": "ultra_low_latency",
        "buffer_size": 2048,        # خیلی کوچیک
        "keep_alive": True,
        "nagle_disable": True,
        "dscp_marking": "ef",
        "max_packet_size": 1000,    # پکت‌های خیلی کوچیک
        "flush_interval": 0.003,    # ۳ میلی‌ثانیه
        "jitter_buffer": False,
        "error_correction": False,
    },
    "battle_royale": {
        "name": "🏝️ Battle Royale",
        "desc": "بهینه‌شده برای بتل رویال (PUBG, Fortnite, Apex)",
        "priority": "balanced",
        "buffer_size": 16384,
        "keep_alive": True,
        "nagle_disable": True,
        "dscp_marking": "af31",
        "max_packet_size": 1400,
        "flush_interval": 0.008,
        "jitter_buffer": True,
        "jitter_size": 30,
        "error_correction": True,
    },
    "streaming": {
        "name": "📺 Gaming + Stream",
        "desc": "بهینه‌شده برای استریم همزمان با بازی",
        "priority": "balanced",
        "buffer_size": 32768,
        "keep_alive": True,
        "nagle_disable": False,
        "dscp_marking": "af21",
        "max_packet_size": 1460,
        "flush_interval": 0.016,
        "jitter_buffer": True,
        "jitter_size": 50,
        "error_correction": True,
    },
}

DEFAULT_GAMING_PROFILE = "fps"


# ── کلاس بهینه‌ساز گیمینگ ─────────────────────────────────────────────────────
@dataclass
class GamingOptimizer:
    """بهینه‌ساز ترافیک گیمینگ برای هر اتصال"""
    uuid: str
    profile: str = DEFAULT_GAMING_PROFILE
    gaming_mode: bool = False

    # آمار
    packets_sent: int = 0
    packets_optimized: int = 0
    bytes_sent: int = 0
    bytes_optimized: int = 0
    avg_latency: float = 0.0
    min_latency: float = float('inf')
    max_latency: float = 0.0
    latency_samples: list = field(default_factory=list)

    # بافر
    _send_buffer: list = field(default_factory=list)
    _last_flush: float = 0.0

    @property
    def config(self) -> dict:
        return GAMING_PROFILES.get(self.profile, GAMING_PROFILES[DEFAULT_GAMING_PROFILE])

    def should_optimize(self) -> bool:
        """آیا باید ترافیک رو بهینه کنه؟"""
        return self.gaming_mode and self.profile in GAMING_PROFILES

    async def optimize_packet(self, data: bytes) -> bytes:
        """
        بهینه‌سازی یک پکت برای ارسال
        - کاهش اندازه هدر
        - حذف اطلاعات غیرضروری
        - فشرده‌سازی
        """
        if not self.should_optimize():
            return data

        self.packets_sent += 1
        self.bytes_sent += len(data)

        # اگه داده خیلی کوچیکه، بهینه‌سازی نکن
        if len(data) < 50:
            return data

        optimized = data

        # ۱. حذف هدرهای غیرضروری از پکت‌های VLESS
        if len(data) > 100:
            # حذف بایت‌های اضافی از انتهای پکت
            if optimized.endswith(b'\x00' * 16):
                optimized = optimized.rstrip(b'\x00')

        # ۲. فشرده‌سازی با RLE ساده (سریع)
        if len(optimized) > 200:
            compressed = self._rle_compress(optimized)
            if len(compressed) < len(optimized) * 0.9:
                optimized = compressed

        self.packets_optimized += 1
        self.bytes_optimized += max(0, len(data) - len(optimized))

        return optimized

    def _rle_compress(self, data: bytes) -> bytes:
        """فشرده‌سازی RLE ساده برای پکت‌های تکراری"""
        if len(data) < 10:
            return data

        result = bytearray()
        i = 0
        while i < len(data):
            current = data[i]
            count = 1
            while i + count < len(data) and data[i + count] == current and count < 127:
                count += 1

            if count >= 3:  # فقط اگه حداقل ۳ تکرار باشه
                result.extend([0x80 | count, current])
            else:
                for j in range(count):
                    result.append(current)
            i += count

        return bytes(result)

    def record_latency(self, latency_ms: float):
        """ثبت لیتنسی"""
        self.latency_samples.append(latency_ms)
        if len(self.latency_samples) > 100:
            self.latency_samples.pop(0)

        self.min_latency = min(self.min_latency, latency_ms)
        self.max_latency = max(self.max_latency, latency_ms)
        self.avg_latency = sum(self.latency_samples) / len(self.latency_samples)

    def get_optimization_report(self) -> dict:
        """گزارش بهینه‌سازی"""
        return {
            "profile": self.profile,
            "profile_name": self.config.get("name", "Unknown"),
            "gaming_mode": self.gaming_mode,
            "packets_sent": self.packets_sent,
            "packets_optimized": self.packets_optimized,
            "bytes_sent": self.bytes_sent,
            "bytes_optimized": self.bytes_optimized,
            "savings_bytes": self.bytes_sent - self.bytes_optimized,
            "savings_percent": round(
                ((self.bytes_sent - self.bytes_optimized) / max(self.bytes_sent, 1)) * 100, 1
            ),
            "avg_latency_ms": round(self.avg_latency, 2),
            "min_latency_ms": round(self.min_latency, 2) if self.min_latency != float('inf') else 0,
            "max_latency_ms": round(self.max_latency, 2),
            "latency_samples": len(self.latency_samples),
        }


# ── مدیریت بهینه‌سازها ────────────────────────────────────────────────────────
_optimizers: dict[str, GamingOptimizer] = {}


def get_optimizer(uuid: str, gaming_mode: bool = False, profile: str = "") -> GamingOptimizer:
    """دریافت یا ساخت بهینه‌ساز برای یک کانفیگ"""
    if uuid not in _optimizers:
        _optimizers[uuid] = GamingOptimizer(
            uuid=uuid,
            profile=profile or DEFAULT_GAMING_PROFILE,
            gaming_mode=gaming_mode,
        )
    opt = _optimizers[uuid]
    opt.gaming_mode = gaming_mode
    if profile:
        opt.profile = profile
    return opt


def remove_optimizer(uuid: str):
    """حذف بهینه‌ساز یک کانفیگ"""
    _optimizers.pop(uuid, None)


def get_all_optimizers() -> dict:
    """لیست تمام بهینه‌سازها"""
    return {uuid: opt.get_optimization_report() for uuid, opt in _optimizers.items()}


def get_gaming_profiles() -> dict:
    """لیست پروفایل‌های گیمینگ"""
    return GAMING_PROFILES
