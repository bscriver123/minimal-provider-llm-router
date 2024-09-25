from functools import partial

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from app.deps.config import get_settings
from app.services.agent_market_scan import fill_open_instances_in_agent_market

scheduler = AsyncIOScheduler()


def start_scheduler() -> None:
    logger.info("Starting Agent Market scheduler...")
    settings = get_settings()
    job_func = partial(fill_open_instances_in_agent_market, settings=settings)
    scheduler.add_job(job_func, "interval", seconds=settings.agent_market_scan_interval)
    scheduler.start()
    logger.info("Agent Market scheduler started.")


def stop_scheduler() -> None:
    logger.info("Stopping Agent Market scheduler...")
    scheduler.shutdown()
    logger.info("Agent Market scheduler stopped.")
