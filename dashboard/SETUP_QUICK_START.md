# Quick Start Guide - Google OAuth Authentication

## ⚡ 5-Minute Setup

### 1. Get Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select project
3. APIs & Services → Credentials → Create OAuth 2.0 Client ID
4. Add origin: `http://localhost:3000`
5. Copy **Client ID**

### 2. Configure Dashboard

```bash
cd dashboard

# Copy environment template
cp .env.example .env

# Edit .env file
nano .env
```

Add your Google Client ID:
```bash
NUXT_PUBLIC_API_URL=http://localhost:8000
NUXT_PUBLIC_GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
NUXT_PUBLIC_ENV=development
```

### 3. Install & Run

```bash
# Install dependencies
pnpm install

# Start dev server
pnpm dev
```

Dashboard: http://localhost:3000

### 4. Verify Backend is Running

Make sure your backend is running at `http://localhost:8000`

```bash
cd ../backend
# Follow backend setup instructions
```

### 5. Test Login

1. Open http://localhost:3000
2. You'll be redirected to `/login`
3. Click "Продолжить с Google"
4. Authenticate with Google
5. Complete onboarding
6. Welcome to your dashboard! 🎉

---

## 🔑 Key Features

- ✅ Google OAuth login
- ✅ Automatic session restore
- ✅ Protected routes
- ✅ CSRF protection
- ✅ Token auto-refresh
- ✅ Logout (single device)
- ✅ Logout all devices
- ✅ Remember me (30 days)

---

## 📚 Full Documentation

For detailed documentation, see [AUTHENTICATION.md](./AUTHENTICATION.md)

## 🐛 Quick Troubleshooting

**Login button doesn't work?**
- Check browser console for errors
- Verify Google Client ID is correct
- Check backend is running

**Redirected to login after refresh?**
- Check backend is running
- Verify cookies are enabled
- Check CORS settings in backend

**CSRF token error?**
- Backend Redis must be running
- Check backend CSRF configuration

---

## 📝 Environment Variables Checklist

- [ ] `NUXT_PUBLIC_API_URL` - Backend API URL
- [ ] `NUXT_PUBLIC_GOOGLE_CLIENT_ID` - From Google Cloud Console
- [ ] Backend is configured with same Google Client ID
- [ ] Backend ALLOWED_ORIGINS includes dashboard URL

---

**Need help?** Check [AUTHENTICATION.md](./AUTHENTICATION.md) for detailed documentation.
