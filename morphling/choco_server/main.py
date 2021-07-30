import subprocess
import time
import argparse
import sys
import os

from utilities.internalizer import *
from sig_generator.signaturegenerator import *
from updating.nupkgupdater import *

from consts import *
from config import *


def cache_one_package(package_name, package_version=None) -> bool: 
	internalizer = Internalizer(
		choco_push_source=CHOCO_PUSH_SOURCE
		, repo_dep_folder=REPO_DEPENDENCIES_PATH
		, repoint_dep_folder=DEPENDENCIES_REPOINT_PATH)

	internalizer.internalize(
		save_folder=DOWNLOAD_DUMP_FOLDER
		, package_name=package_name
		, version=package_version)

def periodic_update(sleep_min_interval=1) -> bool:
	try:
		package_updater = NupkgUpdater(CHOCO_PUSH_SOURCE, REPO_DEPENDENCIES_PATH, DEPENDENCIES_REPOINT_PATH)
		sig_generator = SignatureGenerator(sig_file=HOSTED_SIG_FILE, repo_source=CHOCO_PUSH_SOURCE)
		while True:
			if package_updater.sync_community_packages():
				print("Manged to sync community packages")
				print("package_updater._community_packages:", package_updater._community_packages)
				# If manage to retrieve community packages details
				package_updater.update_repo_packages(DOWNLOAD_DUMP_FOLDER)
				print("---update sig file---")
				sig_generator.update_sig_files()
				print("---finish update sig file---")
			time.sleep(5)

	except KeyboardInterrupt:
		sys.exit()


def internalize_all_from_community():

	package_updater = NupkgUpdater(
		CHOCO_PUSH_SOURCE
		, REPO_DEPENDENCIES_PATH
		, DEPENDENCIES_REPOINT_PATH)

	print("---Retrieving packages from community repo: \"chocolatey\"---")
	# package_updater.sync_community_packages()
	package_updater.update_repo_packages(DOWNLOAD_DUMP_FOLDER)
	print("Done")

def sig_generate():
	print("---Capture differences into signature procedure---")
	sig_gen = SignatureGenerator(repo_source=CHOCO_PUSH_SOURCE)
	sig_gen.update_sig_files()
	print("Done")


class ArgParser(argparse.ArgumentParser):

	def __init__(self):
		self.stealth = None
		self.ap = argparse.ArgumentParser(description="Choco Server modules")
		self.ap.add_argument("-c", dest="internalize", action='store_true', help="Cache one chocolatey package mode")
		self.ap.add_argument("-ia", dest="internalize_all", action='store_true', help="Internalize all community packages mode")	
		self.ap.add_argument("-GS", dest="generate_sigs", action='store_true', help="Generate signatures for all packages at local choco repo")
		self.ap.add_argument("-F", dest="full_process", action='store_true', help="Internalizes all available community packges and generate signatures at intervals")

		self.ap.add_argument("--name", dest="package_name", action='store', help="Specify package name when using -i internalize mode.")
		self.ap.add_argument("--version", dest="package_version", action='store', help="Specify package version when using -i internalize mode.")

	def error(self, message):
		sys.stderr.write('error: %s\n' % message)
		self.ap.print_help()
		sys.exit(2)

	def parse_args(self):

		res = self.ap.parse_args()

		if res.internalize and not (res.internalize_all and res.generate_sigs and res.full_process):

			if not res.package_name:
				print("Please specifiy chocolatey package name to internalize\n")
				return False
				
			if not cache_one_package(res.package_name, res.package_version):
				print("Failed to internalize package: {} version: {}".format(res.package_name, res.package_version or None))

		elif res.internalize_all and not (res.internalize and res.generate_sigs and res.full_process):
			internalize_all_from_community()
		elif res.generate_sigs and not(res.internalize and res.internalize_all and res.full_process):
			sig_generate()
		elif res.full_process and not (res.internalize and res.internalize_all and res.generate_sigs):
			periodic_update()
		else:
			self.error("Please input something")
			return False


if __name__ == '__main__':
	
	parse_obj = ArgParser()
	parse_obj.parse_args()

