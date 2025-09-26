from celery import Celery
from ai_tasks import *
import requests

celery_app = Celery("tasks", broker="redis://127.0.0.1:6379/0")
celery_app.conf.result_backend = "redis://127.0.0.1:6379/1"


@celery_app.task
def run_task():
    task_id = run_task.request.id
    run_task_for_n_seconds(20, task_id)


@celery_app.task
def call_update_api():
    requests.get("http://127.0.0.1:5000/update")


celery_app.conf.beat_schedule = {
    "run-me-every-ten-seconds": {
        "task": "tasks.call_update_api",
        "schedule": 10.0
    }
}