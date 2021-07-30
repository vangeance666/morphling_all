import json
import os
import re

from configs.config import *
from .signature import Signature

class FailedRegKeys(Signature):
	
	name = "failed_reg_keys"
	description = "Failed queried registry keys to be tuned for next round of analysis"
	severity = -1
	categories = ["context"]
	authors = ["boomer_kang"]
	minimum = "1.2"

	def run(self):

		REG_KEY_START = [
			"HKEY_CLASSES_ROOT"     
			, "HKEY_CURRENT_USER"     
			, "HKEY_LOCAL_MACHINE"    
			, "HKEY_USERS"            
			, "HKEY_CURRENT_CONFIG"   
		]

		found_failed_keys = set()

		try:
			calls = [call for process in self.results['behavior']['processes'] for call in process['calls']]

			for call in calls:
				if 'status' not in call:
					continue

				if not call['status']: #only look at those status is failed. 

					if not 'arguments' in call:
						continue

					for arg in call['arguments']:
						if ('value' in arg) and any(arg['value'].upper().startswith(x) for x in REG_KEY_START):
							found_failed_keys.add(arg['value'])
		except:
			return False

		if found_failed_keys:
			for K in found_failed_keys:
				self.data.append({"Failed_keys": K})

			return True

		return False



		