# Authentication System Documentation

Production-ready Google OAuth authentication system for MuscleUp Vision Dashboard.

## 🔐 Security Features

This implementation follows security best practices from the backend:

- ✅ **Google OAuth 2.0** - No password storage, delegated authentication
- ✅ **HttpOnly Cookies** - Tokens stored in secure cookies (XSS protection)
- ✅ **CSRF Protection** - One-time CSRF tokens for state-changing operations
- ✅ **Token Rotation** - Refresh tokens rotated on every refresh
- ✅ **Automatic Token Refresh** - Seamless session extension
- ✅ **SameSite Cookies** - CSRF attack prevention
- ✅ **Secure Cookies** - HTTPS-only in production
- ✅ **Protected Routes** - Middleware-based route protection
- ✅ **Session Restore** - Persistent sessions across page refreshes
- ✅ **Multi-device Logout** - Revoke all sessions capability

---

## 📋 Prerequisites

1. **Backend API Running**
   - MuscleUp Vision API must be running at configured URL
   - Default: `http://localhost:8000`

2. **Google OAuth Credentials**
   - Create a project in [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Add authorized redirect URIs

---

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```bash
cd dashboard
pnpm install
```

### Step 2: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and fill in your configuration:

```bash
# Backend API URL
NUXT_PUBLIC_API_URL=http://localhost:8000

# Google OAuth Client ID
NUXT_PUBLIC_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com

# Environment (development or production)
NUXT_PUBLIC_ENV=development
```

### Step 3: Configure Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Navigate to "APIs & Services" > "Credentials"
4. Click "Create Credentials" > "OAuth 2.0 Client ID"
5. Configure consent screen if prompted
6. Select "Web application" as application type
7. Add authorized JavaScript origins:
   - `http://localhost:3000` (development)
   - Your production domain (production)
8. Add authorized redirect URIs:
   - `http://localhost:3000` (development)
   - Your production domain (production)
9. Copy the **Client ID** and paste it in your `.env` file

### Step 4: Start Development Server

```bash
pnpm dev
```

The dashboard will be available at `http://localhost:3000`

---

## 🏗️ Architecture Overview

### Authentication Flow

```
┌─────────────┐
│   User      │
│  /login     │
└──────┬──────┘
       │
       │ 1. Click "Login with Google"
       ▼
┌─────────────────────────┐
│  Google OAuth Popup     │
│  (Google's servers)     │
└──────┬──────────────────┘
       │
       │ 2. User authenticates
       │ 3. Google returns ID token
       ▼
┌─────────────────────────┐
│  Dashboard (Frontend)   │
│  - Fetch CSRF token     │
│  - Send ID token + CSRF │
└──────┬──────────────────┘
       │
       │ 4. POST /api/v1/auth/login/oauth
       ▼
┌─────────────────────────┐
│  Backend API            │
│  - Verify Google token  │
│  - Create/find user     │
│  - Generate JWT tokens  │
│  - Set HttpOnly cookies │
└──────┬──────────────────┘
       │
       │ 5. Return user data
       │ 6. Set cookies (access_token, refresh_token)
       ▼
┌─────────────────────────┐
│  Dashboard              │
│  - Store user in Pinia  │
│  - Redirect to home/    │
│    onboarding           │
└─────────────────────────┘
```

### Token Management

**Access Token:**
- Lifetime: 30 minutes
- Storage: HttpOnly cookie
- Purpose: Authenticate API requests
- Auto-refresh: Yes (when expired)

**Refresh Token:**
- Lifetime: 30 days (default for all users)
- Storage: HttpOnly cookie (restricted to `/api/v1/auth/refresh`)
- Purpose: Obtain new access tokens
- Rotation: Yes (new token issued on each refresh)

---

## 📁 File Structure

```
dashboard/
├── app/
│   ├── composables/
│   │   └── useApi.ts              # API client with CSRF & auth handling
│   ├── middleware/
│   │   ├── auth.global.ts         # Authentication middleware
│   │   └── onboarding.global.ts   # Onboarding flow middleware
│   ├── pages/
│   │   ├── login.vue              # Login page with Google OAuth
│   │   └── profile.vue            # Profile with logout functionality
│   ├── plugins/
│   │   ├── google-oauth.client.ts # Google OAuth initialization
│   │   └── init.client.ts         # Session restore on app load
│   └── stores/
│       └── auth.ts                # Auth state management (Pinia)
├── .env                           # Environment variables (gitignored)
├── .env.example                   # Environment template
├── nuxt.config.ts                 # Nuxt configuration
└── AUTHENTICATION.md              # This file
```

---

## 🔑 Key Components

### 1. Auth Store (`app/stores/auth.ts`)

Manages authentication state using Pinia.

**State:**
- `user` - Current user data
- `isAuthenticated` - Auth status
- `isLoading` - Loading state
- `error` - Error messages

**Actions:**
- `loginWithGoogle(idToken, rememberMe)` - Login with Google
- `logout()` - Logout current device
- `logoutAllDevices()` - Logout all devices
- `refreshToken()` - Refresh access token
- `fetchCurrentUser()` - Get current user (for session restore)
- `updateProfile(data)` - Update user profile

**Usage:**
```typescript
const authStore = useAuthStore()

// Login
await authStore.loginWithGoogle(googleIdToken, rememberMe)

// Check if authenticated
if (authStore.isAuthenticated) {
  console.log('User:', authStore.user)
}

// Logout
await authStore.logout()
```

### 2. API Client (`app/composables/useApi.ts`)

Provides a configured API client with built-in security features.

**Features:**
- CSRF token management (fetch, cache, send)
- Automatic token refresh on 401 errors
- Credentials included (sends cookies)
- Error handling

**Usage:**
```typescript
const api = useApi()

// GET request
const user = await api.get('/api/v1/users/profile')

// POST request (CSRF token automatically added)
const workout = await api.post('/api/v1/workouts/', workoutData)

// Other methods
await api.put(endpoint, data)
await api.patch(endpoint, data)
await api.delete(endpoint)
```

### 3. Auth Middleware (`app/middleware/auth.global.ts`)

Protects routes and redirects unauthorized users.

**Flow:**
1. Check if route is public (`/login`)
2. If public, allow access (redirect if already authenticated)
3. If protected, check authentication
4. If not authenticated, redirect to `/login`
5. If authenticated, allow access

**Public Routes:**
- `/login` - Login page

**Protected Routes:**
- All other routes require authentication

### 4. Session Restore Plugin (`app/plugins/init.client.ts`)

Restores user session on app load.

**Flow:**
1. Check if user was previously authenticated (from localStorage)
2. If yes, attempt to fetch current user
3. If access token valid, session restored
4. If access token expired, attempt refresh
5. If refresh fails, user redirected to login by middleware

---

## 🔒 Security Considerations

### What's Secure

✅ **No tokens in localStorage** - All tokens in HttpOnly cookies (cannot be accessed by JavaScript)
✅ **CSRF protection** - One-time CSRF tokens for state-changing operations
✅ **Token rotation** - Refresh tokens rotated on every use (prevents replay attacks)
✅ **SameSite cookies** - Protects against CSRF attacks
✅ **Secure cookies in production** - HTTPS-only cookie transmission
✅ **Automatic token refresh** - Seamless UX without compromising security
✅ **Path-restricted refresh token** - Only sent to refresh endpoint

### What to Configure in Production

1. **Environment Variables:**
   ```bash
   NUXT_PUBLIC_ENV=production
   NUXT_PUBLIC_API_URL=https://api.yourapp.com
   ```

2. **Backend Cookie Settings:**
   ```python
   COOKIE_SECURE=true           # HTTPS only
   COOKIE_SAMESITE=lax          # CSRF protection
   COOKIE_DOMAIN=yourapp.com    # Your domain
   ```

3. **CORS Settings:**
   ```python
   ALLOWED_ORIGINS=https://yourapp.com,https://www.yourapp.com
   ```

4. **Google OAuth:**
   - Update authorized origins to production domain
   - Update redirect URIs to production URLs

---

## 🧪 Testing the Implementation

### Manual Testing Checklist

1. **Login Flow:**
   - [ ] Click "Login with Google" button
   - [ ] Google popup appears
   - [ ] After authentication, redirected to home or onboarding
   - [ ] User data displayed correctly on profile page

2. **Session Persistence:**
   - [ ] Login successfully
   - [ ] Refresh the page
   - [ ] User still logged in (no redirect to login)

3. **Token Refresh:**
   - [ ] Login successfully
   - [ ] Wait 30 minutes (or modify access token expiry in backend)
   - [ ] Make an API request
   - [ ] Token should auto-refresh (no logout)

4. **Logout:**
   - [ ] Click logout button
   - [ ] Redirected to login page
   - [ ] Cannot access protected routes
   - [ ] Cookies cleared (check browser DevTools)

5. **Logout All Devices:**
   - [ ] Login on two different browsers/devices
   - [ ] Click "Logout from all devices" on one
   - [ ] Other device should be logged out on next request

6. **Protected Routes:**
   - [ ] Try to access `/home` without login
   - [ ] Should redirect to `/login`
   - [ ] After login, can access protected routes

7. **Session Duration:**
   - [ ] Login successfully
   - [ ] Check refresh token expiry in browser DevTools (should be 30 days by default)
   - [ ] Session persists across browser restarts

---

## 🐛 Troubleshooting

### Issue: "Failed to fetch CSRF token"

**Cause:** Backend API not running or CORS misconfigured

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/api/v1/auth/csrf-token`
2. Check CORS settings in backend allow your frontend origin
3. Verify `ALLOWED_ORIGINS` includes your dashboard URL

### Issue: "Invalid CSRF token"

**Cause:** CSRF token expired or already used

**Solution:**
- This is handled automatically by the API client
- If persists, check backend Redis connection
- Verify backend CSRF token generation is working

### Issue: "Session expired. Please login again"

**Cause:** Both access and refresh tokens expired

**Solution:**
- Normal behavior if user hasn't accessed app for 7/30 days
- User needs to login again

### Issue: Google OAuth popup blocked

**Cause:** Browser popup blocker

**Solution:**
- Allow popups for your site
- Or user can manually allow popup

### Issue: "Invalid Google token"

**Cause:** Google Client ID mismatch or expired token

**Solution:**
1. Verify `NUXT_PUBLIC_GOOGLE_CLIENT_ID` matches backend `GOOGLE_CLIENT_ID`
2. Verify Google OAuth credentials are correct
3. Check Google Cloud Console for credential status

---

## 📚 API Endpoints Reference

### Authentication Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/v1/auth/csrf-token` | GET | No | Get CSRF token for login |
| `/api/v1/auth/login/oauth` | POST | No (CSRF) | Login with Google OAuth |
| `/api/v1/auth/refresh` | POST | No | Refresh access token |
| `/api/v1/auth/logout` | POST | Yes | Logout current device |
| `/api/v1/auth/logout-all` | POST | Yes | Logout all devices |
| `/api/v1/auth/me` | GET | Yes | Get current user |

### User Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/v1/users/profile` | GET | Yes | Get user profile |
| `/api/v1/users/profile` | PATCH | Yes | Update user profile |

---

## 🔄 Migration from Mock Data

If you have existing mock data or local storage from development:

1. **Clear localStorage:**
```javascript
// In browser console
localStorage.clear()
```

2. **Clear cookies:**
   - Open DevTools > Application > Cookies
   - Delete all cookies for your domain

3. **Restart development server:**
```bash
pnpm dev
```

---

## 📝 Development Tips

### Enable Debug Logging

Add this to your page/component to see auth state changes:

```typescript
watch(() => authStore.user, (newUser) => {
  console.log('User changed:', newUser)
}, { deep: true })

watch(() => authStore.isAuthenticated, (isAuth) => {
  console.log('Auth status:', isAuth)
})
```

### Check Cookie Values

In browser DevTools:
1. Open Application tab
2. Navigate to Cookies > your domain
3. Check for `access_token` and `refresh_token`
4. Note: Values are HttpOnly (cannot be read by JavaScript)

### Test Token Refresh

Temporarily reduce access token expiry in backend:

```python
# backend/app/config.py
ACCESS_TOKEN_EXPIRE_MINUTES = 1  # 1 minute instead of 30
```

Then test that tokens auto-refresh after 1 minute.

---

## 🎯 Next Steps

1. **Profile Editing:**
   - Implement profile editing functionality
   - Connect to backend `/api/v1/users/profile` PATCH endpoint

2. **Error Handling:**
   - Add toast notifications for errors
   - Better error messages for users

3. **Loading States:**
   - Add skeleton loaders during auth operations
   - Improve UX during token refresh

4. **Session Management UI:**
   - Show active sessions/devices
   - Allow selective device logout

5. **Analytics:**
   - Track login events
   - Monitor token refresh patterns
   - Detect suspicious activity

---

## 📖 Additional Resources

- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Nuxt 3 Documentation](https://nuxt.com/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [vue3-google-login](https://www.npmjs.com/package/vue3-google-login)
- [Backend API Documentation](../backend/README.md)

---

## 🤝 Support

For issues or questions:
1. Check this documentation
2. Review backend authentication implementation
3. Check browser console for errors
4. Verify network requests in DevTools
5. Contact development team

---

**Last Updated:** January 2026
**Version:** 1.0.0
**Author:** MuscleUp Vision Team
