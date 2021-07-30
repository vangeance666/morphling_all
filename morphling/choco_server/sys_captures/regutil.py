import os
from collections import defaultdict
import win32security
import win32api
import winreg

# from consts import ROOT_KEY_STR
ROOT_KEY_STR = {
    winreg.HKEY_CLASSES_ROOT:"HKCR",
    winreg.HKEY_CURRENT_USER:"HKCU",
    winreg.HKEY_LOCAL_MACHINE:"HKLM",
    winreg.HKEY_USERS:"HKU",
    winreg.HKEY_CURRENT_CONFIG:"HKCC"
}

priv_flags = win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
hToken = win32security.OpenProcessToken(
    win32api.GetCurrentProcess(), priv_flags)
privilege_id = win32security.LookupPrivilegeValue(None, "SeBackupPrivilege")
win32security.AdjustTokenPrivileges(
    hToken, 0, [(privilege_id, win32security.SE_PRIVILEGE_ENABLED)])

class RegUtil:

    @staticmethod
    def full_key_path(details: dict) -> str:
        print("details", details)
        
        return os.path.join(ROOT_KEY_STR[details['root_key']], details['key'])

    def _enum_keys(self, key_obj):
        i = 0
        res = []
        while True:
            try:
                k = winreg.EnumKey(key_obj, i)
                yield k
                i += 1
            except OSError as e:
                break

    def _enum_values(self, key_obj):
        i = 0
        while True:
            try:
                k = winreg.EnumValue(key_obj, i)
                yield k
                i += 1
            except OSError as e:
                break

    def iter_key_with_values(self, root_key, key, opened_key):

        i = 0
        results = defaultdict(list)

        for sub_key_name in self._enum_keys(opened_key):
            
            try:
                value_name = "\\".join([key, sub_key_name])
                with winreg.OpenKey(root_key, value_name, 0, winreg.KEY_READ) as sub_key:           
                    for v in self._enum_values(sub_key):
                        # K = os.path.join(ROOT_KEY_STR[root_key], key)
                        K = os.path.join(ROOT_KEY_STR[root_key], key, sub_key_name)
                        # print("key :", key)
                        # print("sub_key_name :", sub_key_name)
                        # print("K :", K)         
                        results[K].append(v)
            except OSError as e:
                print(e)
                break

        return results

    def rec_tranverse_tree(self, key, sub_key, key_list=[]) -> list:

        if not sub_key:
            return key_list

        try:
            with winreg.OpenKey(key, sub_key, 0, winreg.KEY_READ) as opened_key:
                sub_keys = self._enum_keys(opened_key)
                
                for sub_key_name in sub_keys:
                    value_name = "\\".join([sub_key, sub_key_name])
                    self.rec_tranverse_tree(key, value_name, key_list)

                K = os.path.join(ROOT_KEY_STR[key], sub_key)
                datas = []

                for V in self._enum_values(opened_key):
                    # print(v)
                    datas.append(V)

                key_list.append(K)

        except Exception as e:
            # print(e)
            pass

        return key_list

