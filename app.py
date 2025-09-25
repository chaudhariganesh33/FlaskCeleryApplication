from flask import Flask, render_template, redirect
from tasks import *

app = Flask(__name__)

celery_tasks = []

@app.route("/")
def home():
    task_list = []
    if len(celery_tasks) > 0:
        for task in celery_tasks:
            task_list.append({'id': task.id, 'status': task.state})
    return render_template('home.html', context={'title': 'Home', 'tasks': task_list})


@app.route("/add")
def add_task():
    task = run_task.delay()
    celery_tasks.append(task)
    return redirect("/")


@app.route("/clear_tasks")
def clear_tasks():
    for task in celery_tasks:
        if task.state == "SUCCESS":
            celery_tasks.remove(task)
    return redirect("/")


if __name__ == "__main__":
    app.run()