# راهنمای دیپلوی Cloudflare Worker

## مراحل:

### ۱. آدرس Railway رو پیدا کنید
آدرس اپلیکیتون رو از Railway کپی کنید (مثلاً `https://myapp.up.railway.app`)

### ۲. Worker بسازید
1. برید به [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Workers & Pages > Create Application > Create Worker
3. یه اسم بذارید (مثلاً `x4g-glass`)
4. کد `PRODUCTION_WORKER.js` رو کپی-پیست کنید
5. خط `ORIGIN` رو به آدرس Railway خودتون تغییر بدید:
   ```js
   const ORIGIN = 'https://your-app.up.railway.app';
   ```
6. Deploy کنید

### ۳. لینک Worker رو کپی کنید
لینک Worker شما چیزی شبیه این هست:
```
https://x4g-glass.YOUR-SUBDOMAIN.workers.dev
```

### ۴. لینک رو بهم بدید
من لینک Worker رو در X4G-Glass جاسازی می‌کنم و فقط دیپلوی Railway باقی می‌مونه.

## تست:
بعد از دیپلوی، این آدرس رو باز کنید:
```
https://your-worker.workers.dev/health
```
باید چیزی شبیه این ببینید:
```json
{
  "ok": true,
  "worker": "x4g-glass",
  "colo": "LHR",
  "country": "GB"
}
```

## نکته:
- هر بار که لینک Worker رو تغییر بدید، باید دوباره بهم بدید تا آپدیت کنم
- Worker رایگان هست (Plan: Free)
- محدودیت: 100,000 درخواست رایگان در روز
