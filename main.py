# Importing psycopg2 to be able to connect/interact with postgres directly with normal python code.
from psycopg2 import connect


# Creating a handy function to connect to the DB
def create_table():
    conn = connect(
        dbname="bincom_todo_list",
        user="Skibo555",
        password="4253",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS todo_items (
                    id SERIAL PRIMARY KEY,
                    task TEXT NOT NULL,
                    status BOOLEAN NOT NULL DEFAULT FALSE
                )''')
    conn.commit()
    cur.close()
    conn.close()

create_table()

def add_task(task):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO todo_items (task) VALUES (%s)", (task,))
    conn.commit()
    cur.close()
    conn.close()

def get_tasks():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, task, status FROM todo_items")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks

def update_task(task_id, new_task):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE todo_items SET task = %s WHERE id = %s", (new_task, task_id))
    conn.commit()
    cur.close()
    conn.close()

def mark_task_completed(task_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE todo_items SET status = TRUE WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()

def delete_task(task_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM todo_items WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()


# Creating UI from the command line to display what I have.
def menu():
    while True:
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Mark Task Completed")
        print("5. Delete Task")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            task = input("Enter task: ")
            add_task(task)
        elif choice == '2':
            tasks = get_tasks()
            for task in tasks:
                print(f"{task[0]}. {task[1]} - {'Completed' if task[2] else 'Pending'}")
        elif choice == '3':
            task_id = int(input("Enter task ID to update: "))
            new_task = input("Enter new task: ")
            update_task(task_id, new_task)
        elif choice == '4':
            task_id = int(input("Enter task ID to mark as completed: "))
            mark_task_completed(task_id)
        elif choice == '5':
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)
        elif choice == '6':
            break
        else:
            print("Invalid choice, please try again.")

menu()
