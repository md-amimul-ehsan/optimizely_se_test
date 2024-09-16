class Storage:

	def __init__(self):
		self.__tasks = []

	def save_task(self, task):
		self.__tasks.append(task)

	def update_task(self, updated_task):
		for i, task in enumerate(self.__tasks):
			if task.title == updated_task.title:
				self.__tasks[i] = updated_task
				break

	def get_task(self, title):
		for task in self.__tasks:
			if task.title == title:
				return task
		return None

	def get_all_tasks(self):
		return list(self.__tasks)

	def clear_all_tasks(self):
		self.__tasks = []

	def save_tasks(self, tasks):
		self.__tasks = tasks
