#!/bin/bash

################################################################################
# Remove nginx-proxy and switch to standalone Nginx
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  Remove nginx-proxy Setup${NC}"
echo -e "${YELLOW}========================================${NC}"

echo -e "\n${YELLOW}This will:${NC}"
echo -e "1. Stop and remove nginx-proxy containers"
echo -e "2. Free ports 80 and 443"
echo -e "3. Allow standalone Nginx to run"
echo -e ""
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Stop containers
echo -e "\n${YELLOW}Stopping nginx-proxy containers...${NC}"
if docker ps | grep -q nginx-proxy-acme; then
    docker stop nginx-proxy-acme
    echo -e "${GREEN}✓ Stopped nginx-proxy-acme${NC}"
fi

if docker ps | grep -q nginx-proxy; then
    docker stop nginx-proxy
    echo -e "${GREEN}✓ Stopped nginx-proxy${NC}"
fi

# Ask about removal
echo -e "\n${YELLOW}Do you want to completely remove these containers?${NC}"
echo -e "(You can restart them later if needed)"
read -p "Remove containers? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker rm nginx-proxy-acme 2>/dev/null || true
    docker rm nginx-proxy 2>/dev/null || true
    echo -e "${GREEN}✓ Containers removed${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  nginx-proxy stopped!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e ""
echo -e "Ports 80 and 443 are now available."
echo -e ""
echo -e "Next steps:"
echo -e "1. Deploy Nginx configuration:"
echo -e "   sudo bash scripts/deploy/setup-server.sh"
echo -e ""
echo -e "2. Get SSL certificate:"
echo -e "   sudo bash scripts/deploy/setup-ssl-simple.sh"
echo -e ""
echo -e "3. Start your backend:"
echo -e "   docker compose -f docker compose.prod.yml up -d"
echo -e ""
