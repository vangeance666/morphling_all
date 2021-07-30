from datatypes.submission import *
from datatypes.task import *
from restapis.capeapi import *

from utils.plugins import import_package

import signatures
from signatures.app_presence_reg import *
from signatures.app_presence_file import *
from signatures.failed_reg_keys import *

from tuning.chocopackagetuner import *
from tuning.regtuner import *


class Evaluator:
	
	SIG_TO_TUNNER_MAPPING = [
		{ 
			"signature_class": "AppPresenceReg"
			, "tuner_class":"ChocoPackageTuner"
		}
		, { "signature_class": "AppPresenceFile"
			, "tuner_class":"ChocoPackageTuner"
		}
		, { "signature_class": "FailedRegKeys"
			, "tuner_class":"RegTuner"
		}
	]

	def _packages_to_install(self, report_data) -> set:
		packages = set()

		for sig in report_data['signatures']:
			if sig['name'] in self.PKG_SIG_NAMES:
				for sig_data in sig['data']:
					packages.update(sig_data.items())

		return packages

	def _reg_keys_to_add(self) -> set:
		ret = set()
		# TODO check against behavior and see if the key status is false. 		
		return ret

	def apply_local_signatures(self, cape_api: CapeApi, task: Task) -> bool:
		""" Parses task report and flags applies local signatures
			based on CAPE analysis report details.
		
		Args:
		    cape_api (CapeApi): CAPE rest api utility object
		    task (Task): Task Object
		
		Returns:
		    bool: True if no error else False
		"""
		if not cape_api or not task:
			return False

		report_data = cape_api.get_report(task.id)
		# print("report_data", report_data)

		if not report_data:
			print("[Evaluator] report data not found")
			return False
		
		for mapping in self.SIG_TO_TUNNER_MAPPING:

			sig_obj = globals()[mapping['signature_class']](report_data)
			print("sig_obj: ", sig_obj)

			if sig_obj.run(): #if the signature returns true, then pass the signature data to the tuner
				task.signatures.append(sig_obj)
				print("task.signatures: ", task.signatures)

		return True

	def evalaute_next_task(self, task: Task) -> Task:
		""" Evaluates current task to check and 
			generate next task with tunning configurations
			to be applied before submission of sample.

		Args:
		    task (Task): Description
		
		Returns:
		    Task: Description
		"""
		#
		if not task or not task.do_retune:
			return None

		tuners = []

		for sig in task.signatures:

			sig_class_name = sig.__class__.__name__
			print("sig_class_name", sig_class_name)

			for mapping in self.SIG_TO_TUNNER_MAPPING:
				print("mapping['signature_class']", mapping['signature_class'])
				if sig_class_name == mapping['signature_class']:
					
					# The tuner should interpret the signature object data and tune acoordingly
					tuner_obj = globals()[mapping['tuner_class']](sig.data)
					print("tuner_obj", tuner_obj)
					print("tuner_obj", type(tuner_obj))
					tuners.append(tuner_obj)

		print("tuners: ", tuners)

		if not tuners:
			
			return None

		new_task = Task(task.file_path, task.machine_name)
		# TODO make sure the append tuners after 


		new_task.tuners_to_apply = tuners
		return new_task

	def evaluate_next_task_old(self, cape_api: CapeApi, task: Task) -> Task:
		# Evaluate the task report details and resubmit again.
		if not task or not task.do_retune:
			return None
		print("task.id", task.id)
		
		res =  cape_api.view_task(task.id)
		
		print("res", res)

		if res['error']:
			return None

		if not res['data']:
			return None

		task.parse_cape_task_data(res['data'])

		# Parse reported details and evalute packages to choco install + reg keys to add

		if not task.is_reported():
			return None

		report_details = cape_api.get_report(task.id)

		if "signatures" not in report_details:
			return None

		pkgs_to_install: set = self._packages_to_install(report_details)
		keys_to_add: set = self._reg_keys_to_add()

		if not pkgs_to_install and not keys_to_add:
			return None

		new_task = Task(task.file_path, task.machine_name)

		# If got packages to add then create a new task with current details but with the packges to tune
		if pkgs_to_install:
			new_task.to_install = task.to_install + list(pkgs_to_install)
		
		if keys_to_add:
			new_task._reg_keys_to_add = task._reg_keys_to_add + list(keys_to_add)

		return new_task
		