import json
import os
import re

from configs.config import *
from .signature import Signature

class AppPresenceReg(Signature):

    name = "app_presence_reg"
    description = "To extract chocolatey packages to install based on registry keys found"
    severity = -1
    categories = ["context"]
    authors = ["boomer_kang"]
    
    def __init__(self, results=[]):
        self.results = results
        self.data = []

    def run(self) -> bool:

        choco_sig_file = '/home/cape/Desktop/signatures/registry.json'

        if not os.path.isfile(choco_sig_file):
            self.data.append("Choco registry signature file not found.")
            return True

        if os.stat(choco_sig_file).st_size == 0:
            self.data.append("Choco registry signature file is empty.")
            return True

        try:
            with open(choco_sig_file, 'r', encoding="UTF-8", errors='ignore') as f:
                pkgs_sig = json.load(f)
        except:
            self.data.append("Error loading json signature file.")
            return True

        store = set() #To make sure unique entries

        for pkg in pkgs_sig:

            if not all(K in pkg for K in ('package_name', 'version', 'signatures')):
                continue

            for pkg_reg_keys in pkg['signatures']:
                for keys in self.results['behavior']['summary']['keys']:
                    try:
                        if re.match(pkg_reg_keys, keys, flags=re.IGNORECASE):
                            dict_str = "{{'package_name': '{}', 'version': '{}'}}".format(pkg['package_name'], pkg['version'])
                            store.add(dict_str)
                    except:
                        continue
                        
        if store:
            self.data = [{"package_found": dict_str} for dict_str in store]
            return True
        
        return False

