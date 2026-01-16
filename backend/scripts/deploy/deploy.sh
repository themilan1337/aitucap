#!/bin/bash

################################################################################
# Manual Deployment Script
#
# Deploys the current project to production server
# Usage: bash deploy.sh [ENVIRONMENT]
################################################################################

set -e

# Configuration
PROJECT_NAME="muscleup"
ENVIRONMENT=${1:-production}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEPLOY_PATH="/opt/projects/$PROJECT_NAME"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deploying $PROJECT_NAME${NC}"
echo -e "${GREEN}  Environment: $ENVIRONMENT${NC}"
echo -e "${GREEN}========================================${NC}"

# ============================================================================
# Pre-deployment checks
# ============================================================================
echo -e "\n${YELLOW}[1/7] Running pre-deployment checks...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running${NC}"
    exit 1
fi

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    echo -e "${RED}✗ .env.production not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Pre-deployment checks passed${NC}"

# ============================================================================
# Build Docker image
# ============================================================================
echo -e "\n${YELLOW}[2/7] Building Docker image...${NC}"

docker build -f Dockerfile.prod -t ${PROJECT_NAME}-backend:latest -t ${PROJECT_NAME}-backend:${TIMESTAMP} .

echo -e "${GREEN}✓ Docker image built${NC}"

# ============================================================================
# Create release directory
# ============================================================================
echo -e "\n${YELLOW}[3/7] Creating release directory...${NC}"

RELEASE_PATH="$DEPLOY_PATH/releases/$TIMESTAMP"
mkdir -p "$RELEASE_PATH"

# Copy files to release directory
cp docker-compose.prod.yml "$RELEASE_PATH/"
cp .env.production "$RELEASE_PATH/"
cp -r nginx "$RELEASE_PATH/" || true
cp -r models "$RELEASE_PATH/" || true

echo -e "${GREEN}✓ Release directory created: $RELEASE_PATH${NC}"

# ============================================================================
# Health check on current deployment
# ============================================================================
echo -e "\n${YELLOW}[4/7] Checking current deployment...${NC}"

if curl -sf http://localhost:8001/health > /dev/null 2>&1; then
    CURRENT_HEALTHY=true
    echo -e "${GREEN}✓ Current deployment is healthy${NC}"
else
    CURRENT_HEALTHY=false
    echo -e "${YELLOW}⚠ Current deployment is not responding${NC}"
fi

# ============================================================================
# Start new deployment
# ============================================================================
echo -e "\n${YELLOW}[5/7] Starting new deployment...${NC}"

cd "$RELEASE_PATH"

# Start containers
docker-compose -f docker-compose.prod.yml up -d

# ============================================================================
# Health check on new deployment
# ============================================================================
echo -e "\n${YELLOW}[6/7] Waiting for new deployment...${NC}"

HEALTH_CHECK_ATTEMPTS=0
MAX_ATTEMPTS=30

while [ $HEALTH_CHECK_ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    if curl -sf http://localhost:8001/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ New deployment is healthy!${NC}"
        NEW_HEALTHY=true
        break
    fi

    HEALTH_CHECK_ATTEMPTS=$((HEALTH_CHECK_ATTEMPTS + 1))
    echo "Attempt $HEALTH_CHECK_ATTEMPTS/$MAX_ATTEMPTS: Waiting for health check..."
    sleep 5
done

if [ "$NEW_HEALTHY" != "true" ]; then
    echo -e "${RED}✗ New deployment failed health check${NC}"
    echo -e "${YELLOW}Rolling back...${NC}"
    docker-compose -f docker-compose.prod.yml down
    exit 1
fi

# ============================================================================
# Update symlink
# ============================================================================
echo -e "\n${YELLOW}[7/7] Finalizing deployment...${NC}"

# Update current symlink
ln -sfn "$RELEASE_PATH" "$DEPLOY_PATH/current"

# Cleanup old releases (keep last 5)
cd "$DEPLOY_PATH/releases"
ls -t | tail -n +6 | xargs -r rm -rf

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Successful!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Release: $TIMESTAMP"
echo "Location: $RELEASE_PATH"
echo "Health: http://localhost:8001/health"
echo ""
echo "To rollback: bash rollback.sh"
echo ""
