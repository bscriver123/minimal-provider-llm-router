from functools import partial

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from app.deps.config import get_settings
from app.services.market_scan import fill_open_instances_in_market

scheduler = AsyncIOScheduler()


def start_scheduler() -> None:
    logger.info("Starting Market scheduler...")
    settings = get_settings()
    job_func = partial(fill_open_instances_in_market, settings=settings)
    scheduler.add_job(job_func, "interval", seconds=settings.market_scan_interval)
    scheduler.start()
    logger.info("Market scheduler started.")


def stop_scheduler() -> None:
    logger.info("Stopping Market scheduler...")
    scheduler.shutdown()
    logger.info("Market scheduler stopped.")
