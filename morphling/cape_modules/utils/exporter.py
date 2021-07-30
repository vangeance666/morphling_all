import pickle
import os

class Exporter:
	@staticmethod
	def load(file_path):
		try:
			if os.path.getsize(file_path) > 0:   
				with open(file_path, 'rb') as f:
					ret = pickle.load(f)
					print("ret", ret)
					return ret
		except Exception as e:
			raise e 


	@staticmethod
	# can save class object but not queue object
	def save(file_path, data) -> bool:
		try:
			with open(file_path, 'wb') as f:
				pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
		except:
			return False
		return True


	