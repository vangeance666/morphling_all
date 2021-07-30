from .tuner import *
from configs.config import *


class RegTuner(Tuner):

	name = "reg_tuner"
	description = "To create registry keys in the analysis VM"

	def __init__(self, keys_to_add=None):
		self.data = keys_to_add

	def add_key(self, username, password, hostname, reg_key_name) -> bool:
		command = "REG ADD \\\"{} \\\" /f /ve".format(reg_key_name)
		print("command", command)
		out, err = self.send_pws_command(username, password, hostname, command)
		return not err.decode('utf-8')

	def tune(self, username, password, hostname):
		print("Reg tunner tuning")
		# try:
		for key in self.data:
			print("self.data", self.data)
			print("reg tuner key:", key)
			self.add_key(username, password, hostname, key['Failed_keys'])

		# except:
		# 	print("Failed to send pws command")
		# 	return False
		# return True

		# return all([self.add_key(username, password, hostname, key) for key in self.data])		
	def get_info(self):

		data = []

		for reg_key in self.data:
			print("reg_key", reg_key)			
			data.append({"Added": str(reg_key)})

		return {
			"name": self.name
			, "description": self.description
			, "data": data
		}

