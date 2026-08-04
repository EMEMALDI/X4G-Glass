# subscribe_page.py
# صفحه ساب‌پیج عمومی — Glass Morphism Premium Design

SUBSCRIBE_PAGE_HTML = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>اشتراک · X4G Glass</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#060b18;--bg2:#0a1128;--bg3:#0f1a36;
  --accent:#00d4ff;--accent2:#0ea5e9;--accent-d:rgba(0,212,255,.08);
  --accent-glow:rgba(0,212,255,.25);
  --success:#00ff88;--success-d:rgba(0,255,136,.08);
  --danger:#ff4466;--danger-d:rgba(255,68,102,.08);
  --warning:#ffaa00;--warning-d:rgba(255,170,0,.08);
  --purple:#a855f7;--purple-d:rgba(168,85,247,.08);
  --gold:#ffd700;--gold-d:rgba(255,215,0,.08);
  --pink:#f472b6;--pink-d:rgba(244,114,182,.08);
  --t1:#eaf0ff;--t2:#7b8db5;--t3:#3d5078;
  --glass:rgba(255,255,255,.04);--glass-b:rgba(255,255,255,.08);--glass-h:rgba(255,255,255,.18);
  --radius:22px;--radius-sm:14px;
}
html{scroll-behavior:smooth}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--t1);min-height:100vh;overflow-x:hidden}

/* ═══ Aurora Background ═══ */
.aurora{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.aurora::before{content:'';position:absolute;top:-30%;left:-20%;width:70%;height:70%;background:radial-gradient(ellipse,rgba(0,150,255,.12) 0%,transparent 70%);animation:aurora1 20s ease-in-out infinite alternate}
.aurora::after{content:'';position:absolute;bottom:-20%;right:-15%;width:60%;height:60%;background:radial-gradient(ellipse,rgba(0,100,200,.08) 0%,transparent 70%);animation:aurora2 25s ease-in-out infinite alternate}
@keyframes aurora1{0%{transform:translate(0,0) scale(1)}100%{transform:translate(10%,15%) scale(1.2)}}
@keyframes aurora2{0%{transform:translate(0,0) scale(1)}100%{transform:translate(-10%,-10%) scale(1.15)}}

/* Floating Particles */
.particles{position:fixed;inset:0;z-index:1;pointer-events:none;overflow:hidden}
.particle{position:absolute;width:3px;height:3px;background:var(--accent);border-radius:50%;opacity:.3;animation:float linear infinite}
@keyframes float{0%{transform:translateY(100vh) scale(0);opacity:0}10%{opacity:.4}90%{opacity:.4}100%{transform:translateY(-10vh) scale(1);opacity:0}}

.container{position:relative;z-index:10;max-width:860px;margin:0 auto;padding:16px}

/* ═══ Header ═══ */
.header{text-align:center;padding:40px 0 24px;position:relative}
.logo-wrap{display:inline-flex;align-items:center;gap:14px;margin-bottom:20px;padding:12px 24px 12px 16px;background:var(--glass);backdrop-filter:blur(20px);border:1.5px solid var(--glass-b);border-radius:60px;transition:all .3s}
.logo-wrap:hover{border-color:var(--accent);box-shadow:0 0 30px var(--accent-glow)}
.logo-glow{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:80px;height:80px;background:radial-gradient(circle,var(--accent-glow),transparent 70%);border-radius:50%;filter:blur(20px);animation:logoPulse 3s ease-in-out infinite}
@keyframes logoPulse{0%,100%{opacity:.5;transform:translate(-50%,-50%) scale(1)}50%{opacity:.8;transform:translate(-50%,-50%) scale(1.2)}}
.logo-icon{width:44px;height:44px;border-radius:50%;overflow:hidden;border:2px solid var(--accent);position:relative;z-index:2;box-shadow:0 0 20px var(--accent-glow)}
.logo-icon img{width:100%;height:100%;object-fit:cover}
.logo-text{position:relative;z-index:2}
.logo-name{font-size:18px;font-weight:900;color:var(--t1);letter-spacing:-.02em}
.logo-sub{font-size:10px;color:var(--accent);font-weight:600;letter-spacing:.08em;text-transform:uppercase}

.hero-title{font-size:28px;font-weight:900;margin-bottom:8px;background:linear-gradient(135deg,var(--t1),var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.4}
.hero-sub{font-size:13px;color:var(--t2);line-height:1.8}

/* ═══ Stats ═══ */
.stats-row{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:24px 0}
.stat-card{background:var(--glass);backdrop-filter:blur(20px);border:1.5px solid var(--glass-b);border-radius:var(--radius-sm);padding:18px 16px;text-align:center;transition:all .3s;position:relative;overflow:hidden}
.stat-card::before{content:'';position:absolute;top:0;left:20%;right:20%;height:1px;background:linear-gradient(90deg,transparent,var(--glass-h),transparent)}
.stat-card:hover{border-color:var(--accent);transform:translateY(-2px);box-shadow:0 8px 32px rgba(0,0,0,.2)}
.stat-icon{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;font-size:16px}
.stat-icon.blue{background:var(--accent-d);color:var(--accent)}
.stat-icon.green{background:var(--success-d);color:var(--success)}
.stat-icon.purple{background:var(--purple-d);color:var(--purple)}
.stat-num{font-size:22px;font-weight:900;color:var(--t1);line-height:1}
.stat-label{font-size:10px;color:var(--t3);margin-top:4px;text-transform:uppercase;letter-spacing:.06em}

/* ═══ Filter Tabs ═══ */
.filter-row{display:flex;gap:8px;margin:20px 0;flex-wrap:wrap;justify-content:center}
.filter-btn{background:var(--glass);border:1.5px solid var(--glass-b);border-radius:12px;padding:8px 18px;font-size:12px;font-weight:600;color:var(--t2);cursor:pointer;transition:all .25s;font-family:inherit;display:inline-flex;align-items:center;gap:7px;user-select:none}
.filter-btn:hover{background:var(--accent-d);border-color:rgba(0,212,255,.25);color:var(--t1)}
.filter-btn.on{background:rgba(0,212,255,.12);border-color:var(--accent);color:var(--accent);box-shadow:0 0 16px var(--accent-glow)}
.filter-count{font-size:10px;background:rgba(0,212,255,.12);color:var(--accent);padding:2px 7px;border-radius:10px;font-weight:700}

/* ═══ Config Cards ═══ */
.configs{display:flex;flex-direction:column;gap:16px}
.cfg{position:relative;background:var(--glass);backdrop-filter:blur(24px) saturate(150%);-webkit-backdrop-filter:blur(24px) saturate(150%);border:1.5px solid var(--glass-b);border-radius:var(--radius);padding:0;transition:all .35s ease;overflow:hidden;animation:cardIn .4s ease both}
.cfg::before{content:'';position:absolute;top:0;left:8%;right:8%;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.25),transparent)}
.cfg::after{content:'';position:absolute;inset:0;border-radius:var(--radius);opacity:0;background:linear-gradient(135deg,rgba(0,212,255,.03),transparent 50%);transition:opacity .3s}
.cfg:hover{border-color:var(--glass-h);transform:translateY(-3px);box-shadow:0 16px 48px rgba(0,0,0,.3)}
.cfg:hover::after{opacity:1}
.cfg.off{opacity:.45}
.cfg-head{display:flex;align-items:center;justify-content:space-between;padding:18px 20px 0}
.cfg-name{font-size:16px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.cfg-tag{font-size:10px;padding:3px 10px;border-radius:20px;font-weight:700;display:inline-flex;align-items:center;gap:4px;letter-spacing:.02em}
.tag-gaming{background:var(--danger-d);color:var(--danger)}
.tag-streaming{background:var(--purple-d);color:var(--purple)}
.tag-browsing{background:var(--accent-d);color:var(--accent)}
.tag-social{background:var(--success-d);color:var(--success)}
.tag-download{background:var(--warning-d);color:var(--warning)}
.tag-vip{background:var(--gold-d);color:var(--gold)}
.tag-economy{background:var(--pink-d);color:var(--pink)}
.cfg-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.cfg-dot.on{background:var(--success);box-shadow:0 0 8px var(--success);animation:pulse 2s infinite}
.cfg-dot.off{background:var(--danger)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}

/* ═══ Info Grid ═══ */
.cfg-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;padding:16px 20px}
.cfg-cell{background:rgba(0,0,0,.25);border-radius:10px;padding:10px 12px;border:1px solid rgba(255,255,255,.03)}
.cfg-cell-label{font-size:9px;color:var(--t3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.cfg-cell-val{font-size:13px;font-weight:700;color:var(--t1)}

/* ═══ Progress ═══ */
.cfg-bar-wrap{padding:0 20px 14px}
.cfg-bar-hdr{display:flex;justify-content:space-between;margin-bottom:5px}
.cfg-bar-hdr span{font-size:10px;color:var(--t3)}
.cfg-bar{height:5px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden}
.cfg-bar-fill{height:100%;border-radius:3px;transition:width .5s ease}
.bar-ok{background:linear-gradient(90deg,#00cc88,var(--success))}
.bar-warn{background:linear-gradient(90deg,var(--warning),#ffcc44)}
.bar-danger{background:linear-gradient(90deg,var(--danger),#ff6688)}

/* ═══ Actions ═══ */
.cfg-actions{display:flex;gap:8px;padding:0 20px 18px;border-top:1px solid rgba(255,255,255,.04);padding-top:14px;margin-top:2px}
.abtn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:10px 20px;border-radius:12px;font-size:12px;font-weight:700;font-family:inherit;cursor:pointer;transition:all .25s;border:none;outline:none;position:relative;overflow:hidden}
.abtn::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,.1),transparent);opacity:0;transition:opacity .25s}
.abtn:hover::before{opacity:1}
.abtn:active{transform:scale(.96)}
.abtn-p{background:linear-gradient(135deg,#00d4ff,#0088cc);color:#fff;box-shadow:0 4px 16px rgba(0,212,255,.25)}
.abtn-p:hover{box-shadow:0 8px 28px rgba(0,212,255,.35);transform:translateY(-1px)}
.abtn-s{background:var(--glass);border:1.5px solid var(--glass-b);color:var(--t1)}
.abtn-s:hover{border-color:rgba(0,212,255,.3);color:var(--accent)}
.abtn-g{background:linear-gradient(135deg,var(--success),#00bb77);color:#060b18}
.abtn-r{background:linear-gradient(135deg,var(--danger),#cc3355);color:#fff}

/* ═══ Copy All ═══ */
.copy-all-wrap{text-align:center;margin:24px 0}
.copy-all-btn{display:inline-flex;align-items:center;gap:10px;padding:14px 36px;background:linear-gradient(135deg,var(--accent),#0088cc);color:#fff;border:none;border-radius:16px;font-size:14px;font-weight:800;font-family:inherit;cursor:pointer;box-shadow:0 8px 32px rgba(0,212,255,.3);transition:all .3s;position:relative;overflow:hidden}
.copy-all-btn::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:linear-gradient(45deg,transparent,rgba(255,255,255,.1),transparent);transform:rotate(45deg);animation:shimmer 3s infinite}
@keyframes shimmer{0%{transform:translateX(-100%) rotate(45deg)}100%{transform:translateX(100%) rotate(45deg)}}
.copy-all-btn:hover{transform:translateY(-2px);box-shadow:0 12px 40px rgba(0,212,255,.4)}

/* ═══ Toast ═══ */
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(20px);background:rgba(0,255,136,.12);backdrop-filter:blur(16px);border:1.5px solid rgba(0,255,136,.25);color:var(--success);padding:14px 28px;border-radius:16px;font-size:13px;font-weight:700;z-index:9999;opacity:0;transition:all .35s cubic-bezier(.4,0,.2,1);pointer-events:none;display:flex;align-items:center;gap:8px}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

/* ═══ Empty ═══ */
.empty{text-align:center;padding:60px 20px}
.empty-icon{font-size:48px;margin-bottom:16px;opacity:.3}
.empty-text{color:var(--t3);font-size:14px}

/* ═══ Footer ═══ */
.footer{text-align:center;padding:32px 0 20px;color:var(--t3);font-size:11px;line-height:2}
.footer a{color:var(--accent);text-decoration:none;font-weight:700}
.footer-brand{margin-top:8px;font-size:10px;letter-spacing:.08em;text-transform:uppercase}

/* ═══ Animations ═══ */
@keyframes cardIn{from{opacity:0;transform:translateY(16px) scale(.97)}to{opacity:1;transform:none}}

/* ═══ Scrollbar ═══ */
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--glass-h);border-radius:4px}

/* ═══ Mobile ═══ */
@media(max-width:600px){
  .stats-row{grid-template-columns:1fr}
  .cfg-grid{grid-template-columns:1fr 1fr}
  .cfg-actions{flex-direction:column}
  .abtn{width:100%}
  .hero-title{font-size:22px}
  .container{padding:10px}
}
</style>
</head>
<body>
<div class="aurora"></div>
<div class="particles" id="particles"></div>
<div class="container">

  <!-- Header -->
  <div class="header">
    <div class="logo-wrap">
      <div class="logo-glow"></div>
      <div class="logo-icon"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0%25' stop-color='%2300d4ff'/%3E%3Cstop offset='100%25' stop-color='%230088cc'/%3E%3C/linearGradient%3E%3C/defs%3E%3Ccircle cx='50' cy='50' r='46' fill='%23060b18' stroke='url(%23g)' stroke-width='2.5'/%3E%3Ctext x='50' y='62' text-anchor='middle' font-size='36' font-weight='900' fill='url(%23g)' font-family='sans-serif'%3EX4G%3C/text%3E%3C/svg%3E" alt="X4G"></div>
      <div class="logo-text">
        <div class="logo-name">X4G Glass</div>
        <div class="logo-sub">Premium VPN</div>
      </div>
    </div>
    <div class="hero-title">لینک‌های اشتراک شما</div>
    <div class="hero-sub">کانفیگ‌های فعال خود را مشاهده کنید · روی دکمه کپی بزنید</div>
  </div>

  <!-- Stats -->
  <div class="stats-row">
    <div class="stat-card">
      <div class="stat-icon blue"><i class="ti ti-link"></i></div>
      <div class="stat-num" id="s-total">0</div>
      <div class="stat-label">کانفیگ فعال</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon green"><i class="ti ti-device-gamepad"></i></div>
      <div class="stat-num" id="s-game">0</div>
      <div class="stat-label">گیمینگ</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon purple"><i class="ti ti-chart-line"></i></div>
      <div class="stat-num" id="s-traffic">0</div>
      <div class="stat-label">مصرف کل</div>
    </div>
  </div>

  <!-- Filters -->
  <div class="filter-row" id="filters"></div>

  <!-- Copy All -->
  <div class="copy-all-wrap" id="copy-all-wrap" style="display:none">
    <button class="copy-all-btn" onclick="copyAll()"><i class="ti ti-copy"></i> کپی همه لینک‌ها</button>
  </div>

  <!-- Configs -->
  <div class="configs" id="configs"></div>

  <!-- Footer -->
  <div class="footer">
    <div>پشتیبانی: <a href="https://t.me/X4GHUB" target="_blank">@X4GHUB</a></div>
    <div class="footer-brand">Powered by X4G Glass Edition</div>
  </div>
</div>
<div class="toast" id="toast"></div>

<script>
const TOKEN='__TOKEN__';
let allConfigs=[],activeFilter='all';

// Particles
(function(){const c=document.getElementById('particles');for(let i=0;i<30;i++){const p=document.createElement('div');p.className='particle';p.style.left=Math.random()*100+'%';p.style.animationDuration=(8+Math.random()*12)+'s';p.style.animationDelay=Math.random()*10+'s';p.style.width=p.style.height=(1.5+Math.random()*2.5)+'px';c.appendChild(p)}})();

function toast(m){const t=document.getElementById('toast');t.innerHTML='<i class="ti ti-circle-check"></i> '+m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2200)}
function fmtB(b){if(b<1024)return b+' B';if(b<1048576)return(b/1024).toFixed(1)+' KB';if(b<1073741824)return(b/1048576).toFixed(1)+' MB';return(b/1073741824).toFixed(2)+' GB'}
function esc(s){return(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function escJ(s){return(s||'').replace(/\\\\/g,'\\\\\\\\').replace(/'/g,"\\\\'")}

function tagClass(c){return{gaming:'tag-gaming',streaming:'tag-streaming',browsing:'tag-browsing',social:'tag-social',download:'tag-download',vip:'tag-vip',economy:'tag-economy'}[c]||'tag-browsing'}

function renderFilters(){
  const cats={};allConfigs.forEach(c=>{cats[c.category]=(cats[c.category]||0)+1});
  let h='<button class="filter-btn on" onclick="setFilter(this,\'all\')">همه<span class="filter-count">'+allConfigs.length+'</span></button>';
  for(const[k,v]of Object.entries(cats)){const lbl=allConfigs.find(c=>c.category===k)?.category_label||k;h+='<button class="filter-btn" onclick="setFilter(this,\''+k+'\')">'+lbl+'<span class="filter-count">'+v+'</span></button>'}
  document.getElementById('filters').innerHTML=h;
}

function setFilter(btn,cat){
  activeFilter=cat;
  document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');
  renderConfigs();
}

function renderConfigs(){
  const list=activeFilter==='all'?allConfigs:allConfigs.filter(c=>c.category===activeFilter);
  const el=document.getElementById('configs');
  const caw=document.getElementById('copy-all-wrap');
  caw.style.display=allConfigs.length>1?'block':'none';

  if(!list.length){el.innerHTML='<div class="empty"><div class="empty-icon"><i class="ti ti-folder-open"></i></div><div class="empty-text">کانفیگی یافت نشد</div></div>';return}

  el.innerHTML=list.map((c,i)=>{
    const pct=c.limit_bytes>0?Math.min(c.used_bytes/c.limit_bytes*100,100):0;
    const bc=pct>80?'bar-danger':pct>50?'bar-warn':'bar-ok';
    const exp=c.expires_at?new Date(c.expires_at).toLocaleDateString('fa-IR'):'∞';
    return`<div class="cfg${c.active?'':' off'}" style="animation-delay:${i*.06}s">
      <div class="cfg-head">
        <div class="cfg-name">
          <span class="cfg-dot ${c.active?'on':'off'}"></span>
          ${esc(c.label)}
          <span class="cfg-tag ${tagClass(c.category)}">${esc(c.category_label)}</span>
          ${c.gaming_mode?'<span class="cfg-tag tag-gaming">🎮 گیمینگ</span>':''}
          ${c.bandwidth_saver?'<span class="cfg-tag tag-economy">💰 صرفه‌جو</span>':''}
        </div>
      </div>
      <div class="cfg-grid">
        <div class="cfg-cell"><div class="cfg-cell-label">پروتکل</div><div class="cfg-cell-val">${esc(c.protocol)}</div></div>
        <div class="cfg-cell"><div class="cfg-cell-label">اتصال</div><div class="cfg-cell-val">${c.connections||0} نفر</div></div>
        <div class="cfg-cell"><div class="cfg-cell-label">مصرف</div><div class="cfg-cell-val">${c.used_fmt}</div></div>
        <div class="cfg-cell"><div class="cfg-cell-label">سقف</div><div class="cfg-cell-val">${c.limit_fmt}</div></div>
        <div class="cfg-cell"><div class="cfg-cell-label">انقضا</div><div class="cfg-cell-val">${exp}</div></div>
      </div>
      ${c.limit_bytes>0?`<div class="cfg-bar-wrap"><div class="cfg-bar-hdr"><span>مصرف حجم</span><span>${pct.toFixed(1)}%</span></div><div class="cfg-bar"><div class="cfg-bar-fill ${bc}" style="width:${pct}%"></div></div></div>`:''}
      <div class="cfg-actions">
        <button class="abtn abtn-p" onclick="copy('${escJ(c.vless_link)}')"><i class="ti ti-copy"></i> کپی VLESS</button>
        <button class="abtn abtn-s" onclick="copy('${escJ(c.sub_url)}')"><i class="ti ti-link"></i> لینک اشتراک</button>
      </div>
    </div>`}).join('');
}

function copy(t){navigator.clipboard.writeText(t).then(()=>toast('کپی شد ✓'))}
function copyAll(){const links=allConfigs.map(c=>c.vless_link).filter(Boolean).join('\\n');if(links)navigator.clipboard.writeText(links).then(()=>toast('همه '+allConfigs.length+' لینک کپی شد ✓'))}

async function loadData(){
  try{
    const r=await fetch('/api/subscribe/'+TOKEN);
    if(!r.ok)throw new Error();
    const d=await r.json();allConfigs=d.configs||[];
    document.getElementById('s-total').textContent=allConfigs.length;
    document.getElementById('s-game').textContent=allConfigs.filter(c=>c.gaming_mode).length;
    document.getElementById('s-traffic').textContent=fmtB(allConfigs.reduce((s,c)=>s+(c.used_bytes||0),0));
    renderFilters();renderConfigs();
  }catch(e){
    document.getElementById('configs').innerHTML='<div class="empty"><div class="empty-icon"><i class="ti ti-alert-circle"></i></div><div class="empty-text" style="color:var(--danger)">خطا در بارگذاری</div></div>';
  }
}
loadData();
</script>
</body>
</html>"""


def get_subscribe_page_html(token: str) -> str:
    """تولید HTML صفحه ساب‌پیج با توکن"""
    return SUBSCRIBE_PAGE_HTML.replace("__TOKEN__", token)
