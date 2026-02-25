from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

from database import get_setting, set_setting, cleanup_old_news
from fetcher import fetch_all_news
from config import FETCH_INTERVAL_MINUTES, MAX_NEWS_AGE_HOURS

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def scheduled_fetch():
    import asyncio
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(fetch_all_news())
        loop.close()
    except Exception as e:
        logger.error(f"Scheduled fetch error: {e}")


def start_scheduler():
    interval = int(get_setting("fetch_interval_minutes") or FETCH_INTERVAL_MINUTES)
    
    scheduler.add_job(
        scheduled_fetch,
        trigger=IntervalTrigger(minutes=interval),
        id="fetch_news",
        replace_existing=True
    )
    
    scheduler.add_job(
        lambda: cleanup_old_news(MAX_NEWS_AGE_HOURS),
        trigger=IntervalTrigger(hours=1),
        id="cleanup_old",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"Scheduler started. Fetch interval: {interval} minutes")


def update_fetch_interval(minutes: int):
    scheduler.reschedule_job(
        "fetch_news",
        trigger=IntervalTrigger(minutes=minutes)
    )
    set_setting("fetch_interval_minutes", str(minutes))
    logger.info(f"Fetch interval updated to {minutes} minutes")
