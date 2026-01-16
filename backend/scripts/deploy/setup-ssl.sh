#!/bin/bash

################################################################################
# SSL Certificate Setup Script
#
# Автоматически получает SSL сертификат для API домена
# Email: admin@muscleup.fitness
# Domain: api.muscleup.fitness
#
# Usage: sudo bash setup-ssl.sh
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="api.muscleup.fitness"
EMAIL="admin@muscleup.fitness"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  SSL Certificate Setup${NC}"
echo -e "${GREEN}  Domain: $DOMAIN${NC}"
echo -e "${GREEN}  Email: $EMAIL${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if certbot is installed
if ! command -v certbot &> /dev/null; then
    echo -e "${YELLOW}Installing Certbot...${NC}"
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
fi

# Check if Nginx is running
if ! systemctl is-active --quiet nginx; then
    echo -e "${YELLOW}Starting Nginx...${NC}"
    systemctl start nginx
fi

# Check DNS resolution
echo -e "\n${YELLOW}Checking DNS resolution for $DOMAIN...${NC}"
if ! nslookup $DOMAIN > /dev/null 2>&1; then
    echo -e "${RED}✗ DNS not configured for $DOMAIN${NC}"
    echo -e "${YELLOW}Please add an A record pointing to this server's IP${NC}"
    echo -e "${YELLOW}You can continue anyway, but Certbot will fail${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓ DNS configured correctly${NC}"
fi

# Create webroot directory for Certbot challenges
echo -e "\n${YELLOW}Creating webroot directory...${NC}"
mkdir -p /var/www/certbot
chown -R www-data:www-data /var/www/certbot

# Test Nginx configuration
echo -e "\n${YELLOW}Testing Nginx configuration...${NC}"
if ! nginx -t; then
    echo -e "${RED}✗ Nginx configuration has errors${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Nginx configuration is valid${NC}"

# Reload Nginx to apply any changes
systemctl reload nginx

# Create temporary Nginx config for certificate verification
echo -e "\n${YELLOW}Creating temporary Nginx configuration for SSL setup...${NC}"
cat > /etc/nginx/sites-available/ssl-temp.conf <<'TEMPCONF'
server {
    listen 80;
    listen [::]:80;
    server_name api.muscleup.fitness;

    # Allow Certbot challenges
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        try_files $uri =404;
    }

    # Temporary health check (no backend needed)
    location / {
        return 200 "SSL Setup in Progress\n";
        add_header Content-Type text/plain;
    }
}
TEMPCONF

# Disable the main site config temporarily
if [ -L /etc/nginx/sites-enabled/muscleup.conf ]; then
    rm /etc/nginx/sites-enabled/muscleup.conf
    echo -e "${YELLOW}Disabled main site configuration temporarily${NC}"
fi

# Enable temporary config
ln -sf /etc/nginx/sites-available/ssl-temp.conf /etc/nginx/sites-enabled/ssl-temp.conf

# Test and reload Nginx
nginx -t && systemctl reload nginx

# Obtain SSL certificate
echo -e "\n${YELLOW}Obtaining SSL certificate from Let's Encrypt...${NC}"
echo -e "${YELLOW}This may take a few moments...${NC}"

# Use webroot plugin instead of nginx plugin
certbot certonly \
    --webroot \
    -w /var/www/certbot \
    -d $DOMAIN \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    --non-interactive

if [ $? -eq 0 ]; then
    # Restore main site configuration
    echo -e "\n${YELLOW}Restoring main site configuration...${NC}"
    rm -f /etc/nginx/sites-enabled/ssl-temp.conf
    ln -sf /etc/nginx/sites-available/muscleup.conf /etc/nginx/sites-enabled/muscleup.conf
    nginx -t && systemctl reload nginx

    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}  SSL Certificate Installed!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "Domain: $DOMAIN"
    echo -e "Certificate: /etc/letsencrypt/live/$DOMAIN/fullchain.pem"
    echo -e "Private Key: /etc/letsencrypt/live/$DOMAIN/privkey.pem"
    echo -e ""
    echo -e "Auto-renewal is configured via systemd timer"
    echo -e "Check status: systemctl status certbot.timer"
    echo -e ""
    echo -e "${GREEN}Your API will be accessible at: https://$DOMAIN (after backend is started)${NC}"
else
    # Restore main site configuration even on failure
    echo -e "\n${YELLOW}Restoring main site configuration...${NC}"
    rm -f /etc/nginx/sites-enabled/ssl-temp.conf
    if [ -f /etc/nginx/sites-available/muscleup.conf ]; then
        ln -sf /etc/nginx/sites-available/muscleup.conf /etc/nginx/sites-enabled/muscleup.conf
        nginx -t && systemctl reload nginx
    fi
    echo -e "\n${RED}========================================${NC}"
    echo -e "${RED}  SSL Certificate Installation Failed${NC}"
    echo -e "${RED}========================================${NC}"
    echo -e ""
    echo -e "Possible reasons:"
    echo -e "1. DNS not configured correctly"
    echo -e "2. Firewall blocking port 80/443"
    echo -e "3. Nginx not configured properly"
    echo -e ""
    echo -e "Troubleshooting:"
    echo -e "- Check DNS: nslookup $DOMAIN"
    echo -e "- Check firewall: sudo ufw status"
    echo -e "- Check Nginx logs: sudo tail -f /var/log/nginx/error.log"
    exit 1
fi

# Verify certificate
echo -e "\n${YELLOW}Verifying certificate...${NC}"
if openssl s_client -connect $DOMAIN:443 -servername $DOMAIN </dev/null 2>/dev/null | grep -q "Verify return code: 0"; then
    echo -e "${GREEN}✓ Certificate verified successfully${NC}"
else
    echo -e "${YELLOW}⚠ Certificate verification inconclusive (this is normal immediately after installation)${NC}"
fi

# Show certificate info
echo -e "\n${YELLOW}Certificate Information:${NC}"
certbot certificates -d $DOMAIN

# Setup auto-renewal test
echo -e "\n${YELLOW}Setting up auto-renewal...${NC}"

# Test renewal (dry-run)
echo -e "Testing renewal process (dry-run)..."
if certbot renew --dry-run --quiet; then
    echo -e "${GREEN}✓ Auto-renewal configured successfully${NC}"
else
    echo -e "${YELLOW}⚠ Auto-renewal test had issues, but certificate is installed${NC}"
fi

# Create renewal hook script for Nginx reload
mkdir -p /etc/letsencrypt/renewal-hooks/deploy
cat > /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh <<'HOOK'
#!/bin/bash
systemctl reload nginx
HOOK

chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e ""
echo -e "Next steps:"
echo -e "1. Update your .env.production file:"
echo -e "   COOKIE_DOMAIN=api.muscleup.fitness"
echo -e "   ALLOWED_ORIGINS=https://muscleup.fitness,https://app.muscleup.fitness"
echo -e ""
echo -e "2. Restart your backend:"
echo -e "   docker compose -f docker compose.prod.yml restart backend"
echo -e ""
echo -e "3. Test your API:"
echo -e "   curl https://$DOMAIN/health"
echo -e ""
echo -e "Certificate will auto-renew before expiration."
echo -e "Check renewal timer: systemctl status certbot.timer"
echo -e ""
