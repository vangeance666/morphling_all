from .task import *
class Submission:

	def __init__(self, file_sha_256):
		self.hash = file_sha_256
		self.tasks: list = [] #list of tasks that are related
		self.auto_resubmit: bool = True


	def add_task(self, task: Task):
		try:
			self.tasks.append(task)
		except:
			return False
		return True

	def get_info(self):

		return {
			"hash": self.hash,
			"tasks": [x.get_info() for x in self.tasks],
			"auto_resubmit": self.auto_resubmit
		}
