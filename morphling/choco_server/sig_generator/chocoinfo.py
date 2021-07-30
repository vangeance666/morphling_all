import subprocess
import re
import os

class ChocoInfo:
	
	REG_PACKAGE_PATTERN = r'([\w.\-]+) (\d[\d.]*)'

	@staticmethod
	def get_repo_packages(source: str, approved_only=False, ignore_broken=True):
		packages = []
		cmd = "choco list --source={}".format(source)
		print("cmd", cmd)
		output = subprocess.check_output(cmd, universal_newlines=True)

		package_re = re.compile(ChocoInfo.REG_PACKAGE_PATTERN)		

		for line in output.splitlines():

			if approved_only and ('[Approved]' not in line):
				continue

			if ignore_broken and ('broken' in line):
				continue

			match = package_re.match(line)
			
			if match and match.group(1).lower() != 'chocolatey':
				print("appended smth---")
				packages.append({'name': match.group(1), 'version': match.group(2)})

		return packages

	@staticmethod
	def get_community_packages(approved_only=False, ignore_broken=True) -> list:
		""" Retrieves all avaiable packages from chocolatey community repo.
		
		Args:
		    approved_only (bool, optional): Toggle to only retrived approved only packages
		    ignore_broken (bool, optional): Toggle to exclude broken packages
		
		Returns:
		    list: List of packages along with their version nummber
		"""

		return ChocoInfo.get_repo_packages("chocolatey", approved_only, ignore_broken)
		

	@staticmethod
	def get_local_packages(package_root_dir: str) -> list:
		""" Parses locally pushed packages storing their package
			name and version number.
		
		Args:
		    package_root_dir (str): Folder path of choco local repo
		    						pushed packages

		Returns:
		    list: List of packages along with their version nummber
		"""

		res = []

		for f in os.listdir(package_root_dir):
			package_dir = os.path.join(package_root_dir, f)
			if os.path.isdir(package_dir):
				for fd in os.listdir(package_dir):
					res.append({'name':f, 'version':fd})
		return res

