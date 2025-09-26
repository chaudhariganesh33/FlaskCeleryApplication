from flask import Flask, render_template, redirect
from tasks import *
from db_config import *
from celery.result import AsyncResult

app = Flask(__name__)

@app.route("/")
def home():
    all_tasks = get_all_tasks()
    task_list = []
    if len(all_tasks) > 0:
        for task in all_tasks:
            task_list.append({'id': task[1], 'status': task[2], 'date_of_creation': task[3]})
    return render_template('home.html', context={'title': 'Home', 'tasks': task_list})


@app.route("/add")
def add_task():
    task = run_task.delay()
    add_task_to_db(task.id, task.state)
    return redirect("/")


@app.route("/update")
def update_tasks_status():
    all_tasks = get_all_tasks()
    for task in all_tasks:
        result = AsyncResult(task[1], app=celery_app)
        update_task(task[1], result.state)
    return redirect('/')


@app.route("/delete_task/<task_id>")
def delete_task(task_id):
    remove_task(task_id)
    return redirect("/")


@app.route("/clear_tasks")
def clear_tasks():
    all_tasks = get_all_tasks()
    for task in all_tasks:
        result = AsyncResult(task[1], app=celery_app)
        if result.state == "SUCCESS":
            remove_task(task[1])            
    return redirect("/")


if __name__ == "__main__":
    app.run()