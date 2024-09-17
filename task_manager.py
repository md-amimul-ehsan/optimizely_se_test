import os
import pickle
from datetime import datetime


class Task:

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False
        self.created_at = datetime.now().isoformat()
        self.completed_at = None


class TaskManager:
    file_path = "tasks.pkl"

    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title, description):
        task = self.storage.get_task(title)
        if task is not None and task.title == title:
            return None

        task = Task(title, description)
        self.storage.save_task(task)

        return task

    def complete_task(self, title):
        task = self.storage.get_task(title)

        if not task:
            return False
        elif task.completed:
            return True

        task.completed = True
        task.completed_at = datetime.now().isoformat()

        self.storage.update_task(task)

        return True

    def list_tasks(self, include_completed=False):
        tasks = self.storage.get_all_tasks()
        tasks = [task for task in tasks if include_completed or not task.completed]
        return tasks

    def generate_report(self):
        tasks = self.storage.get_all_tasks()
        total_tasks = len(tasks)
        completed_task_list = [task for task in tasks if task.completed]
        completed_tasks = len(completed_task_list)

        report = {
            "total": total_tasks,
            "completed": completed_tasks,
            "pending": total_tasks - completed_tasks,
            "average completion time": get_average_completion_time(completed_task_list)
        }

        return report

    def load_tasks(self):
        if not os.path.exists(self.file_path):
            open(self.file_path, "wb")
            return
        elif os.path.getsize(self.file_path) == 0:
            return

        with open(self.file_path, "rb") as file:
            self.storage.save_tasks(pickle.load(file))

    def save_tasks_to_file(self):
        with open(self.file_path, "wb") as file:
            pickle.dump(self.storage.get_all_tasks(), file)


def get_average_completion_time(completed_task_list):
    if len(completed_task_list) == 0:
        return "N/A"

    sum_of_completion_times_in_seconds = sum(
        (datetime.fromisoformat(task.completed_at) - datetime.fromisoformat(task.created_at)).total_seconds()
        if task.completed_at else 0
        for task in completed_task_list
    )

    if sum_of_completion_times_in_seconds == 0:
        return "N/A"

    avg_time_in_seconds = int(sum_of_completion_times_in_seconds / len(completed_task_list))

    minutes_part, seconds_part = divmod(avg_time_in_seconds, 60)
    hours_part, minutes_part = divmod(minutes_part, 60)

    return f"{hours_part:02}:{minutes_part:02}:{seconds_part:02}"
