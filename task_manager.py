import os
import pickle
from datetime import datetime


class Task:

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False
        self.created_at = datetime.now().isoformat()


class TaskManager:

    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title, description):
        task = self.storage.get_task(title)
        if task:
            return None
        task = Task(title, description)
        self.storage.save_task(task)
        return task

    def complete_task(self, title):
        task = self.storage.get_task(title)
        if task:
            task.completed = True
            task.completed_at = datetime.now().isoformat()
            self.storage.update_task(task)
            return True
        return False

    def list_tasks(self, include_completed=False):
        tasks = self.storage.get_all_tasks()
        tasks = [task for task in tasks if include_completed or not task.completed]
        return tasks

    def generate_report(self):
        tasks = self.storage.get_all_tasks()
        total_tasks = len(tasks)
        completed_task_list = [task for task in tasks if task.completed]
        completed_tasks = len(completed_task_list)

        # hours, minutes, seconds = get_average_completion_time(completed_task_list)

        report = {
            "total": total_tasks,
            "completed": completed_tasks,
            "pending": total_tasks - completed_tasks
            # "average completion time": (str(hours) + " hour(s) " if hours > 0 else "")
            #                            + (str(minutes) + " minute(s) " if minutes > 0 else "")
            #                            + str(seconds) + " second(s)"
        }

        return report

    def load_tasks(self):
        file_path = "tasks.pkl"

        if not os.path.exists(file_path):
            open(file_path, "wb")
            return
        elif os.path.getsize(file_path) == 0:
            return

        with open(file_path, "rb") as file:
            self.storage.save_tasks(pickle.load(file))

    def save_tasks_to_file(self):
        with open("tasks.pkl", "wb") as file:
            pickle.dump(self.storage.get_all_tasks(), file)


def get_average_completion_time(completed_task_list):
    if len(completed_task_list) == 0:
        return 0, 0, 0

    sum_of_completion_times_in_seconds = sum(
        (task.completed_at - task.created_at).total_seconds() if task.completed_at else 0
        for task in completed_task_list)

    avg_completion_time_in_seconds = int(sum_of_completion_times_in_seconds / len(completed_task_list))

    avg_completion_time_minutes_part, avg_completion_time_seconds_part = divmod(avg_completion_time_in_seconds, 60)
    avg_completion_time_hours_part, avg_completion_time_minutes_part = divmod(avg_completion_time_minutes_part, 60)

    return avg_completion_time_hours_part, avg_completion_time_minutes_part, avg_completion_time_seconds_part