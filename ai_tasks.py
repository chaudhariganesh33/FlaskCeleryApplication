import time


def run_task_for_n_seconds(n, task_id):
    try:
        start_time = time.time()
        print(f"Started {task_id} task for {n} seconds")
        while time.time() - start_time < n:
            time.sleep(1)
        print(f"{task_id} execution completed")
        return True
    except Exception as err:
        return False
