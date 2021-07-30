import subprocess

class Tuner:

	name = ""
	description = ""

	def __init__(self):
		self.data = []

	def send_pws_command(self, username, password, hostname, command: str) -> bool:
		
		cmd = "winexe -U {}%{} //{} \"{}\"".format(username
			, password
			, hostname
			, command)
		print("cmd", cmd)
		
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

		return p.communicate()

	def tune(self, username, password, hostname):
		raise NotImplementedError

	def get_info(self):
		return {
			"name": self.name
			, "description": self.description
			, "data": self.data
		}