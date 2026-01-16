#!/bin/bash

################################################################################
# Deploy MuscleUp Backend with nginx-proxy
#
# This script:
# 1. Checks nginx-proxy setup
# 2. Creates necessary networks
# 3. Deploys the application
# 4. Monitors SSL certificate generation
#
# Usage: sudo bash scripts/deploy/deploy-with-nginx-proxy.sh
################################################################################

set -e

# Determine which docker-compose command to use
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

DOMAIN="api.muscleup.fitness"
EMAIL="admin@muscleup.fitness"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  MuscleUp Backend Deployment${NC}"
echo -e "${BLUE}  with nginx-proxy + SSL${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

# 1. Check nginx-proxy
echo -e "\n${YELLOW}[1/6] Checking nginx-proxy setup...${NC}"
if ! docker ps | grep -q "nginx-proxy"; then
    echo -e "${RED}✗ nginx-proxy container not found${NC}"
    echo -e "\nPlease set up nginx-proxy first:"
    echo -e "${YELLOW}docker network create nginx-proxy${NC}"
    echo -e "${YELLOW}docker run -d --name nginx-proxy --restart always \\${NC}"
    echo -e "${YELLOW}  --network nginx-proxy -p 80:80 -p 443:443 \\${NC}"
    echo -e "${YELLOW}  -v /var/run/docker.sock:/tmp/docker.sock:ro \\${NC}"
    echo -e "${YELLOW}  -v nginx-certs:/etc/nginx/certs \\${NC}"
    echo -e "${YELLOW}  -v nginx-vhost:/etc/nginx/vhost.d \\${NC}"
    echo -e "${YELLOW}  -v nginx-html:/usr/share/nginx/html \\${NC}"
    echo -e "${YELLOW}  jwilder/nginx-proxy${NC}"
    exit 1
fi
echo -e "${GREEN}✓ nginx-proxy is running${NC}"

# 2. Check acme-companion
echo -e "\n${YELLOW}[2/6] Checking acme-companion...${NC}"
if ! docker ps | grep -q "nginx-proxy-acme"; then
    echo -e "${YELLOW}⚠ acme-companion not found, starting it...${NC}"
    docker run -d \
      --name nginx-proxy-acme \
      --restart always \
      --network nginx-proxy \
      --volumes-from nginx-proxy \
      -v /var/run/docker.sock:/var/run/docker.sock:ro \
      -v acme-state:/etc/acme.sh \
      -e DEFAULT_EMAIL=$EMAIL \
      nginxproxy/acme-companion
    echo -e "${GREEN}✓ Started acme-companion${NC}"
else
    echo -e "${GREEN}✓ acme-companion is running${NC}"
fi

# 3. Check nginx-proxy network
echo -e "\n${YELLOW}[3/6] Checking nginx-proxy network...${NC}"
if ! docker network ls | grep -q "nginx-proxy"; then
    echo -e "${YELLOW}Creating nginx-proxy network...${NC}"
    docker network create nginx-proxy
    echo -e "${GREEN}✓ Created nginx-proxy network${NC}"
else
    echo -e "${GREEN}✓ nginx-proxy network exists${NC}"
fi

# 4. Check .env.production
echo -e "\n${YELLOW}[4/6] Checking environment configuration...${NC}"
if [ ! -f .env.production ]; then
    echo -e "${RED}✗ .env.production not found${NC}"
    echo -e "Please create .env.production with your configuration"
    exit 1
fi
echo -e "${GREEN}✓ .env.production exists${NC}"

# 5. Build and deploy
echo -e "\n${YELLOW}[5/6] Building and deploying application...${NC}"
$DOCKER_COMPOSE -f docker-compose.prod.yml pull
$DOCKER_COMPOSE -f docker-compose.prod.yml build --no-cache
$DOCKER_COMPOSE -f docker-compose.prod.yml up -d

echo -e "${GREEN}✓ Application deployed${NC}"

# 6. Monitor SSL certificate generation
echo -e "\n${YELLOW}[6/6] Monitoring SSL certificate generation...${NC}"
echo -e "${BLUE}This may take 1-2 minutes...${NC}"
echo -e ""

# Wait for backend to be healthy
echo -ne "Waiting for backend to be healthy..."
for i in {1..30}; do
    if docker exec muscleup_backend curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        echo -e " ${GREEN}✓${NC}"
        break
    fi
    echo -n "."
    sleep 2
done

# Check acme-companion logs
echo -e "\n${BLUE}acme-companion activity:${NC}"
docker logs --tail 20 nginx-proxy-acme

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  Deployment Status${NC}"
echo -e "${BLUE}========================================${NC}"

# Check container status
echo -e "\n${YELLOW}Running containers:${NC}"
$DOCKER_COMPOSE -f docker-compose.prod.yml ps

# Check if certificate is being generated
echo -e "\n${YELLOW}Checking SSL certificate...${NC}"
sleep 5

if docker exec nginx-proxy ls /etc/nginx/certs/${DOMAIN}.crt 2>/dev/null; then
    echo -e "${GREEN}✓ SSL certificate exists!${NC}"
    echo -e "\n${GREEN}Your API is now available at:${NC}"
    echo -e "${GREEN}https://${DOMAIN}${NC}"

    # Test the endpoint
    echo -e "\n${YELLOW}Testing endpoint...${NC}"
    sleep 2
    if curl -sf https://${DOMAIN}/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ HTTPS endpoint is working!${NC}"
    else
        echo -e "${YELLOW}⚠ Endpoint not responding yet (may take a few more seconds)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ SSL certificate not yet generated${NC}"
    echo -e "This is normal for first deployment. Certificate will be issued shortly."
    echo -e "\nMonitor progress with:"
    echo -e "  ${BLUE}docker logs nginx-proxy-acme -f${NC}"
    echo -e "\nThe certificate should appear within 1-2 minutes."
fi

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  Useful Commands${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e ""
echo -e "View logs:"
echo -e "  $DOCKER_COMPOSE -f docker-compose.prod.yml logs -f backend"
echo -e "  docker logs nginx-proxy-acme -f"
echo -e ""
echo -e "Check certificate:"
echo -e "  docker exec nginx-proxy ls -la /etc/nginx/certs/"
echo -e ""
echo -e "Restart services:"
echo -e "  $DOCKER_COMPOSE -f docker-compose.prod.yml restart backend"
echo -e ""
echo -e "Stop all:"
echo -e "  $DOCKER_COMPOSE -f docker-compose.prod.yml down"
echo -e ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
