#!/bin/bash

################################################################################
# Server Setup Script
#
# This script sets up an Ubuntu server for multi-project Docker deployment
# with Nginx, SSL, monitoring, and all necessary infrastructure.
#
# Usage: sudo bash setup-server.sh
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Multi-Project Server Setup${NC}"
echo -e "${GREEN}========================================${NC}"

# ============================================================================
# Step 1: Update system packages
# ============================================================================
echo -e "\n${YELLOW}[1/8] Updating system packages...${NC}"
apt-get update
apt-get upgrade -y

# ============================================================================
# Step 2: Install essential packages
# ============================================================================
echo -e "\n${YELLOW}[2/8] Installing essential packages...${NC}"
apt-get install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    ufw \
    fail2ban \
    certbot \
    python3-certbot-nginx \
    build-essential \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# ============================================================================
# Step 3: Install Docker
# ============================================================================
echo -e "\n${YELLOW}[3/8] Installing Docker...${NC}"

# Remove old Docker versions
apt-get remove -y docker docker-engine docker.io containerd runc || true

# Add Docker's official GPG key
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start and enable Docker
systemctl start docker
systemctl enable docker

# Add current user to docker group (if not root)
if [ -n "$SUDO_USER" ]; then
    usermod -aG docker $SUDO_USER
    echo -e "${GREEN}Added $SUDO_USER to docker group${NC}"
fi

echo -e "${GREEN}✓ Docker installed: $(docker --version)${NC}"

# ============================================================================
# Step 4: Install Nginx
# ============================================================================
echo -e "\n${YELLOW}[4/8] Installing Nginx...${NC}"
apt-get install -y nginx

# Backup default config
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# Create sites directory structure
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/nginx/sites-enabled

# Remove default site
rm -f /etc/nginx/sites-enabled/default

systemctl start nginx
systemctl enable nginx

echo -e "${GREEN}✓ Nginx installed: $(nginx -v 2>&1 | cut -d'/' -f2)${NC}"

# ============================================================================
# Step 5: Configure firewall (UFW)
# ============================================================================
echo -e "\n${YELLOW}[5/8] Configuring firewall...${NC}"

# Reset UFW to defaults
ufw --force reset

# Default policies
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (important!)
ufw allow 22/tcp

# Allow HTTP and HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Enable UFW
ufw --force enable

echo -e "${GREEN}✓ Firewall configured${NC}"

# ============================================================================
# Step 6: Configure Fail2Ban
# ============================================================================
echo -e "\n${YELLOW}[6/8] Configuring Fail2Ban...${NC}"

# Create custom jail
cat > /etc/fail2ban/jail.local <<EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = 22
logpath = %(sshd_log)s
backend = %(sshd_backend)s

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
port = http,https
logpath = /var/log/nginx/error.log
EOF

systemctl restart fail2ban
systemctl enable fail2ban

echo -e "${GREEN}✓ Fail2Ban configured${NC}"

# ============================================================================
# Step 7: Create project directory structure
# ============================================================================
echo -e "\n${YELLOW}[7/8] Creating project directory structure...${NC}"

# Main projects directory
mkdir -p /opt/projects

# Shared directories
mkdir -p /opt/deploy/scripts
mkdir -p /opt/deploy/configs
mkdir -p /var/www/certbot  # For Let's Encrypt challenges

# Set permissions
chown -R $SUDO_USER:$SUDO_USER /opt/projects
chown -R $SUDO_USER:$SUDO_USER /opt/deploy

echo -e "${GREEN}✓ Directory structure created${NC}"

# ============================================================================
# Step 8: Create helper scripts
# ============================================================================
echo -e "\n${YELLOW}[8/8] Creating helper scripts...${NC}"

# Create new-project script
cat > /opt/deploy/scripts/new-project.sh <<'EOFSCRIPT'
#!/bin/bash

# New Project Setup Script
# Usage: bash new-project.sh PROJECT_NAME DOMAIN PORT_BASE

set -e

PROJECT_NAME=$1
DOMAIN=$2
PORT_BASE=$3

if [ -z "$PROJECT_NAME" ] || [ -z "$DOMAIN" ] || [ -z "$PORT_BASE" ]; then
    echo "Usage: bash new-project.sh PROJECT_NAME DOMAIN PORT_BASE"
    echo "Example: bash new-project.sh myapp api.myapp.com 8100"
    exit 1
fi

echo "Creating new project: $PROJECT_NAME"

# Create project directory
mkdir -p /opt/projects/$PROJECT_NAME/{releases,shared/{logs,backups}}

# Create Nginx config
cat > /etc/nginx/sites-available/$PROJECT_NAME.conf <<EOF
upstream ${PROJECT_NAME}_backend {
    server localhost:${PORT_BASE};
}

server {
    listen 80;
    server_name ${DOMAIN};

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name ${DOMAIN};

    # SSL will be configured by Certbot

    location / {
        proxy_pass http://${PROJECT_NAME}_backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/$PROJECT_NAME.conf /etc/nginx/sites-enabled/

# Test Nginx config
nginx -t && systemctl reload nginx

echo "✓ Project $PROJECT_NAME created!"
echo "Next steps:"
echo "1. Get SSL certificate: sudo bash /opt/deploy/scripts/setup-ssl.sh"
echo "2. Deploy your code to /opt/projects/$PROJECT_NAME"
EOFSCRIPT

chmod +x /opt/deploy/scripts/new-project.sh

echo -e "${GREEN}✓ Helper scripts created${NC}"

# ============================================================================
# Final steps
# ============================================================================
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Server is now configured for multi-project deployment!"
echo ""
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  ⚠️  ВАЖНО: Перелогиньтесь!${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "Ваш пользователь был добавлен в группу 'docker',"
echo "но изменения вступят в силу только после выхода и повторного входа."
echo ""
echo -e "${GREEN}Выполните:${NC}"
echo "  1. Выйдите: ${YELLOW}exit${NC}"
echo "  2. Войдите снова: ${YELLOW}ssh user@server${NC}"
echo ""
echo "Или примените изменения сейчас (без перелогина):"
echo "  ${YELLOW}newgrp docker${NC}"
echo ""
echo -e "${GREEN}========================================${NC}"
echo ""
echo "После перелогина выполните:"
echo "1. Setup SSL certificate: bash scripts/deploy/setup-ssl.sh"
echo "2. Configure GitHub Actions secrets for CI/CD"
echo "3. Deploy your first project: git push origin main"
echo ""
