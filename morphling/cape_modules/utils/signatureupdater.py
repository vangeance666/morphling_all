import subprocess
import os
from configs.config import *

class SignatureUpdater:

	SIG_PATHS_MAPPING = [
		{"from": CHOCO_SIG_FILE_PATH, "to": LOCAL_SIG_FILE_PATH}
		, {"from": CHOCO_SIG_REG_PATH, "to": LOCAL_SIG_REG_PATH}
		, {"from": CHOCO_SIG_SHA256_PATH, "to": LOCAL_SIG_SHA256_PATH}
	]

	def _get_remote_file(self, username, hostname, remote_path, local_save_path):
		cmd = "scp -P {} {}@{}:{} {}".format(SIG_PORT, username, hostname, remote_path, local_save_path)
		print("cmd", cmd)
		subprocess.call(cmd, shell=True)

	def update_local_sig_file(self) -> bool:
		if not os.path.isdir(LOCAL_SIG_FOLDER):
			print("LOCAL_SIG_FOLDER", LOCAL_SIG_FOLDER)
			os.makedirs(LOCAL_SIG_FOLDER)

		for sig_path in self.SIG_PATHS_MAPPING:
			self._get_remote_file(
				username=SIG_GEN_USER_NAME
				, hostname=SIG_GEN_HOSTNAME
				, remote_path=sig_path['from']
				, local_save_path=sig_path['to'])

			