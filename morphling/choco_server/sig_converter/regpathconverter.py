import os
import re
from .converter import Converter

from consts import *

class RegPathConverter(Converter):

	REG_CONTROL_SETS = "(CurrentControlSet|ControlSet001|ControlSet002)"

	ROOT_KEY_BINDING = {
		"HKCR":	"HKEY_CLASSES_ROOT" 	
	    , "HKCU":	"HKEY_CURRENT_USER" 	
	    , "HKLM":	"HKEY_LOCAL_MACHINE" 	
	    , "HKU":	"HKEY_USERS" 			
	    , "HKCC":	"HKEY_CURRENT_CONFIG" 	
	}

	def replace_root_keys(self, line):
		for k in self.ROOT_KEY_BINDING:
			if line.upper().startswith(k):
				return line.replace(k, self.ROOT_KEY_BINDING[k], 1)
		return line

	def make_slash_reg_compatible(self, line):
		return re.sub(r'\\+', "\\\\\\\\", line)

	def handle_full_stop(self, line):
		return line.replace(".", "\\.")
		
	def trim_root_key(self, line):
		for root in ROOT_SUBKEYS:
			for sub in ROOT_SUBKEYS[root]:
				start = os.path.join(root, sub)
				if line.startswith(start):
					return line.replace(start, ".*")
		return line

	def standardize_control_sets(self, line):
		return re.sub(self.REG_CONTROL_SETS, self.REG_CONTROL_SETS, line, flags=re.IGNORECASE)

	# def allow_spacing(self, line):

	def apply(self, line):
		res = line

		# res = self.standardize_slash(res)
		res = self.make_slash_reg_compatible(res)
		res = self.escape_special_chars(res)
		res = self.trim_root_key(res)
		res = self.standardize_control_sets(res)
		res = self.replace_root_keys(res)

		
		return res