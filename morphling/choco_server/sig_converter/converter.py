from abc import ABC, abstractmethod

class Converter(ABC):
	
	# SPECIAL_CHARS = ['[' ,'\\','^',"'" ,"$" ,".","|","?" ,"*","+","(" ,")"]
	SPECIAL_CHARS = ['[' ,'^',"'" ,"$" ,"|","?","+","(" ,")"]

	def standardize_slash(self, line):
		return line.replace("/", "\\")

	def escape_special_chars(self, line):
		res = line
		for c in self.SPECIAL_CHARS:
			res = res.replace(c, "\\"+c)
		return res
		
	@abstractmethod
	def apply(self, line):
		raise NotImplementedError

