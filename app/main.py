# Import necessary modules and dependencies
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Final

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.deps.config import Settings, get_settings
from app.endpoints import completions_router
from app.schedulers.market_scheduler import start_scheduler as start_market_scheduler
from app.schedulers.market_scheduler import stop_scheduler as stop_market_scheduler

# Define the application version
APP_VERSION: Final[str] = "0.0.2"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Lifecycle management for the FastAPI application
    logger.info("Starting up FastAPI application...")
    start_market_scheduler()  # Start the market scheduler
    yield
    logger.info("Shutting down FastAPI application...")
    stop_market_scheduler()  # Stop the market scheduler


# Initialize the FastAPI application with CORS middleware
app = FastAPI(version=APP_VERSION, debug=True, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
app.include_router(completions_router)  # Include the completions router


def run():
    # Run the FastAPI application using Uvicorn
    settings: Settings = get_settings()
    uvicorn.run(app, host="0.0.0.0", port=settings.web_port)


if __name__ == "__main__":
    # Entry point for running the application
    run()
