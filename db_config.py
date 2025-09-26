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
    
def execute_query(query, params=None, fetch=False, many=False):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                conn.commit()
                return True
    except Exception as e:
        print(f"DB Error: {e}")
        return None
    

def create_table():
    query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task_id VARCHAR(150) NOT NULL,
            task_status VARCHAR(100),
            date_added date DEFAULT CURRENT_TIMESTAMP
        );
    """
    return execute_query("DROP TABLE IF EXISTS tasks;") and execute_query(query)

def add_task_to_db(task_id, task_status):
    query = "INSERT INTO tasks (task_id, task_status) VALUES (%s, %s);"
    return execute_query(query, (task_id, task_status))
 
    
def update_task(task_id, task_status):
    query = "UPDATE tasks SET task_status = %s WHERE task_id = %s;"
    return execute_query(query, (task_status, task_id))


def remove_task(task_id):
    query = "DELETE FROM tasks WHERE task_id = %s;"
    return execute_query(query, (task_id,))


def get_completed_tasks():
    query = "SELECT * FROM tasks WHERE task_status = 'SUCCESS';"
    return execute_query(query, fetch=True)


def get_all_tasks():
    query = "SELECT * FROM tasks;"
    return execute_query(query, fetch=True)