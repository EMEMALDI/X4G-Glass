// ══════════════════════════════════════════════════════════════════════════════
// X4G-Glass Cloudflare Worker — FINAL PRODUCTION VERSION
// ══════════════════════════════════════════════════════════════════════════════
// Worker URL: https://restless-heart-cb0d.emem-32281.workers.dev
//
// ⚠️ فقط خط ORIGIN رو با آدرس Railway خودتون عوض کنید
// ══════════════════════════════════════════════════════════════════════════════

const ORIGIN = 'https://YOUR-RAILWAY-APP.up.railway.app';  // ← اینو عوض کنید

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // ── CORS ────────────────────────────────────────────────────────────────
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors() });
    }

    // ── Health Check ────────────────────────────────────────────────────────
    if (url.pathname === '/health') {
      return json({
        ok: true,
        worker: 'x4g-glass',
        version: '1.0',
        origin: ORIGIN !== 'https://YOUR-RAILWAY-APP.up.railway.app' ? 'configured' : 'NOT_SET',
        colo: request.cf?.colo || 'unknown',
        country: request.cf?.country || 'unknown',
        city: request.cf?.city || 'unknown',
        ip: request.headers.get('CF-Connecting-IP') || 'unknown',
        ts: new Date().toISOString(),
      });
    }

    // ── Stats ───────────────────────────────────────────────────────────────
    if (url.pathname === '/stats') {
      return json({
        worker: 'x4g-glass',
        origin: ORIGIN,
        cf: request.cf || {},
        headers: Object.fromEntries(request.headers),
      });
    }

    // ── WebSocket (VLESS WS / XHTTP) ───────────────────────────────────────
    if (request.headers.get('Upgrade') === 'websocket') {
      return handleWS(request, url);
    }

    // ── HTTP Proxy ──────────────────────────────────────────────────────────
    return handleHTTP(request, url);
  },
};

// ══════════════════════════════════════════════════════════════════════════════
// WebSocket Proxy
// ══════════════════════════════════════════════════════════════════════════════
async function handleWS(request, url) {
  try {
    const originWs = ORIGIN.replace(/^https/, 'wss') + url.pathname + url.search;
    const resp = await fetch(originWs, {
      headers: request.headers,
    });
    return resp;
  } catch (e) {
    return json({ error: 'ws_failed', detail: e.message }, 502);
  }
}

// ══════════════════════════════════════════════════════════════════════════════
// HTTP Proxy
// ══════════════════════════════════════════════════════════════════════════════
async function handleHTTP(request, url) {
  try {
    const target = new URL(ORIGIN + url.pathname + url.search);
    const headers = new Headers();

    // فوروارد IP واقعی
    const clientIP = request.headers.get('CF-Connecting-IP') || '';
    headers.set('X-Forwarded-For', clientIP);
    headers.set('X-Real-IP', clientIP);
    headers.set('X-Forwarded-Proto', 'https');

    // اطلاعات Edge
    if (request.cf?.colo) headers.set('X-CF-Colo', request.cf.colo);
    if (request.cf?.country) headers.set('X-CF-Country', request.cf.country);

    // Content-Type
    const ct = request.headers.get('Content-Type');
    if (ct) headers.set('Content-Type', ct);

    const resp = await fetch(target.toString(), {
      method: request.method,
      headers,
      body: request.body,
    });

    return new Response(resp.body, {
      status: resp.status,
      headers: resp.headers,
    });
  } catch (e) {
    return json({ error: 'origin_unreachable', detail: e.message }, 502);
  }
}

// ══════════════════════════════════════════════════════════════════════════════
// Helpers
// ══════════════════════════════════════════════════════════════════════════════
function cors() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': '*',
    'Access-Control-Allow-Headers': '*',
  };
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { 'Content-Type': 'application/json', ...cors() },
  });
}
