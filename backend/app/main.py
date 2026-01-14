from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import close_db
from app.services.redis_service import redis_service
from app.middleware.rate_limit import rate_limit_middleware

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.is_production else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting MuscleUp Vision API...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")

    # Initialize Redis
    await redis_service.connect()

    yield

    # Shutdown
    logger.info("🛑 Shutting down MuscleUp Vision API...")
    await close_db()
    await redis_service.close()
    logger.info("Connections closed")


# Create FastAPI application
app = FastAPI(
    title="MuscleUp Vision API",
    description="AI-powered computer vision fitness tracking backend",
    version="1.0.0",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    lifespan=lifespan
)

# Configure CORS with credentials support
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,  # CRITICAL: Required for cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "X-CSRF-Token"],  # Allow CSRF header
    expose_headers=["X-CSRF-Token"],  # Expose CSRF token to frontend
)


# Add rate limiting middleware
@app.middleware("http")
async def add_rate_limiting(request: Request, call_next):
    """Apply rate limiting to auth endpoints"""
    await rate_limit_middleware(request)
    response = await call_next(request)
    return response


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }


@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "message": "MuscleUp Vision API",
        "version": "1.0.0",
        "docs": "/docs" if not settings.is_production else "disabled in production"
    }


# Include routers
from app.api.v1 import auth, users, plans, workouts, stats, achievements, vision

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(plans.router, prefix="/api/v1/plans", tags=["plans"])
app.include_router(workouts.router, prefix="/api/v1/workouts", tags=["workouts"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["stats"])
app.include_router(achievements.router, prefix="/api/v1/achievements", tags=["achievements"])
app.include_router(vision.router, prefix="/api/v1/vision", tags=["vision"])
