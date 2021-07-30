import datetime
import time
import os
import sys
import traceback
import shutil

import xml.etree.ElementTree as ET

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

import requests
import tempfile
import zipfile

import random
import socket
import ipaddress

import struct

from enum import Enum

import subprocess
import re

from urllib.parse import urlparse

from sig_generator.chocoinfo import *

from config import *

class AgentRandomizer:

	"""Generates random user agents strings

	Attributes:
		MAX_LIMIT (int): Max number of randomized useragents
		OPERATING_SYSTEMS (list): Randomize based on specified OS for e.g Windows, Linux, MAC
		SOFTWARE_NAMES (list): Randomize based on specified software names for e.g Firefox, Chrome

	"""

	# Read https://pypi.org/project/random-user-agent/ for more info

	MAX_LIMIT = 100
	SOFTWARE_NAMES = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
	OPERATING_SYSTEMS = [OperatingSystem.WINDOWS.value,
						 OperatingSystem.LINUX.value]

	def __init__(self):
		self._rotator = UserAgent(software_names=self.SOFTWARE_NAMES,
								  operating_systems=self.OPERATING_SYSTEMS, limit=self.MAX_LIMIT)

	def get_random_agent(self) -> str:
		return self._rotator.get_random_user_agent()


class Downloader:

	def __init__(self, spoof_agent=False, bypass_limit_rate=False):

		# self._bypass_rate_limit = bypass_limit_rate
		self._spoof_agent = spoof_agent

		# self._limit_bypasser = RateLimitBypass() if bypass_limit_rate else None
		self._agent_randomizer = AgentRandomizer() if spoof_agent else None

	def _generate_headers(self):

		ret_headers = {}

		# if self._bypass_rate_limit:
		#   ret_headers = {**ret_headers, **self._limit_bypasser.gen_headers()}

		if self._spoof_agent:
			ret_headers = {**ret_headers, **{'User-Agent': self._agent_randomizer.get_random_agent()}}

		return ret_headers

	def download_url(self, url, save_folder, save_name) -> str:

		print("---download-url")

		print("save_folder :", save_folder)
		print("save_name :", save_name)

		try:
			r = requests.get(url, allow_redirects=True,
							 headers=self._generate_headers())
			save_path = save_folder+"\\"+save_name
			print("save_path :", save_path)

			open(save_path, 'wb').write(r.content)
			return save_name
			# return file_name
		except Exception as e:
			raise e
			return ""


class PackageInfo(dict):

	def __init__(self):
		self.name = None
		self.version = None
		self.dependencies: list = []

	def __getattr__(self, attr):
		return self[attr]

	def __str__(self):
		return str(self.__dict__)


class FilesUtility:

	@staticmethod
	def delete_folder(folder_path) -> bool:
		try:
			shutil.rmtree(folder_path)
		except OSError as e:
			print("Delete_folder OS error: {0}".format(err))
			return False
		return True

	@staticmethod
	def delete_file(file_path) -> bool:
		try:
			os.remove(file_path)
		except OSError:
			print("Delete_file OS error: {0}".format(err))
			return False
		return True


class Internalizer:

	CHOCO_PACKAGE_API_URL = "https://chocolatey.org/api/v2/package/"

	DEL_FOLDERS = ['_rels', 'package']
	DEL_FILES = ['[Content_Types].xml']

	DEF_NUPKG_FILE = "default.nupkg"

	REG_URL_PATTERN = r'[\'\"]http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[\'\"]'

	def __init__(self, choco_push_source, repo_dep_folder, repoint_dep_folder, spoof_agent=True):
		self._downloader = Downloader(spoof_agent)

		self._choco_push_source = choco_push_source
		self._repo_dep_folder = repo_dep_folder
		self._repoint_dep_folder= repoint_dep_folder

	def download_nupkg_package(self, package_name, save_folder, version=None, save_file="temp.nupkg") -> str:

		api_url = '/'.join(s.strip('/')
						   for s in [self.CHOCO_PACKAGE_API_URL, package_name, version or ''])

		dl_url = self._downloader.download_url(api_url, save_folder, save_file)

		if save_file == dl_url:
			return os.path.join(save_folder, save_file)

		return ""

	def _unzip_nupkg(self, nupkg_path, extract_path) -> bool:
		try:
			with zipfile.ZipFile(nupkg_path, 'r') as f:
				f.extractall(extract_path)
		except (IOError, zipfile.BadZipfile) as e:
			print(e)
			return False
		return True

	def _preprocess_extracted_nupkg(self, nupkg_folder) -> bool:
		return all([FilesUtility.delete_file(os.path.join(nupkg_folder, S1)) for S1 in self.DEL_FILES]
				   + [FilesUtility.delete_folder(os.path.join(nupkg_folder, S2)) for S2 in self.DEL_FOLDERS])

	def _process_extracted_nupkg(self, nupkg_folder, save_folder) -> bool:

		tools_folder = os.path.join(nupkg_folder, 'tools')
		downloads_folder = os.path.join(save_folder, 'downloads')

		if not os.path.exists(downloads_folder):
			try:
				os.mkdir(downloads_folder)
			except OSError as e:
				return False

		if not os.path.exists(tools_folder):
			print('WARN: Directory "tools/" is not exists in package.')
			return True

		# Stoped here

		tools_ps_files = [f for f in os.listdir(
			tools_folder) if f.lower().endswith('.ps1')]

		for fn in tools_ps_files:

			process_file_path = os.path.join(tools_folder, fn)
			output_file_path = os.path.join(tools_folder, 'tmp.ps1')

			with open(process_file_path, 'r', encoding="UTF-8", errors='ignore') as process_file, open(output_file_path, 'w', encoding="UTF-8") as out_file:
				for line in process_file.readlines():
					if 'https://' in line or 'http://' in line:

						res = re.search(self.REG_URL_PATTERN, line)
						if res:

							url = urlparse(res[0].strip("'").strip('"'))
							file_name = os.path.basename(url.path)
							print("file_name before if not:", file_name)

							# Download the particular URL and
							if not os.path.exists(os.path.join(downloads_folder, file_name)):
								try:
									file_name = os.path.basename(self._downloader.download_url(
										url.geturl(), save_folder=downloads_folder, save_name=file_name))
									print("file_name :", file_name)
								except Exception as e:
									print(e)
									return False

							out_file.write(line.replace(
								res[0], "'"+os.path.join(self._repoint_dep_folder, file_name).replace("\\", "/")+"'"   ))
					else:
						out_file.write(line)

			shutil.move(os.path.join(tools_folder, 'tmp.ps1'),
						os.path.join(tools_folder, fn))

		return True

	def _parse_nuspec(self, nupkg_folder) -> PackageInfo:

		try:
			pkg_name, pkg_version, pkg_dependencies = None, None, []

			package_info = PackageInfo()

			for f in os.listdir(nupkg_folder):
				if f.endswith('.nuspec'):
					xml_name = os.path.join(nupkg_folder, f)

					tree = ET.parse(xml_name)
					root = tree.getroot()

					namespace = root.tag.split('}').pop(0).strip('{')

					package_info.name = list(root)[0].find(
						'{%s}id' % namespace).text
					package_info.version = list(root)[0].find(
						'{%s}version' % namespace).text
					package_info.dependencies = [i.attrib for i in list(
						list(root)[0].find('{%s}dependencies' % namespace) or [])]

					break

			return package_info
		except Exception as e:
			return None

	def move_dependencies(self, folder):
		if os.path.exists(folder):
			for item in os.listdir(folder):
				if os.path.isfile(src):
					shutil.copyfile(os.path.join(folder, item),
									os.path.join(REPO_DEPENDENCIES_PATH, item))


	def choco_pack(self, package_folder, save_path):
		package_details = self._parse_nuspec(package_folder)

		cmd = "choco pack {}.nuspec --out {}".format(
			os.path.join(package_folder, package_details.name), save_path)

		subprocess.call(cmd)

	def _convert_to_zip(self, download_path) -> str:
		new_path = os.path.splitext(download_path)[0] + '.zip'

		print("new_path :", new_path)
		print("download_path :", download_path)

		os.rename(download_path, new_path)

		return new_path

	def internalize(self, save_folder, package_name, version=None) -> bool:
		print("---Internalize---")
		print("save_folder", save_folder)
		print("package_name", package_name)

		package_folder = str(tempfile.TemporaryDirectory()).strip(
			"<TemporaryDirectory '").strip("'>").replace("\\\\", "\\")

		# downloaded_path = self.download_nupkg_package(package_name=package_name, save_folder=download_folder, version=version)
		downloaded_path = self.download_nupkg_package(
			package_name=package_name, save_folder=save_folder, version=version)

		if downloaded_path == "":
			return False

		if not self._unzip_nupkg(downloaded_path, package_folder):
			return False

		package_info = self._parse_nuspec(package_folder)

		if package_info is None:
			print("package_info is None")
			return False

		if '.extension' in package_info.name:
			ext_package = os.path.join(save_folder, '{}.{}.nupkg'.format(
				package_info.name, package_info.version))

			shutil.copyfile(downloaded_path, os.path.join(
				save_folder, '{}.{}.nupkg'.format(package_info.name, package_info.version)))

		else:
			if not self._preprocess_extracted_nupkg(package_folder):
				return False
			if not self._process_extracted_nupkg(package_folder, save_folder):
				return False

			print("---Executing choco pack---")
			self.choco_pack(package_folder, save_folder)

		for pkg in package_info.dependencies:

			try:  # to handle the
				return self.internalize(
					save_folder=save_folder
					, package_name=pkg['id']
					, version=(None if 'version' not in pkg else pkg['version'].strip('[').strip(']')))
			except:
				return False

		os.remove(os.path.join(save_folder, "temp.nupkg"))

		return True


	def migrate_packages(self, dependencies_folder: str):
		for f in os.listdir(dependencies_folder):
			shutil.copy(os.path.join(dependencies_folder, f), os.path.join(self._repo_dep_folder, f))
			os.remove(os.path.join(dependencies_folder, f))

	def push_nupkg(self, nupkg_path, repo_source) -> bool:
		cmd = "choco push {} --source={} -k=\"chocolateyrocks\" --force".format(
			nupkg_path, repo_source)
		res = subprocess.run(cmd)

		return res.stderr != 0

	def push_all_nupkg(self, nupkgs_folder: str) -> bool:
		for f in os.listdir(nupkgs_folder):
			if f.endswith('.nupkg'):		

				src_nupkg_path = os.path.join(nupkgs_folder, f)

				if self.push_nupkg(src_nupkg_path, self._choco_push_source):
					print("successfully pushed {}".format(src_nupkg_path))
					os.remove(src_nupkg_path)
				else:
					print("Failed to push {}".format(src_nupkg_path))

