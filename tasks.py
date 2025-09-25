from celery import Celery
from ai_tasks import *

celery_app = Celery("tasks", broker="redis://127.0.0.1:6379/0")
celery_app.conf.result_backend = "redis://127.0.0.1:6379/1"


@celery_app.task
def run_task():
    task_id = run_task.request.id
    run_task_for_n_seconds(30, task_id)