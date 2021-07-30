from .snapshot import *

import os

from config import *

class FilesCapture(Snapshot):

    def __init__(self, folders: list): 

        print("---files init---")


        self.captures = {
            "first": {}, "second": {}
        }

        self.folders: list = folders
        self._difference: set = {}
        self._difference_done: bool = False

        # print("self.folders: ", self.folders)

    def _snap_dir_files(self, folder_path) -> set:
        ret = set()
        for r, _, files in os.walk(folder_path):
            for f in files:
                full_path = os.path.join(r, f)
                if os.path.isfile(full_path):
                # if os.path.exists(full_path):
                    ret.add(full_path)
        return ret

    def _dump(self,file_path,  data):
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            return False
        return True

    def first_snap(self):
        print("files first snap")
        for folder in self.folders:
            self.captures["first"][folder] = self._snap_dir_files(folder)

        # self._dump("C:\\Users\\Administrator\\Desktop\\first.json", self.captures['first'])

    def second_snap(self):
        for folder in self.folders:
            self.captures["second"][folder] = self._snap_dir_files(folder)

        # self._dump("C:\\Users\\Administrator\\Desktop\\second.json", self.captures['second'])

    def evaluate_difference(self) -> bool:
        # try:
        self._difference = {F: list(self.captures['first'][F].symmetric_difference(self.captures['second'][F])) for F in self.captures['first']}
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
        return self.captures["first"]

    @property
    def second_capture(self):
        return self.captures["second"]

    


 




if __name__ == '__main__':
    print("ha")