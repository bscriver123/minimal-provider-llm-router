from contextlib import asynccontextmanager
from typing import AsyncGenerator, Final

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.deps.config import Settings, get_settings
from app.endpoints import completions_router
from app.schedulers.agent_market_scheduler import start_scheduler as start_agent_market_scheduler
from app.schedulers.agent_market_scheduler import stop_scheduler as stop_agent_market_scheduler

APP_VERSION: Final[str] = "0.0.2"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger.info("Starting up FastAPI application...")
    start_agent_market_scheduler()
    yield
    logger.info("Shutting down FastAPI application...")
    stop_agent_market_scheduler()


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
    settings: Settings = get_settings()
    uvicorn.run(app, host="0.0.0.0", port=settings.web_port)


if __name__ == "__main__":
    run()
