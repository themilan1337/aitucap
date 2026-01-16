# Auto-Deploy System Prompt for AI Assistants

> **Purpose**: This document contains instructions for AI assistants (like Claude, ChatGPT, Cursor AI) to generate a production-ready auto-deployment system for backend projects that is compatible with an existing multi-project Ubuntu server infrastructure.

## Context

You are helping to set up an auto-deployment system for a new backend project. This project will be deployed to an Ubuntu server that already hosts multiple backend projects using a standardized deployment infrastructure.

The server uses:
- **Docker & Docker Compose** for containerization and isolation
- **Nginx** as a reverse proxy with SSL/TLS termination
- **GitHub Actions** for CI/CD pipelines
- **Blue-Green deployment** strategy for zero-downtime deployments
- **Let's Encrypt** for automatic SSL certificates

## Your Task

Create a complete auto-deployment configuration for a new backend project that integrates seamlessly with the existing infrastructure.

## Required Files to Generate

### 1. **Dockerfile.prod**
Create a production-optimized multi-stage Dockerfile:

**Requirements**:
- Multi-stage build (builder + runtime)
- Non-root user for security
- Minimal image size
- Health check endpoint
- Proper signal handling for graceful shutdown
- Layer caching optimization

**Template Structure**:
```dockerfile
# Stage 1: Builder
FROM <base-image>:<version>-slim as builder
# Install build dependencies
# Copy and install application dependencies

# Stage 2: Runtime
FROM <base-image>:<version>-slim
# Create non-root user
# Copy from builder
# Set up health check
# Expose port
# CMD with exec form for proper signal handling
```

### 2. **docker compose.prod.yml**
Create a production Docker Compose configuration:

**Requirements**:
- All services (backend, database, cache, etc.)
- Isolated Docker network with custom subnet
- Health checks for all services
- Resource limits (CPU, memory)
- Persistent volumes with named volumes
- Restart policies (`unless-stopped`)
- Proper environment variable injection
- Logging configuration (JSON driver, size limits)
- Port mapping avoiding conflicts (see Port Allocation below)

**Port Allocation Formula**:
```
Base Port = 8000 + (Project_Number × 100)

Example for Project #1 (muscleup):
- Backend:    8001
- PostgreSQL: 5433
- Redis:      6380
- Additional: 8002, 8003, etc.

Example for Project #2:
- Backend:    8101
- PostgreSQL: 5533
- Redis:      6480
```

### 3. **nginx/<project-name>.conf**
Create Nginx reverse proxy configuration:

**Requirements**:
- HTTP to HTTPS redirect
- SSL/TLS configuration (Let's Encrypt paths)
- Modern SSL ciphers (TLS 1.2, 1.3)
- Security headers (HSTS, X-Frame-Options, CSP, etc.)
- Gzip compression
- Rate limiting zones for:
  - Authentication endpoints (strict)
  - API endpoints (moderate)
  - Health checks (no limit)
- WebSocket support (if needed)
- Proxy headers (X-Real-IP, X-Forwarded-For, etc.)
- Access and error logging
- Upstream configuration with health checks
- Client body size limits

**Template**:
```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=<project>_auth:10m rate=5r/s;
limit_req_zone $binary_remote_addr zone=<project>_api:10m rate=10r/s;

# Upstream
upstream <project>_backend {
    server localhost:<backend_port>;
}

# HTTP → HTTPS redirect
server {
    listen 80;
    server_name api.<domain>;
    location /.well-known/acme-challenge/ { root /var/www/certbot; }
    location / { return 301 https://$server_name$request_uri; }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name api.<domain>;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/api.<domain>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.<domain>/privkey.pem;

    # Proxy configuration
    location / {
        proxy_pass http://<project>_backend;
        # Headers...
    }
}
```

### 4. **.github/workflows/deploy.yml**
Create GitHub Actions CI/CD workflow:

**Requirements**:
- Trigger on `push to main` and `workflow_dispatch`
- Multi-job pipeline:
  1. **Test Job**: Linting, tests, coverage
  2. **Build Job**: Docker image build & export
  3. **Deploy Job**: Blue-Green deployment to server
  4. **Rollback Job**: Manual rollback capability
- Service containers for databases during testing
- Artifact upload/download for Docker image
- SSH deployment via GitHub Secrets
- Health checks before traffic switch
- Automatic rollback on failure
- Notifications (optional)

**Required GitHub Secrets**:
```
SERVER_HOST           # Server IP or hostname
SERVER_USER           # SSH username
SERVER_SSH_KEY        # Private SSH key
SERVER_PORT           # SSH port (default: 22)
DATABASE_URL          # Production database URL
REDIS_URL             # Production Redis URL
SECRET_KEY            # Application secret key
[Additional secrets based on project needs]
```

### 5. **.env.production.example**
Create production environment template:

**Requirements**:
- All environment variables with placeholder values
- Comments explaining each variable
- Security warnings for secrets
- Instructions to copy and fill in actual values
- Database connection strings using Docker service names
- Never commit actual `.env.production` to git

### 6. **scripts/deploy/deploy.sh** (Optional)
Manual deployment script for emergencies:

**Requirements**:
- Build Docker image locally
- Create timestamped release directory
- Run health checks
- Blue-Green deployment logic
- Automatic rollback on failure
- Cleanup old releases (keep last 5)

### 7. **scripts/deploy/rollback.sh** (Optional)
Manual rollback script:

**Requirements**:
- Find previous release
- Confirmation prompt
- Stop current, start previous
- Health checks
- Update symlinks

## Project-Specific Considerations

When generating these files, ask the user or detect:

1. **Technology Stack**:
   - Programming language and version (Python, Node.js, Go, etc.)
   - Framework (FastAPI, Express, Django, etc.)
   - Dependencies file (requirements.txt, package.json, go.mod)

2. **Database Requirements**:
   - Database type (PostgreSQL, MySQL, MongoDB, etc.)
   - Database migrations (Alembic, Prisma, etc.)
   - Initial setup scripts

3. **Cache/Queue**:
   - Redis, Memcached, RabbitMQ, etc.

4. **Special Features**:
   - WebSocket support
   - File uploads
   - Background workers
   - Scheduled tasks (cron jobs)
   - ML models (volume mounts)

5. **External Services**:
   - Third-party APIs
   - OAuth providers
   - Cloud services (AWS, Azure, GCP)

6. **Port Assignment**:
   - What project number is this? (determines base port)
   - How many additional ports needed?

7. **Domain**:
   - What domain/subdomain will be used?

## Security Checklist

Ensure the generated configuration includes:

- [ ] Non-root user in Docker container
- [ ] Read-only file systems where possible
- [ ] No secrets in Dockerfiles or docker compose files
- [ ] Environment variables for all secrets
- [ ] SSL/TLS with modern ciphers
- [ ] Security headers (HSTS, CSP, etc.)
- [ ] Rate limiting on sensitive endpoints
- [ ] CORS configuration
- [ ] Resource limits (prevent DoS)
- [ ] Health check endpoints
- [ ] Proper logging (no sensitive data)

## Performance Optimizations

Include these optimizations:

- [ ] Docker layer caching
- [ ] Multi-stage builds for smaller images
- [ ] Gzip compression in Nginx
- [ ] Connection pooling for databases
- [ ] Redis for caching
- [ ] Keepalive connections
- [ ] Resource reservations and limits

## Logging

The generated configuration should:

- [ ] Use structured logging (JSON format)
- [ ] Proper log rotation settings
- [ ] Health check endpoints for availability monitoring

## Deployment Instructions for User

After generating the files, provide these instructions:

### Initial Server Setup (One-Time)

If the server is not yet set up, run on the Ubuntu server:
```bash
sudo bash scripts/deploy/setup-server.sh
```

This sets up Docker, Nginx, firewall, and creates the project structure.

### Project-Specific Setup

1. **Assign Project Port**:
   ```bash
   # Use port calculator: 8000 + (N × 100)
   # N = project number (1, 2, 3, etc.)
   ```

2. **Create Project on Server**:
   ```bash
   sudo /opt/deploy/scripts/new-project.sh <project-name> <domain> <base-port>

   # Example:
   sudo /opt/deploy/scripts/new-project.sh myapp api.myapp.com 8100
   ```

3. **Configure GitHub Secrets**:
   Go to GitHub repo → Settings → Secrets → Actions → New repository secret

   Add all required secrets from the list above.

4. **Get SSL Certificate**:
   ```bash
   sudo certbot --nginx -d api.<domain>
   ```

5. **Create Production Environment File**:
   ```bash
   cp .env.production.example .env.production
   # Edit .env.production with actual values
   # Upload to server at /opt/projects/<project-name>/.env.production
   ```

6. **Deploy**:
   ```bash
   # Automatic via GitHub Actions (push to main branch)
   git push origin main

   # Or manual deployment:
   bash scripts/deploy/deploy.sh
   ```

### Verify Deployment

```bash
# Check health
curl https://api.<domain>/health

# Check logs
docker logs <project>_backend

# Check all containers
docker ps | grep <project>
```

## Example Output Structure

After running this prompt, the AI should generate:

```
<project-root>/
├── Dockerfile.prod
├── docker compose.prod.yml
├── .env.production.example
├── .github/
│   └── workflows/
│       └── deploy.yml
├── nginx/
│   ├── <project-name>.conf
│   └── nginx.conf (if custom needed)
└── scripts/
    └── deploy/
        ├── deploy.sh
        ├── rollback.sh
        └── health-check.sh
```

## Testing the Configuration

After generation, test locally:

```bash
# Build production image
docker build -f Dockerfile.prod -t myapp:test .

# Test docker compose
docker compose -f docker compose.prod.yml config

# Test Nginx config
nginx -t -c nginx/<project>.conf
```

## Common Issues and Solutions

### Port Conflicts
- Always use the port formula: 8000 + (N × 100)
- Check `docker ps` and `netstat -tlnp` for used ports

### SSL Certificate Issues
- Ensure DNS points to server before running Certbot
- Use HTTP-01 challenge (requires port 80 open)
- Certificates auto-renew via cron

### Docker Permission Denied
- Add user to docker group: `sudo usermod -aG docker $USER`
- Log out and log back in

### Health Check Failing
- Ensure health endpoint returns 200 OK
- Check startup time (increase `start_period` if needed)
- Verify container can access database/redis

### Deployment Fails
- Check GitHub Actions logs
- Verify all secrets are set correctly
- SSH key must have no passphrase
- Server must accept SSH key authentication

## Advanced Configurations

### Horizontal Scaling

To run multiple backend instances:

```yaml
# In docker compose.prod.yml
backend:
  deploy:
    replicas: 3
```

Update Nginx upstream:
```nginx
upstream myapp_backend {
    least_conn;
    server localhost:8101;
    server localhost:8102;
    server localhost:8103;
}
```

### Database Read Replicas

Add read replicas in docker compose and use read/write splitting in application.

### Background Workers

Add worker service in docker compose:
```yaml
worker:
  build: .
  command: python worker.py
  depends_on:
    - redis
```

### Scheduled Tasks

Use cron in container or add a scheduler service:
```yaml
scheduler:
  build: .
  command: python scheduler.py
```

## Validation Checklist

Before finalizing, verify:

- [ ] All files generated successfully
- [ ] No hardcoded secrets
- [ ] Ports don't conflict with existing projects
- [ ] Health checks defined
- [ ] Nginx config syntax valid
- [ ] Docker builds successfully
- [ ] GitHub workflow YAML is valid
- [ ] Environment variables documented
- [ ] README includes deployment steps

## Final Notes

This prompt is designed to be pasted into Cursor AI, ChatGPT, Claude, or any AI coding assistant when setting up a new backend project. The AI should:

1. Ask clarifying questions about the project
2. Generate all necessary files
3. Customize based on technology stack
4. Provide deployment instructions
5. Include troubleshooting tips

The generated configuration will be compatible with the existing multi-project server infrastructure and follow all established best practices for security, performance, and reliability.

---

**Generated by**: Claude Code Multi-Project Deployment System
**Compatible with**: Ubuntu 20.04+, Docker 20.10+, Nginx 1.18+
**Last Updated**: 2026-01-16
