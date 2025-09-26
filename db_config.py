import os
import psycopg2


def get_connection():
    try:
        conn = psycopg2.connect(
            host = "localhost",
            database = "flask_db",
            user = os.environ['DB_USERNAME'],
            password = os.environ['DB_PASSWORD']
        )
        return conn
    except:
        return None
    

def create_table():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS tasks;')
        cur.execute('CREATE TABLE tasks (id serial PRIMARY KEY,'
                                        'task_id VARCHAR (150) NOT NULL,'
                                        'task_status VARCHAR (100),'
                                        'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except:
        return False
    

def add_task_to_db(task_id, task_status):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (task_id, task_status)'
                    'VALUES (%s, %s)',
                    (task_id, task_status))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except:
        return 
    
    
def update_task(task_id, task_status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"UPDATE tasks SET task_status = '{task_status}' WHERE task_id = '{task_id}'")
    conn.commit()
    cur.close()
    conn.close()


def remove_task(task_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = f"DELETE FROM tasks WHERE task_id = '{task_id}';"
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except:
        return None


def get_completed_tasks():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE task_status = 'SUCCESS';")
        completed_tasks = cur.fetchall()
        cur.close()
        conn.close()
        return completed_tasks
    except:
        return None


def get_all_tasks():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks;")
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        return tasks
    except:
        return None