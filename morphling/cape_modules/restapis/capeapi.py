import sys
import os
import json

import requests

from configs.config import *



END_POINTS = {
	
	"SUBMIT_FILE":  {"MODE": "POST","PATH": os.path.join(CAPE_API_BASE_URL,"tasks/create/file")},
	"SUBMIT_URL":   {"MODE": "POST","PATH": os.path.join(CAPE_API_BASE_URL,"tasks/create/url")},

	"LIST_TASKS":   {"MODE": "GET","PATH": os.path.join(CAPE_API_BASE_URL,"tasks/list")},
	"VIEW_TASK":    {"MODE": "GET","PATH": os.path.join(CAPE_API_BASE_URL,"tasks/view")},
	"DELETE_TASK":  {"MODE": "GET","PATH": os.path.join(CAPE_API_BASE_URL,"tasks/delete")},

	"GET_REPORT":       {"MODE": "GET","PATH": os.path.join(CAPE_API_BASE_URL,"tasks/get/report")}, #see v2 only
	"GET_SCREENSHOTS":  {"MODE": "GET","PATH": os.path.join(CAPE_API_BASE_URL,"tasks/screenshots")},
	"VIEW_FILES":       {"MODE": "GET","PATH": os.path.join(CAPE_API_BASE_URL,"files/view")},
	"GET_FILES":        {"MODE": "GET","PATH": os.path.join(CAPE_API_BASE_URL,"files/get")},
	"GET_PCAP":         {"MODE": "GET","PATH": os.path.join(CAPE_API_BASE_URL,"pcap/get")},

	"LIST_MACHINES": {"MODE": "GET","PATH": os.path.join(CAPE_API_BASE_URL,"machines/list")},
	"VIEW_MACHINE": {"MODE": "GET","PATH": os.path.join(CAPE_API_BASE_URL,"machines/view")},
	"CUCKOO_STATUS": {"MODE": "GET","PATH": os.path.join(CAPE_API_BASE_URL,"cuckoo/status")}
}

class CapeApi:

	def __init__(self, auth_token=None):
		self._auth_token = auth_token or SUPER_USER_AUTH_TOKEN
		self._auth_headers = {'Authorization': self._auth_token}
		
	def is_accessible(self) -> bool:
		try:
			url = CAPE_API_BASE_URL
			r = requests.get(url, headers=self._auth_headers)
			return r.status_code == 200
		except Exception as e:
			return False
	#Works 
	def submit_file_sample(self, sample_path, machine_name):
		url = END_POINTS['SUBMIT_FILE']['PATH']+'/'

		print("url", url)
		
		with open(sample_path, 'rb') as sample:

		    multipart_file = {
		    	"file": (sample.name, sample)
		    	, "machine": (None, machine_name)
		    }

		    r = requests.post(url, files=multipart_file, headers=self._auth_headers)

		if r.status_code != 200:	
			return None
		return r.json()		

	# Works
	def list_tasks(self) -> dict:
		url = END_POINTS['LIST_TASKS']['PATH']+'/'
		print("url", url)

		r = requests.get(url, headers=self._auth_headers)

		if r.status_code != 200:
			print("Failed to list tasks")
			return None

		return r.json()

	# Works
	def view_task(self, task_id=None) -> dict:
		if not task_id:
			return task_id

		url = os.path.join(END_POINTS['VIEW_TASK']['PATH'],str(task_id)) + '/'

		r = requests.get(url, headers=self._auth_headers)

		if r.status_code != 200:
			print("r.status_code", r.status_code)
			if r.status_code == 404:	
				print("Task not found")

			return None
		return r.json()

	# Works
	def get_report(self, task_id, export_format="json") -> dict:
		url = os.path.join(
			END_POINTS['GET_REPORT']['PATH']
			,str(task_id)
			, export_format) + '/'

		r = requests.get(url, headers=self._auth_headers)
		
		if r.status_code != 200:
			if r.status_code == 400:
				print("Invalid report format")
			elif r.status_code == 404:
				print("Report not found")
			return None

		return r.json()

	#works
	def list_machines(self) -> dict:
		url = END_POINTS['LIST_MACHINES']['PATH'] + '/'

		r = requests.get(url, headers=self._auth_headers)

		if r.status_code != 200:
			print("Error getting machines status")
			return None

		return r.json()

	#Works
	def view_machine(self, machine_name=None) -> dict:
		if not machine_name:
			return None

		url = os.path.join(END_POINTS['VIEW_MACHINE']['PATH']
			, machine_name) + '/'

		print("url", url)

		try:
			r = requests.get(url, headers=self._auth_headers)
			print("r", r)
		except:
			return None

		if r.status_code != 200:
			if r.status_code == 404:
				print("Machine not found")
			return None

		return r.json()


if __name__ == '__main__':
	C = CapeApi()
	C.submit_file_sample("/home/cape/Desktop/small.exe")
	# print(C.list_tasks())
	# print(C.view_task(1))
	# print(C.get_report(2))
	# print(C.list_machines())
	# print(C.view_machine("win7clone"))


	# C.submit_file_sample("/home/cape/Desktop/small.exe")




	








