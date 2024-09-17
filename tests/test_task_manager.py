import unittest
from datetime import datetime
from unittest.mock import MagicMock

from task_manager import Task, TaskManager


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.storage = MagicMock()
        self.manager = TaskManager(self.storage)

    def test_add_task(self):
        task = self.manager.add_task("Test Task", "Description")
        self.storage.save_task.assert_called_once()
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Description")

        self.storage.get_task.return_value = task
        task = self.manager.add_task("Test Task", "Description")
        self.assertEqual(task, None)

    def test_list_tasks_exclude_completed(self):
        tasks = [
            Task("Task 1", "Description 1"),
            Task("Task 2", "Description 2"),
            Task("Task 3", "Description 3")
        ]
        tasks[1].completed = True

        self.storage.get_all_tasks.return_value = tasks
        result = self.manager.list_tasks()

        self.assertEqual(len(result), 2)
        self.assertNotIn(tasks[1], result)

    def test_generate_report(self):
        tasks = [
            Task("Task 1", "Description 1"),
            Task("Task 2", "Description 2"),
            Task("Task 3", "Description 3")
        ]
        tasks[0].completed = True
        tasks[1].completed = True

        self.storage.get_all_tasks.return_value = tasks
        report = self.manager.generate_report()

        self.assertEqual(report["total"], 3)
        self.assertEqual(report["completed"], 2)
        self.assertEqual(report["pending"], 1)

    def test_complete_nonexistent_task(self):
        self.storage.get_task.return_value = None
        result = self.manager.complete_task("Non-existent Task")
        self.assertFalse(result)

    def test_generate_report_average_completion_time(self):
        tasks = [
            Task("Task 1", "Description 1"),
            Task("Task 2", "Description 2"),
            Task("Task 3", "Description 3")
        ]

        tasks[0].completed = True
        tasks[1].completed = True
        tasks[2].completed = True

        tasks[0].created_at = datetime(2024, 9, 17, 12, 0, 0).isoformat()
        tasks[0].completed_at = datetime(2024, 9, 17, 13, 0, 0).isoformat() #1 hour
        tasks[1].created_at = datetime(2024, 9, 17, 14, 0, 0).isoformat()
        tasks[1].completed_at = datetime(2024, 9, 17, 16, 0, 0).isoformat() #2 hours
        tasks[2].created_at = datetime(2024, 9, 17, 17, 0, 0).isoformat()
        tasks[2].completed_at = datetime(2024, 9, 17, 20, 0, 0).isoformat() #3 hours

        self.storage.get_all_tasks.return_value = tasks
        report = self.manager.generate_report()

        self.assertEqual(report["average completion time"], "02:00:00")



if __name__ == "__main__":
    unittest.main()
