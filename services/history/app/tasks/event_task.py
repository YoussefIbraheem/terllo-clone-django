from logging import getLogger
from celery import Celery
import asyncio
from app.core.config import settings
from kombu import Exchange, Queue
from app.services.event_service import create_event
from app.db.database import connect_to_mongo
from pymongo import MongoClient
from beanie import init_beanie
from app.models.event import Event
from datetime import datetime, timezone
from app.schemas.event_schema import EventCreate

app = Celery(
    "tasks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)

logger = getLogger(__name__)

_dlx = Exchange("dlx", type="direct", durable=True)


app.conf.update(
    task_ignore_result=True,
    task_routes=[
        {"app.tasks.event_task.process_event_background": {"queue": "history"}}
    ],
    task_queue=[
        Queue(
            "history",
            Exchange("history", type="direct", durable=True),
            queue_arguments={
                "x-dead-letter-exchange": "dlx",
                "x-dead-letter-routing-key": "history.failed",
            },
        ),
        Queue("history.failed", _dlx, routing_key="history.failed", durable=True),
    ],
)



@app.task(
    name="app.tasks.event_task.process_event_background",
    autoretry_for=(Exception,),
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=60,
    ignore_results=True,
)
def process_event_background(event_data):
    try:
        event_id = asyncio.run(create_event(event_data))
        logger.info(f"Event saved successfully with ID: {event_id}")
        print(f"[HISTORY WORKER] Event triggered with ID: {event_id}")
        return
    except Exception as e:
        logger.error(f"Error processing history event: {e}", exc_info=True)
        print(f"[HISTORY WORKER] Error: {e}")
        raise
