import json
import sys
import os

FILE = 'tasks.json'

def load_tasks():
    try:
        if os.path.exists(FILE):
            with open(FILE, 'r') as f:
                return json.load(f)
        return []
    except json.JSONDecodeError:
        print("Error: tasks.json is corrupted. Resetting to empty list.")
        return []
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return []

def save_tasks(tasks):
    try:
        with open(FILE, 'w') as f:
            json.dump(tasks, f, indent=4)
    except Exception as e:
        print(f"Error saving tasks: {e}")

def add_task(description):
    tasks = load_tasks()
    task_id = max([task["id"] for task in tasks] + [0]) + 1
    tasks.append({"id": task_id, "description": description, "status": "todo"})
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            save_tasks(tasks)
            print(f"Task updated successfully (ID: {task_id})")
            return
    print("Error: Task not found")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task deleted successfully (ID: {task_id})")

def mark_in_progress(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            save_tasks(tasks)
            print(f"Task marked in-progress successfully (ID: {task_id})")
            return
    print("Error: Task not found")

def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            save_tasks(tasks)
            print(f"Task marked done successfully (ID: {task_id})")
            return
    print("Error: Task not found")

def list_tasks(status=None):
    tasks = load_tasks()
    filtered_tasks = [task for task in tasks if status is None or task["status"] == status]
    if not filtered_tasks:
        print("No tasks found.")
    else:
        for task in filtered_tasks:
            print(f"{task['id']}: {task['description']} ({task['status']})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: task-cli [command] [args]")
        print("Commands: add <description>, update <id> <description>, delete <id>, mark-in-progress <id>, mark-done <id>, list, list todo, list done, list in-progress")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif command == "update" and len(sys.argv) > 3:
        try:
            update_task(int(sys.argv[2]), " ".join(sys.argv[3:]))
        except ValueError:
            print("Error: Task ID must be a number")
    elif command == "delete" and len(sys.argv) > 2:
        try:
            delete_task(int(sys.argv[2]))
        except ValueError:
            print("Error: Task ID must be a number")
    elif command == "mark-in-progress" and len(sys.argv) > 2:
        try:
            mark_in_progress(int(sys.argv[2]))
        except ValueError:
            print("Error: Task ID must be a number")
    elif command == "mark-done" and len(sys.argv) > 2:
        try:
            mark_done(int(sys.argv[2]))
        except ValueError:
            print("Error: Task ID must be a number")
    elif command == "list":
        list_tasks()
    elif command in ["list", "list", "list", "list"] and len(sys.argv) > 2:
        status = sys.argv[2].replace("list ", "")
        if status in ["todo", "done", "in-progress"]:
            list_tasks(status)
        else:
            print("Error: Invalid status. Use 'todo', 'done', or 'in-progress'")
    else:
        print("Error: Invalid command or arguments")
