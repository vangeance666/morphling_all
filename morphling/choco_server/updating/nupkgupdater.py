import sys
import time
from utilities.internalizer import *

from config import *

class NupkgUpdater:

	def __init__(self, repo_package_folder, repo_dep_folder, repoint_dep_folder):
		print("--- NupkgUpdater---")
		print("repo_package_folder", repo_package_folder)		
		print("repoint_dep_folder", repoint_dep_folder)
		print("repo_dep_folder", repo_dep_folder)
		print("--- NupkgUpdater---\n\n")

		self._cooldown: int = 60 * SYNC_MINS_COOLDOWN
		self._community_packages: list = None
		self._last_retrieved = None
		self._internalizer = Internalizer(repo_package_folder, repo_dep_folder, repoint_dep_folder)

	def sync_community_packages(self) -> bool:
		print("--- Getting Packages info from community repo ---")

		if self._last_retrieved and ((time.time() - self._last_retrieved) < self._cooldown):
			print("Not time yet to sync packages info!")
			return False

		print("--- Getting Packages info from community repo ---")
		self._community_packages = ChocoInfo.get_community_packages()
		self._last_retrieved = time.time()
		print("--- Finished retriving community packages ---")
		return True

	def get_required_packages(self) -> list:
		""" Identifies which pacakges within community repo is not
			installed in the local choco repo           

		Returns:
			list: List of packages names and version that is required
				  to be installed to match community repo
		"""
		ret = []
		local_packages = ChocoInfo.get_local_packages(
			PUSHED_PACKAGES_PATH)

		print("local_packages", local_packages)

		return [c_package for c_package in self._community_packages if c_package not in local_packages]

	def update_repo_packages(self, download_folder) -> bool:

		print("Getting required packages")		
		# required_packages = self.get_required_packages()
		required_packages = DEMO_PACKAGES_INFO


		# print("need to download {}".format(len(required_packages)))
		# print("required_packages", required_packages)


		# required_packages = [{'name': 'glmixer', 'version': '1.5.1329'}, {'name': 'keytweak', 'version': '2.3.0.20200614'}]
		# required_packages = DEMO_PACKAGES_INFO

		# , {'name': 'powershell', 'version': '6.2.2'}
		# Consider stickynote, 7zip, cpuid, cputemp, VLC, adobe pdf, adobe flash player, opera, paint.net, filezilla, notepad++

		print("required_packages", required_packages)

		if not required_packages:
			print("No packages required to be updated")
			return True

		for package in required_packages:
			if self._internalizer.internalize(download_folder, package['name'], package['version']):
				print("Successfully internalize ",
					  package['name'], package['version'])
			else:
				print("Failed to internalize ",
					  package['name'], package['version'])

		self._internalizer.migrate_packages(dependencies_folder=os.path.join(download_folder, "downloads"))
		self._internalizer.push_all_nupkg(nupkgs_folder=download_folder)

		return True

