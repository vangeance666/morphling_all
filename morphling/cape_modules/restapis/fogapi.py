
import requests
from configs.config import *

class FogApi:

	def __init__(self, ip=None):
		self._ip = ip or FOG_IP

		self._headers = {
			'content-type': 'application/json'
			, 'fog-user-token': FOG_USER_TOKEN 
			, 'fog-api-token': FOG_API_TOKEN
		}

		self._base_url = "http://{}/fog/".format(self._ip)
		print("self._base_url", self._base_url)

	def is_accessible(self) -> bool:
		url = os.path.join(self._base_url, "system/info")
		try:
			r = requests.get(url, headers=self._headers)
			return r.status_code == 200
		except:
			return False


	def machine_has_task(self, machine_name=None) -> bool:
		""" Checks if a machine is analying currently
			analyzing a sample by seeing if there is a
			task assigned to it. 
		
		Args:
		    machine_name (str, optional): Label of machine
		
		Returns:
		    bool: If machine is in analyzing mode (task assigned)
		"""
		url = os.path.join(self._base_url, "task/current")

		try:
			r = requests.get(url, headers=self._headers)
		except:
			raise

		if r.status_code != 200:
			return False

		data = r.json()

		if not data or not data['tasks']:
			return False

		try:
			for task in data['tasks']:
				if task['host']['name'] == machine_name:
					return True
		except Exception as e:
			print(e)

		return False		

		#TODO parse data dict and interpret whether online it is currently doing task
		# based on machine_name
		print(data)

		





		