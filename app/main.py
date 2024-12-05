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
# Define the lifespan of the FastAPI application, managing startup and shutdown events
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger.info("Starting up FastAPI application...")
    start_market_scheduler()
    yield
    logger.info("Shutting down FastAPI application...")
    stop_market_scheduler()


# Initialize the FastAPI application with CORS middleware and include the completions router
app = FastAPI(version=APP_VERSION, debug=True, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(completions_router)


def run():
    # Run the FastAPI application using Uvicorn
    settings: Settings = get_settings()
    uvicorn.run(app, host="0.0.0.0", port=settings.web_port)


if __name__ == "__main__":
    # Entry point for running the application
    run()
