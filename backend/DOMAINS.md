# MuscleUp Domains Configuration

## Production Domains

### Landing Page
- **URL**: https://muscleup.fitness
- **Purpose**: Marketing landing page
- **SSL**: Managed separately (not by this backend)

### Web Application
- **URL**: https://app.muscleup.fitness
- **Purpose**: Main web application dashboard
- **SSL**: Managed separately (not by this backend)

### API Backend
- **URL**: https://api.muscleup.fitness
- **Purpose**: REST API and WebSocket endpoints
- **SSL**: ✅ Managed by this deployment (Let's Encrypt)
- **Email**: admin@muscleup.fitness (for SSL certificate)

## DNS Configuration

Add these A records to your DNS:

```
Type  Name    Value           TTL
A     @       YOUR_SERVER_IP  300
A     www     YOUR_SERVER_IP  300
A     app     YOUR_SERVER_IP  300
A     api     YOUR_SERVER_IP  300
```

Or if using subdomains:
```
muscleup.fitness        →  YOUR_SERVER_IP
www.muscleup.fitness    →  YOUR_SERVER_IP
app.muscleup.fitness    →  YOUR_SERVER_IP
api.muscleup.fitness    →  YOUR_SERVER_IP
```

## SSL Certificate Setup

### Automated Setup (Recommended)

```bash
# Run on server after DNS is configured
sudo bash scripts/deploy/setup-ssl.sh
```

This will:
- Install Certbot if needed
- Obtain SSL certificate for api.muscleup.fitness
- Configure Nginx automatically
- Setup auto-renewal

### Manual Setup

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx \
  -d api.muscleup.fitness \
  --email admin@muscleup.fitness \
  --agree-tos \
  --redirect \
  --hsts
```

### Certificate Information

- **Domain**: api.muscleup.fitness
- **Email**: admin@muscleup.fitness
- **Renewal**: Automatic (via systemd timer)
- **Check status**: `sudo certbot certificates`
- **Test renewal**: `sudo certbot renew --dry-run`

## CORS Configuration

Backend allows these origins:

```bash
# Production
ALLOWED_ORIGINS=https://muscleup.fitness,https://www.muscleup.fitness,https://app.muscleup.fitness

# Development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Cookie Configuration

```bash
# Production
COOKIE_DOMAIN=api.muscleup.fitness
COOKIE_SECURE=true
COOKIE_SAMESITE=lax

# Development
COOKIE_DOMAIN=localhost
COOKIE_SECURE=false
COOKIE_SAMESITE=lax
```

## Environment Files

### `.env` (Development)
```bash
COOKIE_DOMAIN=localhost
COOKIE_SECURE=false
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### `.env.production` (Production)
```bash
COOKIE_DOMAIN=api.muscleup.fitness
COOKIE_SECURE=true
ALLOWED_ORIGINS=https://muscleup.fitness,https://www.muscleup.fitness,https://app.muscleup.fitness
```

## Verification

### Check DNS Resolution

```bash
# Check all domains
nslookup muscleup.fitness
nslookup www.muscleup.fitness
nslookup app.muscleup.fitness
nslookup api.muscleup.fitness
```

### Test SSL Certificate

```bash
# Check certificate
curl -I https://api.muscleup.fitness/health

# Detailed SSL info
openssl s_client -connect api.muscleup.fitness:443 -servername api.muscleup.fitness

# Check expiration
echo | openssl s_client -servername api.muscleup.fitness -connect api.muscleup.fitness:443 2>/dev/null | openssl x509 -noout -dates
```

### Test API Endpoints

```bash
# Health check
curl https://api.muscleup.fitness/health

# CORS test
curl -H "Origin: https://app.muscleup.fitness" -H "Access-Control-Request-Method: POST" -X OPTIONS https://api.muscleup.fitness/api/v1/auth/login/oauth -v
```

## Troubleshooting

### DNS Not Propagating

```bash
# Check with different DNS servers
nslookup api.muscleup.fitness 8.8.8.8
nslookup api.muscleup.fitness 1.1.1.1

# Clear local DNS cache (macOS)
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

# Clear local DNS cache (Linux)
sudo systemd-resolve --flush-caches
```

### SSL Certificate Issues

```bash
# Check Nginx configuration
sudo nginx -t

# Check Certbot logs
sudo tail -f /var/log/letsencrypt/letsencrypt.log

# Renew certificate manually
sudo certbot renew --force-renewal

# Restart Nginx
sudo systemctl restart nginx
```

### CORS Errors

1. Check `.env.production` has correct ALLOWED_ORIGINS
2. Restart backend: `docker-compose -f docker-compose.prod.yml restart backend`
3. Check Nginx headers in response
4. Verify frontend is using correct API URL

## Security Notes

- ✅ SSL/TLS only for API subdomain
- ✅ HTTPS redirect enabled
- ✅ HSTS header enabled
- ✅ Secure cookies in production
- ✅ CORS restricted to known origins
- ✅ Rate limiting enabled

## Contact

- **SSL Issues**: admin@muscleup.fitness
- **Domain Management**: Check your domain registrar
- **Technical Support**: GitHub Issues

---

**Last Updated**: 2026-01-16
**SSL Certificate**: Let's Encrypt (Auto-renewing)
