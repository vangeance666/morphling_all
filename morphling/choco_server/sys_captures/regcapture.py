import os
import sys

from collections import defaultdict
# from regutil import *
# from snapshot import *
from .regutil import *
from .snapshot import *
from consts import ROOT_KEY_STR

# https://docs.python.org/3/library/winreg.html#hkey-constants

class RegCapture(Snapshot):

    SNAPS_SAVE_FLDR = os.path.join(os.path.dirname(__file__), "registry_snaps")

    def __init__(self, to_analyse: list):

        self.reg_util = RegUtil()

        self.captures: dict = {
            "first": {}, "second": {}
        }

        self.reg_keys: list = to_analyse

        self._difference = {}

        self._difference_done: bool = False

        self._first_capture = []
        self._second_capture = []


    def _shorten(self, hash_string):
        return hashlib.sha256(hash_string.encode()).hexdigest()

    def _snap_key_to_file(self, root_key, key, save_path):
        with winreg.OpenKey(root_key, key, 0, winreg.KEY_READ) as opened_key:
            winreg.SaveKey(opened_key, save_path)

    def get_key_details(self, root_key, key) -> dict:
        with winreg.OpenKey(root_key, key, 0, winreg.KEY_READ) as opened_key:
            return self.reg_util.iter_key_with_values(root_key, key, opened_key)

    def first_snap(self):
        all_keys = []
        for P in self.reg_keys:
            all_keys += self.reg_util.rec_tranverse_tree(P['root_key'], P['key']) 
        self._first_capture = list(set(all_keys))

    def second_snap(self):
        all_keys = []
        for P in self.reg_keys:
            all_keys += self.reg_util.rec_tranverse_tree(P['root_key'], P['key'])             
        self._second_capture = list(set(all_keys))

    def _calculate_difference(self):
        # ret = [x for x in self._second_capture if x not in self._first_capture]
        # print("ret", ret)

        # return ret
        return {
            "added": [x for x in self._second_capture if x not in self._first_capture],
            "removed": [b for b in self._first_capture if b not in self._second_capture]
        }       

    def evaluate_difference(self) -> bool:
        # try:

        self._difference = self._calculate_difference()
        self._difference_done = True
        # except Exception as e:
        #     print(e)
        # finally:
        return self._difference_done

    def can_export(self) -> bool:
        return self._difference_done

    @property
    def difference(self):
        return self._difference

    @property
    def first_capture(self):
        return self._first_capture
        # return self.captures['first'] if "first" in self.captures else None

    @property
    def second_capture(self):
        return self._second_capture
        # return self.captures['second'] if "second" in self.captures else None

# if __name__ == '__main__':

    

    


