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

# Define the lifespan of the FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger.info("Starting up FastAPI application...")
    # Start the market scheduler
    start_market_scheduler()
    yield
    logger.info("Shutting down FastAPI application...")
    # Stop the market scheduler
    stop_market_scheduler()

# Create the FastAPI application instance
app = FastAPI(version=APP_VERSION, debug=True, lifespan=lifespan)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the completions router for handling API requests
app.include_router(completions_router)

# Function to run the application using Uvicorn
def run():
    # Retrieve application settings
    settings: Settings = get_settings()
    # Run the Uvicorn server with the specified host and port
    uvicorn.run(app, host="0.0.0.0", port=settings.web_port)

# Entry point for running the application
if __name__ == "__main__":
    run()
