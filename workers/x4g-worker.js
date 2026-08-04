// X4G-Glass Cloudflare Worker - Multi-Location Proxy
// این Worker ترافیک VLESS/XHTTP رو از Cloudflare Edge به سرور اصلی پروکسی می‌کنه
// هر Worker می‌تونه به یه منطقه جغرافیایی مختلف دیپلوی بشه

const CONFIG = {
  // آدرس سرور اصلی X4G-Glass
  ORIGIN_URL: 'https://YOUR_X4GGLASS_URL.railway.app',
  
  // تنظیمات منطقه
  REGION: 'auto', // auto, wnam, enam, weur, eeur, apac, oc
  
  // فعال‌سازی حالت گیمینگ (کاهش لیتنسی)
  GAMING_MODE: false,
  
  // فشرده‌سازی پاسخ
  COMPRESS_RESPONSE: true,
  
  // کش پاسخ‌ها (ثانیه)
  CACHE_TTL: 0, // 0 = بدون کش برای ترافیک زنده
  
  // محدودیت اتصال
  MAX_CONNECTIONS: 1000,
  TIMEOUT_SECONDS: 300,
};

// ── لاگ وضعیت ──────────────────────────────────────────────────────────────
let stats = {
  totalRequests: 0,
  totalBytes: 0,
  activeConnections: 0,
  errors: 0,
  startTime: Date.now(),
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // ── CORS Headers ────────────────────────────────────────────────────────
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Region',
      'Access-Control-Max-Age': '86400',
    };
    
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders });
    }
    
    // ── Health Check ────────────────────────────────────────────────────────
    if (path === '/health' || path === '/') {
      return new Response(JSON.stringify({
        status: 'ok',
        region: CONFIG.REGION,
        origin: CONFIG.ORIGIN_URL,
        uptime: Math.floor((Date.now() - stats.startTime) / 1000),
        stats: {
          requests: stats.totalRequests,
          bytes: stats.totalBytes,
          errors: stats.errors,
        },
      }), {
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders,
        },
      });
    }
    
    // ── Stats ───────────────────────────────────────────────────────────────
    if (path === '/stats') {
      return new Response(JSON.stringify({
        region: CONFIG.REGION,
        config: {
          origin: CONFIG.ORIGIN_URL,
          gaming_mode: CONFIG.GAMING_MODE,
          compress: CONFIG.COMPRESS_RESPONSE,
        },
        stats: {
          ...stats,
          uptime: Math.floor((Date.now() - stats.startTime) / 1000),
          requestsPerSecond: stats.totalRequests / Math.max(1, (Date.now() - stats.startTime) / 1000),
        },
      }), {
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders,
        },
      });
    }
    
    // ── WebSocket Proxy (VLESS WS) ─────────────────────────────────────────
    const upgradeHeader = request.headers.get('Upgrade');
    if (upgradeHeader === 'websocket') {
      return this.handleWebSocket(request, ctx);
    }
    
    // ── HTTP Proxy ──────────────────────────────────────────────────────────
    stats.totalRequests++;
    
    try {
      const originUrl = new URL(CONFIG.ORIGIN_URL + path + url.search);
      
      // کپی هدرها
      const headers = new Headers(request.headers);
      headers.set('Host', originUrl.host);
      headers.set('X-Forwarded-For', request.headers.get('CF-Connecting-IP') || 'unknown');
      headers.set('X-Forwarded-Proto', 'https');
      headers.set('X-Real-IP', request.headers.get('CF-Connecting-IP') || 'unknown');
      
      // حذف هدرهای غیرضروری
      headers.delete('CF-Connecting-IP');
      headers.delete('CF-IPCountry');
      headers.delete('CF-Ray');
      headers.delete('CF-Visitor');
      
      // اضافه کردن اطلاعات منطقه
      headers.set('X-Worker-Region', CONFIG.REGION);
      headers.set('X-Worker-Edge', request.cf?.colo || 'unknown');
      headers.set('X-Worker-Country', request.cf?.country || 'unknown');
      
      const originRequest = new Request(originUrl.toString(), {
        method: request.method,
        headers: headers,
        body: request.body,
        redirect: 'follow',
      });
      
      const response = await fetch(originRequest);
      
      // کپی پاسخ
      const responseHeaders = new Headers(response.headers);
      responseHeaders.set('X-Origin-Region', CONFIG.REGION);
      responseHeaders.set('X-Origin-Edge', request.cf?.colo || 'unknown');
      
      // فشرده‌سازی اگه فعال باشه
      if (CONFIG.COMPRESS_RESPONSE && response.headers.get('Content-Type')?.includes('text')) {
        responseHeaders.set('Content-Encoding', 'br');
      }
      
      stats.totalBytes += parseInt(response.headers.get('Content-Length') || '0');
      
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: responseHeaders,
      });
      
    } catch (error) {
      stats.errors++;
      return new Response(JSON.stringify({
        error: 'Origin server unreachable',
        region: CONFIG.REGION,
        message: error.message,
      }), {
        status: 502,
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders,
        },
      });
    }
  },
  
  // ── WebSocket Handler ─────────────────────────────────────────────────────
  async handleWebSocket(request, ctx) {
    const url = new URL(request.url);
    const originUrl = new URL(CONFIG.ORIGIN_URL + url.pathname + url.search);
    
    // اتصال WebSocket به سرور اصلی
    const originWsUrl = originUrl.toString().replace('https:', 'wss:');
    
    try {
      const originResponse = await fetch(originUrl.toString(), {
        headers: {
          ...Object.fromEntries(request.headers),
          'Upgrade': 'websocket',
          'X-Worker-Region': CONFIG.REGION,
          'X-Worker-Edge': request.cf?.colo || 'unknown',
        },
      });
      
      // اگه سرور اصلی WebSocket رو قبول کرد
      if (originResponse.status === 101) {
        return originResponse;
      }
      
      // اگه WebSocket upgrade رد شد
      return new Response('WebSocket upgrade failed', { status: 400 });
      
    } catch (error) {
      stats.errors++;
      return new Response(JSON.stringify({
        error: 'WebSocket connection failed',
        region: CONFIG.REGION,
        message: error.message,
      }), {
        status: 502,
        headers: { 'Content-Type': 'application/json' },
      });
    }
  },
};
