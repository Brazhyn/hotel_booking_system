from celery import Celery

from src.config import settings


celery_instance = Celery(
    main="tasks",
    broker=settings.REDIS_URL,
    include=["src.tasks.tasks"] # absolute path to tasks.py
)

celery_instance.conf.beat_schedule = {
    "tasks": {
        "task": "booking_today_checkin",
        "schedule": 60 * 60,
    }
}