#!/bin/bash

################################################################################
# SSL Setup for nginx-proxy environment
# Works with existing jwilder/nginx-proxy + acme-companion setup
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  nginx-proxy SSL Configuration${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if nginx-proxy is running
if ! docker ps | grep -q nginx-proxy; then
    echo -e "${RED}nginx-proxy container not found${NC}"
    echo "Please ensure nginx-proxy and acme-companion are running"
    exit 1
fi

echo -e "${GREEN}✓ Found nginx-proxy container${NC}"

# Check if acme-companion is running
if docker ps | grep -q nginx-proxy-acme; then
    echo -e "${GREEN}✓ Found acme-companion container${NC}"
    echo -e "\n${YELLOW}Your nginx-proxy is already configured for automatic SSL!${NC}"
    echo -e "To enable SSL for your backend, you need to:"
    echo -e ""
    echo -e "1. Add these environment variables to your backend container:"
    echo -e "   ${YELLOW}VIRTUAL_HOST=api.muscleup.fitness${NC}"
    echo -e "   ${YELLOW}LETSENCRYPT_HOST=api.muscleup.fitness${NC}"
    echo -e "   ${YELLOW}LETSENCRYPT_EMAIL=admin@muscleup.fitness${NC}"
    echo -e ""
    echo -e "2. Connect your backend container to the nginx-proxy network"
    echo -e ""
    echo -e "Example docker-compose.yml:"
    echo -e "${YELLOW}───────────────────────────────────────${NC}"
    cat <<'COMPOSE'
version: '3.8'

services:
  backend:
    build: .
    environment:
      - VIRTUAL_HOST=api.muscleup.fitness
      - LETSENCRYPT_HOST=api.muscleup.fitness
      - LETSENCRYPT_EMAIL=admin@muscleup.fitness
    expose:
      - "8001"
    networks:
      - nginx-proxy

networks:
  nginx-proxy:
    external: true
COMPOSE
    echo -e "${YELLOW}───────────────────────────────────────${NC}"
    echo -e ""
    echo -e "The acme-companion will automatically:"
    echo -e "  • Request SSL certificate from Let's Encrypt"
    echo -e "  • Configure nginx-proxy for HTTPS"
    echo -e "  • Auto-renew certificates before expiration"
    echo -e ""
else
    echo -e "${YELLOW}⚠ acme-companion not found${NC}"
    echo -e "You need to set up nginx-proxy with acme-companion for automatic SSL"
    echo -e ""
    echo -e "Run these commands to set it up:"
    echo -e "${YELLOW}───────────────────────────────────────${NC}"
    cat <<'SETUP'
# Create network
docker network create nginx-proxy

# Start nginx-proxy
docker run -d \
  --name nginx-proxy \
  --restart always \
  --network nginx-proxy \
  -p 80:80 -p 443:443 \
  -v /var/run/docker.sock:/tmp/docker.sock:ro \
  -v nginx-certs:/etc/nginx/certs \
  -v nginx-vhost:/etc/nginx/vhost.d \
  -v nginx-html:/usr/share/nginx/html \
  jwilder/nginx-proxy

# Start acme-companion
docker run -d \
  --name nginx-proxy-acme \
  --restart always \
  --network nginx-proxy \
  --volumes-from nginx-proxy \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v acme-state:/etc/acme.sh \
  -e DEFAULT_EMAIL=admin@muscleup.fitness \
  nginxproxy/acme-companion
SETUP
    echo -e "${YELLOW}───────────────────────────────────────${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  Next Steps${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e ""
echo -e "1. Update your docker-compose.prod.yml with VIRTUAL_HOST and LETSENCRYPT_HOST"
echo -e "2. Connect to nginx-proxy network"
echo -e "3. Deploy: docker-compose -f docker-compose.prod.yml up -d"
echo -e "4. Wait 1-2 minutes for SSL certificate to be issued"
echo -e "5. Check logs: docker logs nginx-proxy-acme -f"
echo -e ""
