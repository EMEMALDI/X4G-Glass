# X4G-Glass

## Premium Morph Glass UI/UX for X4G VPN Management Panel

A complete visual rebuild of the [X4G VPN management panel](https://github.com/x4gKing) with premium **Morph Glass** (Glassmorphism) design, while preserving 100% of the original backend functionality.

### What's New

- 🪟 **Morph Glass Design System** — Deep blur glass cards with edge light highlights, aurora backgrounds, and luminous borders
- 🎨 **Cyber Blue Theme** — Accent color `#00d4ff` with glow effects, animated background orbs
- ✨ **Premium Animations** — Smooth transitions, floating orbs, pulse animations, card hover effects
- 🌐 **Full RTL Support** — Complete right-to-left layout with Vazirmatn Persian font
- 📱 **Responsive Design** — Adapts from desktop to mobile with glass sidebar, collapsible menus

### Design System

| Element | Style |
|---------|-------|
| Background | `#0a0e1a` with aurora gradients |
| Glass Cards | `rgba(255,255,255,0.08)` + `blur(24px) saturate(180%)` |
| Borders | `1.5px solid rgba(255,255,255,0.18)` |
| Edge Light | `::before` gradient highlight |
| Accent | `#00d4ff` (Cyber Blue) |
| Success | `#00ff88` (Connected) |
| Error | `#ff4466` |
| Warning | `#ffaa00` |
| Font | Vazirmatn (Persian) from Google Fonts CDN |

### Files

| File | Description | Changed? |
|------|-------------|----------|
| `main.py` | FastAPI server, routes, auth, state management | ✅ Unchanged |
| `relay_vless.py` | WebSocket VLESS tunnel relay | ✅ Unchanged |
| `speed_limit.py` | Bandwidth throttling (Token Bucket) | ✅ Unchanged |
| `xhttp_siz10.py` | XHTTP Ultra transport (packet/stream-up) | ✅ Unchanged |
| `telegram_bot.py` | Telegram bot for remote management | ✅ Unchanged |
| `requirements.txt` | Python dependencies | ✅ Unchanged |
| `pages.py` | **UI/UX — Complete rewrite** | 🔄 New Glass Edition |

### Pages

1. **Login Page** (`/login`) — Centered glass card with aurora background, animated orbs, gradient login button with glow
2. **Dashboard** (`/dashboard`) — Full management panel with:
   - Glass sidebar navigation
   - Stats cards with edge light highlights
   - Traffic charts (Chart.js)
   - Links management (create/edit/delete/toggle/bulk)
   - Live connections monitoring
   - Activity & error logs
   - Settings (password change with strength meter)
3. **Public Sub Page** (`/p/{uuid}`) — Glass cards showing config info, QR codes, copy buttons

### Backend API Endpoints

All endpoints remain identical to X4G v9.8:

- `POST /api/login` — Password authentication
- `POST /api/logout` — Session destruction
- `GET /api/me` — Auth check
- `GET /stats` — Dashboard stats + hourly traffic
- `GET /api/links` — List all configs
- `POST /api/links` — Create config
- `PATCH /api/links/{uid}` — Update config
- `DELETE /api/links/{uid}` — Delete config
- `GET /api/connections` — Live connections
- `GET /api/activity` — Activity logs
- `POST /api/change-password` — Change password

### Quick Start

```bash
pip install -r requirements.txt
python main.py
```

### Credits

- **X4G** by [x4gKing](https://github.com/x4gKing)
- **Morph Glass** design inspired by glassmorphism, GlassKit, and VisoDesign
- **Vazirmatn** Persian font by [Saber Rastikerdar](https://github.com/rastikerdar/vazirmatn)
