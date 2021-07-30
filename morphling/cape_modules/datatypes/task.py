from restapis.capeapi import *

class Task:

	STATUS_NEW = "new" # submit thread
	STATUS_SUBMITED = "submit"
	STATUS_RUNNING = "running"
	STATUS_PROCESSING = "processing" 
	STATUS_REPORTED = "reported" #evaluate thread
	STATUS_EVALUATED = "evaluated"
	STATUS_ERROR = "error"
	STATUS_FAILED_ANALYSIS = "failed_analysis"

	def __init__(self, file_path=None, machine_name=None, to_install=None, reg_to_add=None, status="new"):
		self.file_path = file_path
		self.machine_name = machine_name # machine name

		self.status = status # reported | failed | processing # How to store related cases?

		self.id: int = None

		self.resubmit_cap = 1
		self.do_retune: bool = True

		self.do_resubmit: bool = True
		self.resubmited: bool = False
		self.to_install: list = to_install or []

		self.reg_keys_to_add: list = reg_to_add or []

		self.mal_score: float = None

		self.previous_task: Task = None

		self.signatures: list = []
		self.tuners_to_apply: list = []

		self.force_resubmit: bool = False

	def get_info(self):
		return {
			"file_path": self.file_path
			, "machine_name": self.machine_name
			, "status": self.status
			, "id": self.id
			, "resubmit_cap" : self.resubmit_cap
			, "do_retune": self.do_retune
			, "do_resubmit": self.do_resubmit
			, "resubmited": self.resubmited
			, "to_install": self.to_install
			, "reg_keys_to_add": [x.replace('\\', '/') for x in self.reg_keys_to_add] 
			, "mal_score": self.mal_score
			, "previous_task": self.previous_task.get_info() if self.previous_task else None
			, "signatures": [x.get_info() for x in self.signatures]
			, "tuners_to_apply": [x.get_info() for x in self.tuners_to_apply]
		}

	def sync_status_with_cape(self, cape_api: CapeApi):

		""" Only update those cases that are:
			Not new, not evaluated 
		"""
		
		if (self.status != self.STATUS_NEW) \
			and (self.status != self.STATUS_REPORTED) \
			and (self.status != self.STATUS_EVALUATED):
			# and (self.status != self.STATUS_SUBMITED) \

			# print("Task is New or Evalluated, skip.")
			# return 


			# print("Task sync with cape self.id: ", self.id)
			# print("Before status is: ", self.status)
			try:
				task_details = cape_api.view_task(self.id)				
				self.status = task_details['data']['status']
				# print("After status is: ", self.status)
				self.mal_score = cape_api.get_report(self.id)['malscore']
			except:
				self.status = self.STATUS_ERROR
				self.mal_score = None
				return False
				# print("Failed to sync task status against CAPE details")

		return False

	def submit(self, cape_api: CapeApi) -> bool:

		if not self.file_path or not self.machine_name:
			return False

		try:
			res = cape_api.submit_file_sample(self.file_path, self.machine_name)

			if not res:
				return False

			if res['error']:
				return False

			self.id = res['data']['task_ids'][0]
			self.status = self.STATUS_SUBMITED

			return True
			
		except Exception as e:
			return False


	def parse_cape_task_data(self, reply: dict):
		self.machine_name = reply['machine']
		self.status = reply['status']
		self.id = reply['id']

	def is_reported(self) -> bool:
		return self.status == self.STATUS_REPORTED if self.status else False

	






