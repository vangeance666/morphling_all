import os
import json
import time
import subprocess
import hashlib


from .chocoinfo import *

from sig_converter.filepathconverter import *
from sig_converter.regpathconverter import *

from sys_captures.filescapture import *
from sys_captures.regcapture import *

from updating.nupkgupdater import *

from utilities.internalizer import *
from utilities.hasher import *

from config import *

# This file is will be the file where CAPE sandbox grabs through http
# ensure that the folder path is being hosted


# Use choco source list and check which one is the repo you want to install packages from
# REPO_SOURCE = "http://192.168.180.135/chocolatey/"


class SignatureGenerator:   

	CSV_FIELDS_NAMES = [
		"choco_package_name"
		, "file_difference"
		, "reg_difference"
	]

	SIG_SAVE_PATHS = {
		'files': SIG_FILE_PATH
		, "registry": SIG_REG_PATH
		, "hash_256": SIG_SHA256_PATH
	}

	def __init__(self, repo_source=None, to_snap_reg_keys=None, to_snap_folders=None):

		print("---init---")
	
		self._repo_source = repo_source or REPO_SOURCE

		self._reg_capture = RegCapture(to_snap_reg_keys or REG_KEYS_TO_CHECK)
		self._files_capture = FilesCapture(to_snap_folders or FILE_FLDRS_TO_CHECK)

		self._reg_sig_convert = RegPathConverter()
		self._file_sig_convert = FilePathConverter()
		self._hasher = Hasher()

		print("---finish init---")

	def get_installable_packages(self):
		print("inside get _installable packages")
		return ChocoInfo.get_repo_packages(self._repo_source)

	def _write_to_csv(self, rows: list):
		with open(self._csv_path, 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=self.CSV_FIELDS_NAMES)

			writer.writeheader()

			for row_values in rows:
				writer.writerow(dict(zip(self.CSV_FIELDS_NAMES, row_values)))

	def _install_package(self, package_name, version):
		cmd = "choco install {} --version={} --source={} -my".format(package_name, version, self._repo_source)
		print("cmd", cmd)
		subprocess.call(cmd)

	def _uninstall_package(self, package_name, version):
		cmd = "choco uninstall {} --version={} --source={} -y".format(package_name, version, self._repo_source)
		print("cmd", cmd)
		subprocess.call(cmd)

	def _hash_list_from_file_diff(self, file_sigs) -> list:
		ret = []
		for file_path in file_sigs:
			if os.path.isfile(file_path):
				ret.append(self._hasher.hash_256_file(file_path))

		return ret
		
		

	def gen_signatures(self) -> dict:
		
		ret = {
			"files": []
			, "registry": []
			, "hash_256": []
		}

		installables = DEMO_PACKAGES_INFO


		print("installables", installables)

		for item in installables:

			name, version = item['name'], item['version']

			print("=== First Snap ===")
			self._files_capture.first_snap()
			self._reg_capture.first_snap()
			print("=== Finished first Snap ===")

			print("Installing {} version: {}".format(name, version))
			self._install_package(name, version)
			print("Finished installing {} version: {}".format(name, version))
			# if not self._install_package(name, version):
			# 	print("cant install {} {}".format(name, version))
			# 	continue

			time.sleep(1) #Buffer time for changes to apply

			print("=== Second Snap ===")
			self._files_capture.second_snap()
			self._reg_capture.second_snap()
			print("=== Finished second Snap ===")
		
			if self._files_capture.evaluate_difference() and self._reg_capture.evaluate_difference():

				#.difference will be a dict. The values are a list 
				files_added_sig =  [k for x, y in self._files_capture.difference.items() for k in y]
				reg_added_sig =  [k for x, y in self._reg_capture.difference.items() for k in y]
				
				print("files_added_sig", files_added_sig)
				print("reg_added_sig", reg_added_sig)

				if files_added_sig:
					ret['files'].append({"package_name": name, "version": version, "signatures":[self._file_sig_convert.apply(x) for x in files_added_sig]})
					ret['hash_256'].append({"package_name": name, "version": version, "signatures":self._hash_list_from_file_diff(files_added_sig)})

				if reg_added_sig:
					ret['registry'].append({"package_name": name, "version": version, "signatures":[self._reg_sig_convert.apply(x) for x in reg_added_sig]})

			else:
				print("Failed to evaluate_differences for both reg and file")
			
			print("Uninstalling {} version: {}".format(name, version))			
			self._uninstall_package(name, version)
			print("Finished uninstalling {} version: {}".format(name, version))

			# if not self._uninstall_package(name, version):
			# 	print("cant uninstall {} {}".format(name, version))
			# 	continue

		return ret
	
	def load_file_json(self, json_file):
		try:
			if not os.path.isfile(json_file):
				print("Return normal list if sigfile is not created")
				return [] #Return normal list if sigfile is not created

			with open(json_file, "r", encoding="UTF-8") as f:
				return json.load(f)

		except Exception as e:
			return None

	def _update_json_data(self, json_file, data) -> bool:
		try:
			with open(json_file, 'w') as f:
				json.dump(data, f)
		except Exception as e:
			return False
		return True

	def _update_file(self, file_path, data: list) -> bool:
		to_update = data
		# print("to_update", to_update)

		if os.path.isfile(file_path):
			loaded_data = self.load_file_json(file_path)

			# to_update_packages_info = [ for x in to_update]
			# for data in loaded_data:
			# 	if 
			# print("loaded_data", loaded_data)

			for x in loaded_data:
				if x not in to_update:
					to_update.append(x)

			# to_update = (to_update + list(set(loaded_data) - set(to_update))) #Append and make unique

		return self._update_json_data(file_path, to_update)

	def _update_signature_files(self, sigs) -> bool:

		for sig_type in self.SIG_SAVE_PATHS:
			if sigs[sig_type]: # if there is sig generated then update the file accordingly
				self._update_file(self.SIG_SAVE_PATHS[sig_type], sigs[sig_type])
				
				print("self.SIG_SAVE_PATHS[sig_type]", self.SIG_SAVE_PATHS[sig_type])
				print("sigs[sig_type]", sigs[sig_type])

		return True
		
	def update_sig_files(self) -> bool:
		sigs = self.gen_signatures()
		print("sigs", sigs)
		return self._update_signature_files(sigs)

	
		





