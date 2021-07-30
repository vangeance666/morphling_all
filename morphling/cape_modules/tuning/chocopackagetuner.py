from .tuner import *
from configs.config import *


class ChocoPackageTuner(Tuner):
	name = "choco_package_tuner"
	description = "Tuner to install chocolatey packages remotely"

	def __init__(self, packages_to_add):
		self.data: list = packages_to_add
		self._repo_source = LOCAL_REPO_SRC

	def tune(self, username, password, hostname):
		print("choco_package_tuner tunner tuning")
		try:
			for package in self.data:
				pkg_dict = eval(package['package_found'])
				command = "choco install {} --version={} --source={} -my".format(
					pkg_dict['package_name'], pkg_dict['version'], self._repo_source)

				print("command", command)
				self.send_pws_command(username, password, hostname, command)
		except:
			print("Choco tuner failed to tune")
			return False
		return True


	def get_info(self):

		data = []
		for pkg in self.data:
			pkg_dict = eval(pkg['package_found'])
			print("pkg_dict", pkg_dict)
			data.append({"Installed": str(pkg_dict)})

		return {
			"name": self.name
			, "description": self.description
			, "data": data
		}





