from datatypes.task import *

from tuning.chocopackagetuner import *
from tuning.regtuner import *

from restapis.fogapi import *
from restapis.capeapi import *

class Machine:

	DEFAULT = "default"
	OFF = "off"
	READY = "ready"
	TUNING = "tuning"
	TUNED = "tuned"
	RUNNING = "running"
	STOPPED = "stopped"
	ERROR = "error"

	def __init__(self, label, username, password, hostname, status=None):

		self.label = label
		self.status = status or self.DEFAULT

		self.username = username
		self.password = password        
		self.hostname = hostname # This is the ip address

		# self._choco_tuner = ChocoPackageTuner(username, password, hostname) #Put credentials
		# self._reg_tuner = RegTuner(username, password, hostname)

		self.allocated_task = None
		self.locked: bool = False

	def get_info(self):
		return {
			"label": self.label
			, "status": self.status 
			, "username": self.username 
			, "password": self.password 
			, "hostname": self.hostname
			, "allocated_task": self.allocated_task.get_info() if self.allocated_task else None
		}

	def tune_choco_packages(self, task: Task) -> bool:
		try:
			self._choco_tuner.remote_install_packages(task.to_install)
		except Exception as e:
			print(e)
			return False
		return True

	def tune_reg_keys(self, task: Task) -> bool:
		try:
			print("Do nth for now")
			if task.reg_keys_to_add:
				self._reg_tuner.add_task_keys(task.reg_keys_to_add)
		except Exception as e:
			print(e)
			return False
		return True     

	def pingable(self) -> bool:
		""" Determine if host is up using icmp 

		Returns:
		    bool: True if host is pingable
		"""

		p = subprocess.Popen("ping {} -c 1 -W 2".format(self.hostname), shell=True)
		p.wait()
		return p.poll() == 0

	def update_status(self, cape_api: CapeApi, fog_api: FogApi) -> bool:
		""" READY - Check if the ip can ping and there is no task available for it
			RUNNING - there is a task for it 
			TUNING - set by tuner 
			TUNED - set by tuner
			STOPPED - not sure hmm
			ERROR - Just error

		Args:
			fog_api (FogApi): Description
		"""

		# The order matters! 	

		# if not self.pingable():
		# 	self.status = self.OFF

		if not fog_api.is_accessible():
			self.status = self.OFF
			# print("Updating of machine status failed as FOG is down")
			return False

		if self.status == self.TUNING: # Skip it if it is tuning as tunning will be in ready state
			return True

		cape_details = cape_api.view_machine(self.label)
		
		if not cape_details:
			print("cape_details is none")
			return False

		if cape_details['error'] or not cape_details['data']:
			self.status = self.ERROR		
			return True

		if fog_api.machine_has_task() and cape_details['data']['locked']:
			self.status = self.RUNNING
			return True
		elif not fog_api.machine_has_task() and not cape_details['data']['locked']:
			self.status = self.READY
			return True

		# if self.pingable:
			

		self.status = self.STOPPED # since cant ping and no task should be off
		return True






