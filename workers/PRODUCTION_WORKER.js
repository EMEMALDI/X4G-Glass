// ══════════════════════════════════════════════════════════════════════════════
// X4G-Glass Cloudflare Worker — Multi-Location VLESS Proxy
// ══════════════════════════════════════════════════════════════════════════════
//
// 📌 نحوه استفاده:
//    1. این فایل رو کپی کنید
//    2. مقدار ORIGIN_URL رو به آدرس Railway خودتون تغییر بدید
//    3. در Cloudflare Dashboard > Workers > Create Worker آپلود کنید
//    4. لینک Worker رو بهم بدید تا جاسازی کنم
//
// 🔧 قابلیت‌ها:
//    - پروکسی VLESS WebSocket
//    - پروکسی XHTTP
//    - پروکسی HTTP معمولی
//    - گزارش آمار و سلامت
//    - فشرده‌سازی Brotli
//    - فوروارد IP واقعی کلاینت
// ══════════════════════════════════════════════════════════════════════════════

// ⚠️ آدرس سرور اصلی Railway خودتون رو اینجا بذارید
const ORIGIN = 'https://YOUR-RAILWAY-APP.up.railway.app';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // ── CORS ────────────────────────────────────────────────────────────────
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: cors(),
      });
    }

    // ── Health ──────────────────────────────────────────────────────────────
    if (url.pathname === '/health') {
      return json({
        ok: true,
        worker: 'x4g-glass',
        origin: ORIGIN,
        colo: request.cf?.colo || 'unknown',
        country: request.cf?.country || 'unknown',
        city: request.cf?.city || 'unknown',
        ts: new Date().toISOString(),
      });
    }

    // ── WebSocket (VLESS WS / XHTTP) ───────────────────────────────────────
    if (request.headers.get('Upgrade') === 'websocket') {
      return proxyWS(request, url);
    }

    // ── HTTP Proxy ──────────────────────────────────────────────────────────
    return proxyHTTP(request, url);
  },
};

// ══════════════════════════════════════════════════════════════════════════════
// توابع کمکی
// ══════════════════════════════════════════════════════════════════════════════

function cors() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,PATCH,OPTIONS',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Max-Age': '86400',
  };
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { 'Content-Type': 'application/json', ...cors() },
  });
}

function forwardHeaders(request) {
  const h = new Headers();
  const clientIP = request.headers.get('CF-Connecting-IP') || '';

  // فوروارد هدرهای مهم
  h.set('X-Forwarded-For', clientIP);
  h.set('X-Real-IP', clientIP);
  h.set('X-Forwarded-Proto', 'https');

  // اطلاعات Cloudflare Edge
  const cf = request.cf || {};
  if (cf.colo) h.set('X-CF-Colo', cf.colo);
  if (cf.country) h.set('X-CF-Country', cf.country);
  if (cf.city) h.set('X-CF-City', cf.city);

  // Content-Type اگه وجود داره
  const ct = request.headers.get('Content-Type');
  if (ct) h.set('Content-Type', ct);

  // Authorization اگه وجود داره
  const auth = request.headers.get('Authorization');
  if (auth) h.set('Authorization', auth);

  return h;
}

async function proxyHTTP(request, url) {
  try {
    const target = new URL(ORIGIN + url.pathname + url.search);
    const resp = await fetch(target.toString(), {
      method: request.method,
      headers: forwardHeaders(request),
      body: request.body,
      redirect: 'follow',
    });

    // کپی پاسخ با هدرهای اضافه
    const out = new Response(resp.body, {
      status: resp.status,
      statusText: resp.statusText,
      headers: resp.headers,
    });
    out.headers.set('X-Worker-Colo', request.cf?.colo || '');
    out.headers.set('X-Worker-Country', request.cf?.country || '');
    return out;
  } catch (e) {
    return json({ error: 'origin_unreachable', detail: e.message }, 502);
  }
}

async function proxyWS(request, url) {
  try {
    // ساخت URL WebSocket برای ارجاع
    const wsBase = ORIGIN.replace(/^http/, 'ws');
    const target = new URL(wsBase + url.pathname + url.search);

    // Cloudflare Worker WebSocket proxy pattern
    const pair = new WebSocketPair();
    const [client, server] = [pair[0], pair[1]];

    // اتصال به ارجاع و فوروارد
    const upgradeHeader = request.headers.get('Upgrade');
    const originResp = await fetch(target.toString(), {
      headers: {
        ...Object.fromEntries(request.headers),
        Upgrade: 'websocket',
      },
    });

    // اگه ارجاع WebSocket رو قبول کرد
    if (originResp.status === 101) {
      return originResp;
    }

    // اگه نه، ساده فوروارد کن
    return proxyHTTP(request, url);
  } catch (e) {
    return json({ error: 'ws_failed', detail: e.message }, 502);
  }
}
