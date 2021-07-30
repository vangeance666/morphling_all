import hashlib

class Hasher:

	BLOCK_SIZE = 65536

	def hash_256_file(self, file_path) -> str:
		try:
			file_hash = hashlib.sha256() 
			with open(file_path, 'rb') as f: 
			    fb = f.read(self.BLOCK_SIZE) 
			    while len(fb) > 0: 
			        file_hash.update(fb) 
			        fb = f.read(self.BLOCK_SIZE) 
			return file_hash.hexdigest()
		except Exception as e:
			raise e
			return False
		
		

