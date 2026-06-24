import sys
import json
import os
from datetime import datetime

file_name="taskys.json"

def load_tasks(file_name):
    if not os.path.exists(file_name):
        return []
    with open(file_name,"r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []
def save_tasks(tasks,file_name="taskys.json"):
    with open(file_name,"w") as file:
        json.dump(tasks,file,indent=3)


def add_tasks(description):
    tasks = load_tasks(file_name)

    if tasks:
        newID = tasks[-1]["id"]+1
    else:
        newID = 1

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    newTask={"id":newID,
             "description":description,
             "status":"todo",
             "createdAt":current_time,
             "updatedAt":current_time
             }

    tasks.append(newTask)
    save_tasks(tasks)
    print(f"Task added succesfully (ID: {newID})")

def update_tasks(task_id,newDescription):
    tasks = load_tasks(file_name)
    for i in tasks:
        if i["id"]==task_id:
            i["description"] = newDescription
            i["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            print(f"Task updated succesfully (ID: {task_id})")
            return
        else:
            print(f"Task with ID {task_id} is not found")

def delete_tasks(task_id):
    tasks = load_tasks(file_name)

    newTasks =[task for task in tasks if task["id"]!=task_id]

    if len(tasks) == len(newTasks):
        print("Task is not found")
        return
    else:
        save_tasks(newTasks)
        print(f"Task deleted succesfully (ID: {task_id})")

def change_status(task_id,new_status):
    tasks = load_tasks(file_name)
    taskFound = False

    for task in tasks:
        if task["id"]==task_id:
            task["status"]=new_status
            task["updatedAt"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            taskFound=True
            break

    if taskFound==True:
        save_tasks(tasks)
        print(f"Task {task_id} marked as {new_status}")
        return
    else:
        print(f"Task {task_id} is not found {new_status}")
        return

def list_tasks(status_filter=None):
    tasks=load_tasks(file_name)

    if not tasks:
        print("No tasks found")
        return

    if status_filter:
        filtered_tasks=[]
        for task in tasks:
            if task["status"]==status_filter:
                filtered_tasks.append(task)
    else:
        filtered_tasks = tasks

    if filtered_tasks==[]:
        print(f"No tasks found with status {status_filter}")
        return
    for task in filtered_tasks:
        print(f"[{task['id']}] {task['description']}  | {task['status']}")

def main():
    if len(sys.argv)<2:
        print("Usage: python main.py taskys.json command,argument")
        return
    command = sys.argv[1]

    if command == "add":
        if len(sys.argv)<3:
            print("Please provide a description of the task")
            return
        add_tasks(sys.argv[2])

    elif command == "update":
        if len(sys.argv)<4:
            print("Please provide a description of the task")
            return
        update_tasks(int(sys.argv[2]),sys.argv[3])

    elif command == "delete":
        if len(sys.argv)<3:
            print("Please provide a description of the task")
            return
        delete_tasks(int(sys.argv[2]))

    elif command == "mark-in-progress":
        if len(sys.argv)<3:
            print("Please provide a description of the task")
            return
        change_status(int(sys.argv[2]),"in-progress")

    elif command == "mark-done":
        if len(sys.argv)<3:
            print("Please provide a description of the task")
            return
        change_status(int(sys.argv[2]),"done")
    elif command == "list":
        status_filter = sys.argv[2] if len(sys.argv)>2 else None
        list_tasks(status_filter)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()














