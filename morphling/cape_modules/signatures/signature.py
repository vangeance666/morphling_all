class Signature:

	name = ""
	description = ""
	severity = 1
	categories = []
	authors = []

	def __init__(self, results):
		self.results = results
		self.data = []


	def get_info(self):
		return  {
			"name": self.name
			, "description": self.description
			, "data": self.data
		}