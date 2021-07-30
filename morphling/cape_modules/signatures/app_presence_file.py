import json
import os

from configs.config import *
from .signature import Signature

class AppPresenceFile(Signature):

    name = "app_presence_file"
    description = "To extract chocolatey packages to install based on what file it checks"
    severity = -1
    categories = ["context"]
    authors = ["boomer_kang"]

    def run(self) -> bool:

        choco_sig_file = CHOCO_SIG_FILE_PATH

        # '/home/cape/Desktop/signatures/files.json'

        if not os.path.isfile(choco_sig_file):
            self.data.append("Choco registry signature file not found.")
            return False

        if os.stat(choco_sig_file).st_size == 0:
            self.data.append("Choco registry signature file is empty.")
            return False

        try:
            with open(choco_sig_file, 'r', encoding="UTF-8", errors='ignore') as f:
                pkgs_sig = json.load(f)
        except:
            self.data.append("Error loading json signature file.")
            return False

        store = set() #To make sure unique entries

        for pkg in pkgs_sig:

            if not all(K in pkg for K in ('package_name', 'version', 'signatures')):
                continue

            for pkg_files in pkg['signatures']:
                for files_path in self.results['behavior']['summary']['files']:
                    try:
                        if re.match(pkg_files, files_path, flags=re.IGNORECASE):
                            dict_str = "{{'package_name': '{}', 'version': '{}'}}".format(pkg['package_name'], pkg['version'])
                            store.add(dict_str)
                    except:
                        continue

        if store:
            self.data = [{"package_found": dict_str} for dict_str in store]
            return True

        return False
