#!/bin/bash

################################################################################
# Rollback Script
#
# Rolls back to the previous deployment
# Usage: bash rollback.sh
################################################################################

set -e

# Configuration
PROJECT_NAME="muscleup"
DEPLOY_PATH="/opt/projects/$PROJECT_NAME"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${RED}========================================${NC}"
echo -e "${RED}  Rolling Back $PROJECT_NAME${NC}"
echo -e "${RED}========================================${NC}"

# ============================================================================
# Find previous release
# ============================================================================
echo -e "\n${YELLOW}Finding previous release...${NC}"

cd "$DEPLOY_PATH/releases"
RELEASES=($(ls -t))

if [ ${#RELEASES[@]} -lt 2 ]; then
    echo -e "${RED}✗ No previous release found!${NC}"
    exit 1
fi

CURRENT_RELEASE=${RELEASES[0]}
PREVIOUS_RELEASE=${RELEASES[1]}

echo "Current release: $CURRENT_RELEASE"
echo "Previous release: $PREVIOUS_RELEASE"

# Confirm rollback
read -p "Are you sure you want to rollback? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Rollback cancelled"
    exit 0
fi

# ============================================================================
# Stop current deployment
# ============================================================================
echo -e "\n${YELLOW}Stopping current deployment...${NC}"

cd "$DEPLOY_PATH/releases/$CURRENT_RELEASE"
docker compose -f docker compose.prod.yml down

# ============================================================================
# Start previous deployment
# ============================================================================
echo -e "\n${YELLOW}Starting previous deployment...${NC}"

cd "$DEPLOY_PATH/releases/$PREVIOUS_RELEASE"
docker compose -f docker compose.prod.yml up -d

# ============================================================================
# Health check
# ============================================================================
echo -e "\n${YELLOW}Waiting for rollback to complete...${NC}"

HEALTH_CHECK_ATTEMPTS=0
MAX_ATTEMPTS=30

while [ $HEALTH_CHECK_ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    if curl -sf http://localhost:8001/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Rollback successful!${NC}"
        ROLLBACK_HEALTHY=true
        break
    fi

    HEALTH_CHECK_ATTEMPTS=$((HEALTH_CHECK_ATTEMPTS + 1))
    echo "Attempt $HEALTH_CHECK_ATTEMPTS/$MAX_ATTEMPTS: Waiting for health check..."
    sleep 5
done

if [ "$ROLLBACK_HEALTHY" != "true" ]; then
    echo -e "${RED}✗ Rollback failed health check${NC}"
    exit 1
fi

# ============================================================================
# Update symlink
# ============================================================================
echo -e "\n${YELLOW}Updating symlink...${NC}"

ln -sfn "$DEPLOY_PATH/releases/$PREVIOUS_RELEASE" "$DEPLOY_PATH/current"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Rollback Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Rolled back to: $PREVIOUS_RELEASE"
echo "Health: http://localhost:8001/health"
echo ""
