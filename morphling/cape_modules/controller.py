import configparser
import signal
import os
import subprocess
import requests
import json
import pickle
import hashlib
import time

from configs.config import *

from restapis.fogapi import *
from restapis.capeapi import *
from utils.signatureupdater import *

from datatypes.machine import *
from datatypes.submission import *

from utils.evaluator import *
from utils.exporter import *
from utils.hasher import *

from tuning.tuner import *
from tuning.chocopackagetuner import *


from signatures.signature import *
from signatures.app_presence_file import *
from signatures.app_presence_reg import *
from signatures.failed_reg_keys import *

import threading

class Controller:

	TIMER_CHOCO_SIG = 60

	TIMER_MACHINE_STATUS = 3
	TIMER_STATUS_UPDATE = 2
	TIMER_SUBMIT = 1
	TIMER_RESUBMIT_TASK = 1
	TIMER_SAVE_SUBMISSIONS = 2


	def __init__(self , webdriver=None): #webdriver will be selenium obj


		self._submissions: list = []

		if os.path.isfile(DB_SUBMISSIONS_PATH):
			loaded_submissions = Exporter.load(DB_SUBMISSIONS_PATH)
			if loaded_submissions: 
				self._submissions = loaded_submissions
				print("self._submissions", self._submissions)
		

		# for s in self._submissions:
		# 	for task in s.tasks:
		# 		if task.id = 
		# print("init self._submissions", self._submissions)
		# print("self._submissions", self._submissions)
		self._machines:list = self._parse_physical_machines()

		self._signature_updater = SignatureUpdater()
		self._evaluator = Evaluator()
		self._hasher = Hasher()

		self._cape_api = CapeApi()
		self._fog_api = FogApi()

		self._web_driver = webdriver
		
		self._stop = False

	def force_resubmit_task(self, task_id):
		try:
			task = self._get_task_by_id(task_id)
			if not task:
				self._notify_failure("Task does not exist")
				return False
			task.force_resubmit = True
		except:
			self._notify_failure("Error, cant force resubmit task {} .".format(task_id))
			return False
		self._notify_success("Successfully forced resubmission for task {}.".format(task_id))
		return True

	#GUI
	def stop_task_resubmit(self, task_id):
		try:
			task = self._get_task_by_id(task_id)
			if not task:
				self._notify_failure("Task does not exist")
				return False
			task.do_resubmit = False
		except:
			self._notify_failure("Error disabling resubmission for task {} .".format(task_id))
			return False
		self._notify_success("Successfully disable resubmission for task {}.".format(task_id))
		return True

	#GUI
	def enable_task_resubmit(self, task_id):
		try:
			task = self._get_task_by_id(task_id)
			if not task:
				self._notify_failure("Task does not exist")
				return False
			task.do_resubmit = True
		except:
			self._notify_failure("Error enabling resubmission for task {}.".format(task_id))
			return False
		self._notify_success("Successfully enabled resubmission for task {}.".format(task_id))
		return True

	def set_web_driver(self, web_driver):
		self._web_driver = web_driver

	# Done
	def _enable_cuckoo(self):
		subprocess.Popen("python3 /opt/CAPEv2/cuckoo.py", shell=True)

	def _reset_cape_port(self, port=2042):
		try:
			res = subprocess.check_output("lsof -i :{}".format(port), shell=True)
		except Exception as e:
			return 

		for process in res.decode('UTF-8').split("\n")[1:]:
			data = [x for x in process.split(" ") if x != '']
			if data:
				os.kill(int(data[1]), signal.SIGKILL)

	def _notify_info(self, message):
		self._web_driver.execute_script("showInfo('{}');".format(message))
	def _notify_success(self, message):
		self._web_driver.execute_script("showInfo('{}');".format(message))
	def _notify_failure(self, message):
		self._web_driver.execute_script("showError('{}');".format(message))

	def _get_task_by_id(self, task_id) -> Task:
		for submission in self._submissions:
			for task in submission.tasks:
				if task.id == task_id:
					return task

		return None

	def disable_submission_evaluation(self, sha_256):
		for submission in self._submissions:
			if submission.hash == sha_256:
				for task in submission.tasks:
					task.do_retune = False
				break

	def _parse_physical_machines(self):
		""" Creates an Machine object of each physical machine specified
			physical.conf and adds it into the machines list
		"""

		print("inside parse physical machines")

		ret = []

		config = configparser.ConfigParser()
		if not config.read(CONF_MACHINES_PATH):
			raise Exception("Failed to read config file {}".format(CONF_MACHINES_PATH))

		machine_names = config['physical']['machines'].split(',')

		for name in machine_names:
			label = config[name]['label']
			username = config[name]['username']
			password = config[name]['password']
			ip = config[name]['ip'] 

			ret.append(Machine(label, username, password, ip))

		return ret

	def cape_accessible(self) -> bool:
		return self._cape_api.is_accessible()

	def fog_accessible(self) -> bool:
		return self._fog_api.is_accessible()
	# GUI 
	def add_task(self, sample_path, machine_name, choco_packages=None, keys_to_add=None) -> bool:
		"""
			1. Create new task object
			2. Add the task object to queue
			3. Check if the task should fit into any submissions.
			 Append into submissions 
				if already exist else create new and add inside
			4. 
		"""
		if not os.path.isfile(sample_path):
			print("File: {} does not exists".format(sample_path))
			return False

		machine_names = self.get_machines_name()
		if machine_name not in machine_names:
			print("Machine name does not exist")
			return False

		file_hash = self._hasher.hash_256_file(sample_path)

		task = Task(sample_path, machine_name, choco_packages, keys_to_add, "new")
		print("task.__dict__", task.__dict__)

		submission_exists: bool = False

		print("self._submissions", self._submissions)
		if file_hash in [S.hash for S in self._submissions]:
			print("Already got submission, will try add to submission")
			
			for submission in self._submissions:
				if submission.hash == file_hash:
					submission.add_task(task)
					submission_exists = True
					print("Added task to submission {}".format(submission.hash))
					break

		if not submission_exists:
			print("Dont have submission, gona add a new submission and add task")
			new_submission = Submission(file_hash)
			new_submission.add_task(task)
			self._submissions.append(new_submission)
			
		self._save_submissions_info()

		return True

	# GUI
	def get_submissions_info(self):
		# try:
		return [s.get_info() for s in self._submissions]
		# except:
		# 	return None

	# For GUI
	def get_machines_info(self):
		try:
			return [m.get_info() for m in self._machines]
		except:
			return None
	#For gui
	def get_machines_name(self):
		return [m.__dict__['label'] for m in self._machines]

	#for gui
	def get_task_info(self, task_id):
		for sub in self._submissions:
			for task in sub.tasks:
				print("task id: ", task.__dict__)
				if task and (int(task.id) == int(task_id)):
					return task.get_info()
		return None


	def _get_machine(self, machine_name):
		for machine in self._machines:
			if machine.label == machine_name:
				return machine
		return None

	#D 
	def sync_signature_thread(self):
		while True:
			if self._stop:
				break
			self._signature_updater.update_local_sig_file()
			print("Synced local signatures with choco server: {}".format(INNER_CHOCO_IP))
			time.sleep(self.TIMER_CHOCO_SIG) # Sync every min
	#D 
	def machine_status_thread(self):
		while True:
			if self._stop:
				print("Stoped machine status thread")
				break
			for machine in self._machines:
				machine.update_status(self._cape_api, self._fog_api)
				for submission in self._submissions:
					for task in submission.tasks:
						if task.status == task.STATUS_RUNNING and task.machine_name == machine.label:
							machine.allocated_task = task
							self._notify_info("Task {} has been allocated to machine {}".format(task.id, machine.label))
						else:
							machine.allocated_task = None

			time.sleep(self.TIMER_MACHINE_STATUS) # every one second then refresh all machines status

	def task_status_update_thread(self):
		while True:
			if self._stop:
				print("Stoped task status thread")
				break

			for submission in self._submissions:
				for task in submission.tasks:
					task.sync_status_with_cape(self._cape_api)
			time.sleep(self.TIMER_STATUS_UPDATE)
	# D
	def submit_thread(self):
		""" 1. Loop all task task and 
			This one every 5 sec check the queue and submit the task accordingly
		"""
		while True:
			if self._stop:
				print("Stoped submit thread")
				break
			for submission in self._submissions:
				for task in submission.tasks:
					if task.status == task.STATUS_NEW or (task.force_resubmit):
						machine: Machine = self._get_machine(task.machine_name)

						if not machine:
							continue

						if machine.status != machine.READY:
							continue

						print("+++Submit thread before do_retune")
						if task.do_retune:
							print("+++Submit thread inside do_retune")
							machine.status = machine.TUNING
							for tuner in task.tuners_to_apply:
								print("+++Doing tuning hehe")
								tuner.tune(machine.username, machine.password, machine.hostname)

							print("---Sleep 6 seconds after returning---")
							time.sleep(6)

						print("Before task.submit--")
						if task.submit(self._cape_api):
							machine.status = machine.RUNNING
							machine.task = task

							if task.force_resubmit:
								task.force_resubmit = False
							# print("---Submitted Task {}---".format(task.id))
							self._notify_success("Successfully submited {}.".format(task.file_path))
							self._save_submissions_info()

			# print("Submit thread sleeping 3 sec")
			time.sleep(self.TIMER_SUBMIT)
	#D 
	def resubmit_task_thread(self):
		""" Every 5 second check all submission ,
			for each submission check latest task if requires
			retuning + resubmission + update their status
		"""
		while True:
			if self._stop:
				break	

			for submission in self._submissions:
				for task in submission.tasks:


					if task.status == task.STATUS_EVALUATED:
						continue

					if (task.status == task.STATUS_REPORTED):

						print("====Found a reported task: {} .".format(task.id))

						if not self._evaluator.apply_local_signatures(self._cape_api, task):
							continue

						task.status = task.STATUS_EVALUATED #Once apply signatures, treat as evaluated
						print("Successfully evaluated task id: {} .".format(task.id))

						if task.do_resubmit and not task.resubmited:
							
							if task.resubmit_cap == 0:
								print("resubmit cap is 0 found")
								continue

							print("trying to evaluate next task")
							new_task = self._evaluator.evalaute_next_task(task)
							print("new_task", new_task.get_info())

							if not new_task:
								print("Evaluator has decided this case does not need to be resubmitted")
								continue

							if new_task: # Link the tasks 

								new_task.previous_task = task
								new_task.resubmit_cap = task.resubmit_cap - 1

								if submission.add_task(new_task):
									task.resubmited = True
									self._notify_info("Task {} has been evaluated and resubmited for a tuned analysis".format(task.id))
								else:
									task.resubmited = False
									self._notify_failure("Failed to resubmit new task for task: {} .".format(task.id))

						self._save_submissions_info();

			time.sleep(self.TIMER_RESUBMIT_TASK)

	def save_submissions_thread(self):
		while True:
			if self._stop:
				break
			self._save_submissions_info()
			time.sleep(self.TIMER_SAVE_SUBMISSIONS)

	def _save_submissions_info(self):
		return Exporter.save(DB_SUBMISSIONS_PATH, self._submissions)

	#ok
	def _cleanup(self) -> bool:
		self.stop_threads()
		return self._save_submissions_info()
	#ok
	def __del__(self):
		print("__del__")
		self._cleanup()
	#ok
	def __exit__(self):
		self._cleanup()

	def stop_threads(self):
		self._stop = True

	def start_threads(self):

		# t0 = threading.Thread(target=self._enable_cuckoo, daemon=True)
		threading.Thread(target=self.sync_signature_thread, daemon=True).start()

		threading.Thread(target=self.machine_status_thread, daemon=True).start() #ok
		threading.Thread(target=self.submit_thread, daemon=True).start() #ok
		threading.Thread(target=self.resubmit_task_thread, daemon=True).start()
		threading.Thread(target=self.task_status_update_thread, daemon=True).start() #ok
		threading.Thread(target=self.save_submissions_thread, daemon=True).start() #ok		


	def start(self):
		time.sleep(1)
		print("---Starting Threads---")		
		self.start_threads()

def main():

	import socket
	a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	location = ("", 2042)

	result_of_check = a_socket.connect_ex(location)


	if result_of_check == 0:

	   print("Port is open")

	else:

	   print("Port is not open")

	# C = Controller()
	# capi = CapeApi()
	# capi.view_machine("win7final")
	# print("capi.view_machine(\"win7final\")", capi.view_machine("win7final"))

if __name__ == '__main__':
	# main()
	K = [{"Failed_keys": "HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\VLC media player\\"}]
	t = RegTuner(K)
	t.tune("win7clonesp1", "toor", "192.168.180.131")
	# main()

