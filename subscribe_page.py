# subscribe_page.py
# صفحه ساب‌پیج عمومی - Glass UI Design

SUBSCRIBE_PAGE_HTML = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>اشتراک · X4G Glass</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0a0e1a;--bg2:#0f1629;--bg3:#141d33;
  --accent:#00d4ff;--accent2:#00e5ff;--accent-d:rgba(0,212,255,.10);
  --success:#00ff88;--success-bg:rgba(0,255,136,.10);
  --danger:#ff4466;--danger-bg:rgba(255,68,102,.10);
  --warning:#ffaa00;--warning-bg:rgba(255,170,0,.10);
  --purple:#a855f7;--purple-bg:rgba(168,85,247,.10);
  --gold:#ffd700;--gold-bg:rgba(255,215,0,.10);
  --t1:#e8edf5;--t2:#7a8ba8;--t3:#4a5a74;
  --glass:rgba(255,255,255,.06);--glass-b:rgba(255,255,255,.12);--glass-bh:rgba(255,255,255,.25);
  --radius:20px;--radius-sm:14px;
}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--t1);min-height:100vh;padding:20px}
.aurora{position:fixed;inset:0;z-index:0;pointer-events:none;background:radial-gradient(ellipse at 20% 40%,rgba(0,150,255,.15) 0%,transparent 55%),radial-gradient(ellipse at 80% 65%,rgba(0,100,200,.10) 0%,transparent 50%),radial-gradient(ellipse at 50% 20%,rgba(0,212,255,.12) 0%,transparent 50%),linear-gradient(170deg,#0a1628 0%,#0d1f3c 50%,#060e1a 100%)}

.container{position:relative;z-index:10;max-width:800px;margin:0 auto}

/* Header */
.header{text-align:center;padding:30px 0 20px}
.logo{display:inline-flex;align-items:center;gap:12px;margin-bottom:16px}
.logo-img{width:48px;height:48px;border-radius:50%;overflow:hidden;border:2px solid var(--accent);box-shadow:0 0 24px rgba(0,212,255,.3)}
.logo-img img{width:100%;height:100%;object-fit:cover}
.logo-name{font-size:20px;font-weight:800;color:var(--t1)}
.logo-sub{font-size:11px;color:var(--t3)}
h1{font-size:22px;font-weight:800;color:var(--t1);margin-bottom:6px}
.subtitle{font-size:13px;color:var(--t2);line-height:1.7}

/* Stats Bar */
.stats-bar{display:flex;gap:12px;margin:20px 0;flex-wrap:wrap;justify-content:center}
.stat-item{background:var(--glass);backdrop-filter:blur(20px);border:1px solid var(--glass-b);border-radius:12px;padding:12px 18px;display:flex;align-items:center;gap:8px;min-width:140px}
.stat-icon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px}
.stat-icon.blue{background:var(--accent-d);color:var(--accent)}
.stat-icon.green{background:var(--success-bg);color:var(--success)}
.stat-icon.purple{background:var(--purple-bg);color:var(--purple)}
.stat-val{font-size:18px;font-weight:700;color:var(--t1)}
.stat-label{font-size:10px;color:var(--t3);text-transform:uppercase;letter-spacing:.05em}

/* Filter Tabs */
.filter-tabs{display:flex;gap:8px;margin:20px 0;flex-wrap:wrap;justify-content:center}
.filter-tab{background:var(--glass);border:1.5px solid var(--glass-b);border-radius:10px;padding:8px 16px;font-size:12px;font-weight:600;color:var(--t2);cursor:pointer;transition:all .2s;font-family:inherit;display:flex;align-items:center;gap:6px}
.filter-tab:hover{background:var(--accent-d);border-color:rgba(0,212,255,.3);color:var(--t1)}
.filter-tab.active{background:rgba(0,212,255,.15);border-color:var(--accent);color:var(--accent);box-shadow:0 0 12px rgba(0,212,255,.15)}
.filter-count{background:rgba(0,212,255,.15);color:var(--accent);font-size:10px;padding:2px 6px;border-radius:10px}

/* Config Cards */
.configs{display:flex;flex-direction:column;gap:14px}
.config-card{position:relative;background:var(--glass);backdrop-filter:blur(24px) saturate(180%);-webkit-backdrop-filter:blur(24px) saturate(180%);border:1.5px solid var(--glass-b);border-radius:var(--radius);padding:20px;transition:all .3s ease;overflow:hidden}
.config-card::before{content:'';position:absolute;top:0;left:10%;right:10%;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent)}
.config-card:hover{border-color:var(--glass-bh);transform:translateY(-2px);box-shadow:0 12px 40px rgba(0,0,0,.25)}
.config-card.disabled{opacity:.5;pointer-events:none}

.config-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.config-title{display:flex;align-items:center;gap:10px}
.config-name{font-size:15px;font-weight:700;color:var(--t1)}
.config-badge{font-size:10px;padding:3px 10px;border-radius:20px;font-weight:600;display:inline-flex;align-items:center;gap:4px}
.badge-gaming{background:var(--danger-bg);color:var(--danger)}
.badge-streaming{background:var(--purple-bg);color:var(--purple)}
.badge-browsing{background:var(--accent-d);color:var(--accent)}
.badge-social{background:var(--success-bg);color:var(--success)}
.badge-download{background:var(--warning-bg);color:var(--warning)}
.badge-vip{background:var(--gold-bg);color:var(--gold)}
.badge-economy{background:rgba(0,204,136,.1);color:#00cc88}

.config-status{display:flex;align-items:center;gap:6px}
.status-dot{width:8px;height:8px;border-radius:50%;background:var(--success);animation:pulse 2s infinite}
.status-text{font-size:11px;color:var(--success)}

/* Info Grid */
.info-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:14px}
.info-item{background:rgba(0,0,0,.2);border-radius:10px;padding:10px 12px}
.info-label{font-size:10px;color:var(--t3);margin-bottom:4px;text-transform:uppercase;letter-spacing:.05em}
.info-value{font-size:13px;font-weight:600;color:var(--t1)}

/* Progress Bar */
.progress-wrap{margin-bottom:14px}
.progress-header{display:flex;justify-content:space-between;margin-bottom:6px}
.progress-label{font-size:10px;color:var(--t3)}
.progress-bar{height:6px;background:rgba(255,255,255,.08);border-radius:3px;overflow:hidden}
.progress-fill{height:100%;border-radius:3px;transition:width .3s}
.progress-fill.green{background:linear-gradient(90deg,#00cc88,var(--success))}
.progress-fill.yellow{background:linear-gradient(90deg,var(--warning),#ffcc44)}
.progress-fill.red{background:linear-gradient(90deg,var(--danger),#ff6688)}

/* Action Buttons */
.config-actions{display:flex;gap:8px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:10px 18px;border-radius:12px;font-size:12px;font-weight:600;font-family:inherit;cursor:pointer;transition:all .2s;border:none;outline:none}
.btn-primary{background:linear-gradient(135deg,#00d4ff,#0099cc);color:#fff;box-shadow:0 4px 16px rgba(0,212,255,.3)}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,212,255,.4)}
.btn-secondary{background:var(--glass);border:1.5px solid var(--glass-b);color:var(--t1)}
.btn-secondary:hover{background:var(--accent-d);border-color:rgba(0,212,255,.3)}
.btn-success{background:linear-gradient(135deg,var(--success),#00cc88);color:#0a0e1a}
.btn-danger{background:linear-gradient(135deg,var(--danger),#cc3355);color:#fff}
.btn:active{transform:scale(.97)}

/* Toast */
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:rgba(0,255,136,.15);border:1px solid rgba(0,255,136,.3);color:var(--success);padding:12px 24px;border-radius:12px;font-size:13px;font-weight:600;z-index:1000;opacity:0;transition:opacity .3s;pointer-events:none}
.toast.show{opacity:1}

/* Footer */
.footer{text-align:center;padding:30px 0;color:var(--t3);font-size:11px}
.footer a{color:var(--accent);text-decoration:none;font-weight:600}

/* Animations */
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.config-card{animation:fadeIn .3s ease both}

/* Mobile */
@media(max-width:600px){
  .stats-bar{flex-direction:column;align-items:stretch}
  .stat-item{min-width:auto}
  .info-grid{grid-template-columns:1fr 1fr}
  .config-actions{flex-direction:column}
  .btn{width:100%}
}
</style>
</head>
<body>
<div class="aurora"></div>
<div class="container">
  <div class="header">
    <div class="logo">
      <div class="logo-img"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='45' fill='%230a0e1a' stroke='%2300d4ff' stroke-width='3'/%3E%3Ctext x='50' y='65' text-anchor='middle' font-size='40' font-weight='bold' fill='%2300d4ff'%3EX4G%3C/text%3E%3C/svg%3E" alt="X4G"></div>
      <div><div class="logo-name">X4G Glass</div><div class="logo-sub">Premium VPN Service</div></div>
    </div>
    <h1>🔗 لینک‌های اشتراک شما</h1>
    <p class="subtitle">کانفیگ‌های فعال خود را مشاهده و مدیریت کنید</p>
  </div>

  <div class="stats-bar" id="stats">
    <div class="stat-item"><div class="stat-icon blue"><i class="ti ti-link"></i></div><div><div class="stat-val" id="total-configs">0</div><div class="stat-label">کانفیگ فعال</div></div></div>
    <div class="stat-item"><div class="stat-icon green"><i class="ti ti-device-gamepad"></i></div><div><div class="stat-val" id="total-gaming">0</div><div class="stat-label">گیمینگ</div></div></div>
    <div class="stat-item"><div class="stat-icon purple"><i class="ti ti-chart-line"></i></div><div><div class="stat-val" id="total-traffic">0 MB</div><div class="stat-label">مصرف کل</div></div></div>
  </div>

  <div class="filter-tabs" id="filters"></div>
  <div class="configs" id="configs"></div>

  <div class="footer">
    <p>پشتیبانی: <a href="https://t.me/X4GHUB" target="_blank">@X4GHUB</a></p>
    <p style="margin-top:8px">Powered by X4G Glass Edition</p>
  </div>
</div>
<div class="toast" id="toast"></div>

<script>
const TOKEN = '__TOKEN__';
let allConfigs = [];
let activeFilter = 'all';

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => showToast('✅ کپی شد!'));
}

function fmtBytes(b) {
  if (b < 1024) return b + ' B';
  if (b < 1024*1024) return (b/1024).toFixed(1) + ' KB';
  if (b < 1024*1024*1024) return (b/1024/1024).toFixed(2) + ' MB';
  return (b/1024/1024/1024).toFixed(2) + ' GB';
}

function getBadgeClass(cat) {
  const map = {gaming:'badge-gaming',streaming:'badge-streaming',browsing:'badge-browsing',social:'badge-social',download:'badge-download',vip:'badge-vip',economy:'badge-economy'};
  return map[cat] || 'badge-browsing';
}

function getProgressClass(used, limit) {
  if (limit === 0) return 'green';
  const pct = (used / limit) * 100;
  if (pct > 80) return 'red';
  if (pct > 50) return 'yellow';
  return 'green';
}

function renderFilters() {
  const cats = {};
  allConfigs.forEach(c => {
    cats[c.category] = (cats[c.category] || 0) + 1;
  });
  const el = document.getElementById('filters');
  let html = `<button class="filter-tab active" onclick="setFilter('all')">همه<span class="filter-count">${allConfigs.length}</span></button>`;
  for (const [cat, count] of Object.entries(cats)) {
    const label = allConfigs.find(c => c.category === cat)?.category_label || cat;
    html += `<button class="filter-tab" onclick="setFilter('${cat}')">${label}<span class="filter-count">${count}</span></button>`;
  }
  el.innerHTML = html;
}

function setFilter(cat) {
  activeFilter = cat;
  document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
  event.target.closest('.filter-tab').classList.add('active');
  renderConfigs();
}

function renderConfigs() {
  const configs = activeFilter === 'all' ? allConfigs : allConfigs.filter(c => c.category === activeFilter);
  const el = document.getElementById('configs');

  if (configs.length === 0) {
    el.innerHTML = `<div class="config-card" style="text-align:center"><p style="color:var(--t3);padding:20px">کانفیگی یافت نشد</p></div>`;
    return;
  }

  el.innerHTML = configs.map((c, i) => {
    const progressPct = c.limit_bytes > 0 ? Math.min((c.used_bytes / c.limit_bytes) * 100, 100) : 0;
    const progressClass = getProgressClass(c.used_bytes, c.limit_bytes);
    const expiry = c.expires_at ? new Date(c.expires_at).toLocaleDateString('fa-IR') : 'نامحدود';

    return `
    <div class="config-card ${c.active ? '' : 'disabled'}" style="animation-delay:${i*0.05}s">
      <div class="config-header">
        <div class="config-title">
          <span class="config-name">${escHtml(c.label)}</span>
          <span class="config-badge ${getBadgeClass(c.category)}">${escHtml(c.category_label)}</span>
          ${c.gaming_mode ? '<span class="config-badge badge-gaming">🎮 گیمینگ</span>' : ''}
          ${c.bandwidth_saver ? '<span class="config-badge badge-economy">💰 صرفه‌جو</span>' : ''}
        </div>
        <div class="config-status">
          <span class="status-dot"></span>
          <span class="status-text">فعال</span>
        </div>
      </div>

      <div class="info-grid">
        <div class="info-item"><div class="info-label">پروتکل</div><div class="info-value">${escHtml(c.protocol.toUpperCase())}</div></div>
        <div class="info-item"><div class="info-label">اتصالات</div><div class="info-value">${c.connections} نفر</div></div>
        <div class="info-item"><div class="info-label">مصرف</div><div class="info-value">${c.used_fmt}</div></div>
        <div class="info-item"><div class="info-label">سقف</div><div class="info-value">${c.limit_fmt}</div></div>
        <div class="info-item"><div class="info-label">انقضا</div><div class="info-value">${expiry}</div></div>
      </div>

      ${c.limit_bytes > 0 ? `
      <div class="progress-wrap">
        <div class="progress-header"><span class="progress-label">مصرف حجم</span><span class="progress-label">${progressPct.toFixed(1)}%</span></div>
        <div class="progress-bar"><div class="progress-fill ${progressClass}" style="width:${progressPct}%"></div></div>
      </div>` : ''}

      <div class="config-actions">
        <button class="btn btn-primary" onclick="copyToClipboard('${escJs(c.vless_link)}')"><i class="ti ti-copy"></i> کپی لینک VLESS</button>
        <button class="btn btn-secondary" onclick="copyToClipboard('${escJs(c.sub_url)}')"><i class="ti ti-link"></i> کپی لینک اشتراک</button>
      </div>
    </div>`;
  }).join('');
}

function escHtml(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function escJs(s) { return (s||'').replace(/\\/g,'\\\\').replace(/'/g,"\\\\'"); }

async function loadData() {
  try {
    const r = await fetch('/api/subscribe/' + TOKEN);
    if (!r.ok) throw new Error('خطا');
    const data = await r.json();
    allConfigs = data.configs || [];

    document.getElementById('total-configs').textContent = allConfigs.length;
    document.getElementById('total-gaming').textContent = allConfigs.filter(c => c.gaming_mode).length;
    const totalBytes = allConfigs.reduce((s,c) => s + (c.used_bytes||0), 0);
    document.getElementById('total-traffic').textContent = fmtBytes(totalBytes);

    renderFilters();
    renderConfigs();
  } catch(e) {
    document.getElementById('configs').innerHTML = `<div class="config-card" style="text-align:center"><p style="color:var(--danger);padding:20px">خطا در بارگذاری داده‌ها</p></div>`;
  }
}

loadData();
</script>
</body>
</html>"""


def get_subscribe_page_html(token: str) -> str:
    """تولید HTML صفحه ساب‌پیج با توکن"""
    return SUBSCRIBE_PAGE_HTML.replace("__TOKEN__", token)
