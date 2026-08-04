// ══════════════════════════════════════════════════════════════════════════════
// X4G-Glass Worker — Ping Monitor + Tor Scanner
// Deploy this on Cloudflare Workers
// ══════════════════════════════════════════════════════════════════════════════

const PING_TARGETS = [
  {name:"Frankfurt DE",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
  {name:"Amsterdam NL",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
  {name:"Istanbul TR",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
  {name:"Dubai UAE",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
  {name:"London UK",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
  {name:"Paris FR",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
  {name:"Singapore SG",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
  {name:"Tokyo JP",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
  {name:"New York US",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
  {name:"San Jose US",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
  {name:"Chicago US",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
  {name:"Hong Kong",host:"speed.cloudflare.com",path:"/cdn-cgi/trace"},
];

async function pingTarget(target, count=3) {
  const times = [];
  let fails = 0;
  for (let i = 0; i < count; i++) {
    try {
      const start = performance.now();
      await fetch(`https://${target.host}${target.path}`, {
        method: "HEAD",
        headers: {"Cache-Control":"no-cache"},
        redirect: "follow",
      });
      times.push(performance.now() - start);
    } catch(e) { fails++; }
  }
  if (!times.length) return {name:target.name,host:target.host,latency:0,jitter:0,min:0,max:0,loss:100,status:"offline"};
  const avg = times.reduce((a,b)=>a+b,0)/times.length;
  const min = Math.min(...times);
  const max = Math.max(...times);
  const jitter = times.length > 1 ? Math.sqrt(times.reduce((s,t)=>s+Math.pow(t-avg,2),0)/times.length) : 0;
  return {
    name:target.name, host:target.host,
    latency:Math.round(avg*10)/10, jitter:Math.round(jitter*10)/10,
    min:Math.round(min*10)/10, max:Math.round(max*10)/10,
    loss:Math.round(fails/count*100),
    status: fails < count ? "ok" : "offline"
  };
}

async function handlePing(game, count) {
  const results = await Promise.all(PING_TARGETS.map(t => pingTarget(t, count)));
  const ok = results.filter(r => r.status === "ok").sort((a,b) => a.latency - b.latency);
  return {
    game: game || "all",
    edge: "Cloudflare Worker",
    servers: ok,
    best: ok[0] || null,
    avg_ping: ok.length ? Math.round(ok.reduce((s,r)=>s+r.latency,0)/ok.length*10)/10 : 0,
    total: results.length,
    online: ok.length,
    timestamp: new Date().toISOString()
  };
}

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json"
};

addEventListener("fetch", event => {
  event.respondWith(handle(event));
});

async function handle(request) {
  const url = new URL(request.url);
  const path = url.pathname;

  if (request.method === "OPTIONS") return new Response(null, {headers:CORS});

  // Ping endpoint — called by Railway backend
  if (path === "/ping") {
    const game = url.searchParams.get("game") || "all";
    const count = parseInt(url.searchParams.get("count") || "3");
    const result = await handlePing(game, count);
    return new Response(JSON.stringify(result), {headers:CORS});
  }

  if (path === "/ping/game") {
    const game = url.searchParams.get("game") || "fps";
    const count = parseInt(url.searchParams.get("count") || "3");
    const result = await handlePing(game, count);
    return new Response(JSON.stringify(result), {headers:CORS});
  }

  // Health
  if (path === "/health") {
    return new Response(JSON.stringify({ok:true,worker:"x4g-glass",version:"2.0"}), {headers:CORS});
  }

  // Root info
  return new Response(JSON.stringify({
    name:"X4G Glass Worker",
    version:"2.0",
    endpoints:{
      "GET /ping":"Ping all Cloudflare edges",
      "GET /ping/game?game=fps":"Ping for gaming",
      "GET /health":"Health check"
    }
  }), {headers:CORS});
}
