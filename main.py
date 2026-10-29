# main.py
import logging
import sys
from fastapi import FastAPI
from loguru import logger
from app.config.config import settings
from app.routes import api_router
from app.exception_handler import register_exception_handlers

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

# Loguru's default sink logs at DEBUG, so replace it with one using LOG_LEVEL
logger.remove()
logger.add(sys.stderr, level=settings.LOG_LEVEL.upper())

app = FastAPI(
    title="Smoothie Registration API",
    version="1.0.0",
    description="API for registering customers for smoothie subscriptions."
)

register_exception_handlers(app)  # Register custom exception handlers

# Include your API router with a prefix
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True, log_level=settings.LOG_LEVEL.lower())