from .converter import Converter

import re

class FilePathConverter(Converter):

	REG_DRIVE_START = r"^[A-Za-z]:\\"	

	REG_PROG_FILES = r"program files (\(x86\))?"
	
	def make_slash_reg_compatible(self, line):
		return re.sub(r'\\+', "\\\\\\\\", line)
		# return line.replace("\\", 2*"\\")

	def replace_program_files(self, line):
		# print("line", line)
		return re.sub(self.REG_PROG_FILES, ".*", line, flags=re.IGNORECASE)

	def standardize_drive_letter(self, line):
		return re.sub(self.REG_DRIVE_START, self.REG_DRIVE_START, line, flags=re.IGNORECASE)

	def apply(self, line):
		# The sequence matters!
		res = line

		res = self.replace_program_files(res)
		res = self.standardize_slash(res)
		res = self.escape_special_chars(res)
		res  = self.make_slash_reg_compatible(res)
		res = self.standardize_drive_letter(res)
		

		return res



