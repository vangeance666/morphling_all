import os
import json
import sys
import time
import subprocess
import ast

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from tkinter import *
from tkinter import filedialog

from controller import *

import base64

if 'pythonw' in sys.executable:
	f = open(os.devnull, 'w')
	sys.stdout = f
	sys.stderr = f

def returnImagePath(s):
	cwd_url = '/'.join(os.getcwd().split(os.sep))
	return str("file://" + cwd_url + "/" + s)

def saveDataStringIntoPath(s, rel_path):
	#The string returned from web will have twolines spacing 
	#This function will correct the format of the string and save as a temp csv file to be used.
	s.replace('\r\n', '\n')
	# cwd_url = '/'.join(os.getcwd().split(os.sep))
	# save_path = "file://" + cwd_url + "/" + rel_path
	with open(rel_path, 'wb') as f:
		f.write(s)
	return

class OutStream(object):

	def __init__(self, file_object=None):
		if 'pythonw' in sys.executable:
			self._f = None
		else:
			self._f = sys.__stdout__ if file_object is None else file_object

	def __lshift__(self, arg):
		if self._f is not None:
			self._f.write(str(arg))
		return self

def print_exc():
	if 'pythonw' not in sys.executable:
		traceback.print_exc()

cout = OutStream()


def BoolDict(d):
	from collections import defaultdict
	dd = defaultdict(lambda:False)
	dd.update(d if d else dict())
	return dd

#For make_browser_navless
def execute_chrome(browser, script=''):
	browser.command_executor._commands["SET_CONTEXT"] = ("POST", "/session/$sessionId/moz/context")
	browser.execute("SET_CONTEXT", {"context": "chrome"})
	browser.execute_script("""
		var h = function(id) { document.getElementById(id).style.display = 'none' };
		var b = function(k,v) { Services.prefs.setBoolPref(k,v) };
		var i = function(k,v) { Services.prefs.setIntPref(k,v) };%s;"""%(script))
	browser.execute("SET_CONTEXT", {"context": "content"})


#To make firefox browser not have navigation bar to improve UI experience
def make_browser_navless(browser, script=''):	
	execute_chrome(browser, """
	b('browser.tabs.drawInTitlebar', false);
	i('network.http.max-persistent-connections-per-server', 128); 
	h('nav-bar');
	h('TabsToolbar');
	b('reader.parse-on-load.enabled', false);
	b('browser.pocket.enabled', false);
	b('browser.tabs.forceHide', true);
	b('browser.helperApps.deleteTempFileOnExit', true);
	b('toolkit.cosmeticAnimations.enabled', false);
	i('browser.sessionhistory.max_total_viewers', 0);
	i('browser.sessionhistory.max_entries', 0);
	i('browser.sessionhistory.max_serialize_back', 0);
	i('browser.sessionstore.interval', 999999999);
	i('browser.sessionstore.interval.idle', 999999999);
	b('browser.sessionhistory.resume_from_crash', false);%s;"""%(script))

# Minor tweaks
def make_browser_fast(browser, script=''):
	make_browser_navless(browser, """
	i('browser.display.use_document_fonts', 0);
	b('browser.display.show_image_placeholders', false);
	i('layout.frame_rate', 10);%s;"""%(script))

# Personal Cout function to print text
class OutStream(object):
	def __init__(self, file_object=None):
		if 'pythonw' in sys.executable:
			self._f = None
		else:
			self._f = sys.__stdout__ if file_object is None else file_object

	def __lshift__(self, arg):
		if self._f is not None:
			self._f.write(str(arg))
		return self

def print_exc():
	if 'pythonw' not in sys.executable:
		traceback.print_exc()

cout = OutStream()


# Class to set 
class Browser(object):

	def __init__(self, headless=False, gen_iid=False, msg_box_title=None, msg_box_text=None, msg_box_timeout=60*60*1000):
		self._headless = headless
		show_msg_box = (msg_box_title is not None or msg_box_text is not None)
		if show_msg_box:
			gen_iid = True
		if gen_iid:
			try:
				iid_chars = string.ascii_uppercase+string.ascii_lowercase+string.digits
				self._iid = ''.join(random.choice(iid_chars) for x in xrange(16))
				if not os.path.exists('iids'):
					os.mkdir('iids')
				elif not os.path.isdir('iids'):
					os.unlink('iids')
					os.mkdir('iids')
				with open(os.path.join('iids', self._iid), 'w') as iid_f:
					iid_f.write('')
			except e:
				pass
		else:
			self._iid = None
		if show_msg_box and self._iid is not None:
			if msg_box_title is None:
				msg_box_title = ''
			if msg_box_text is None:
				msg_box_text = ''
			prog = '\n'.join(("""title="%s";text="%s";delay=%d;iid="%s";"""%(msg_box_title, msg_box_text, msg_box_timeout, self._iid),
				"""import os""",
				"""try:\n\timport Tkinter as tk\nexcept:\n\timport tkinter as tk""",
				"""r = tk.Tk()\nr.title(title)\ntk.Label(r, text=text).pack()""",
				"""def cf():\n\tif os.path.isfile(os.path.join('iids',iid)):r.after(3000, cf)\n\telse:r.destroy()""",
				"""r.after(3000, cf);r.after(delay, lambda: r.destroy())\nr.mainloop()"""))
			try:
				pkwargs = dict()
				pkwargs['startupinfo'] = subprocess.STARTUPINFO()
				pkwargs['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW
				pkwargs['creationflags'] = 0x00000008
				subprocess.Popen(['pythonw', '-c', prog], close_fds=platform.system() != 'Windows', **pkwargs)
			except:
				subprocess.Popen(['python', '-c', prog], close_fds=platform.system() != 'Windows')

	def __enter__(self):
		MH = 'MOZ_HEADLESS'
		h = os.environ[MH] if MH in os.environ else None
		if self._headless:
			os.environ[MH] = '1'

		# self._firefox_binary = FirefoxBinary(os.getcwd()+"\\FirefoxPortable\\App\\Firefox\\firefox.exe")
		# self._browser = webdriver.Firefox(firefox_binary=self._firefox_binary)

		exec_path = os.path.join(os.getcwd(), "dependencies/geckodriver")
		print("exec_path", exec_path)
		self._browser = webdriver.Firefox(executable_path=exec_path)

		if h is None and MH in os.environ: 
			del os.environ[MH]
		elif h is not None: 
			os.environ[MH] = h
		self._browser.iid = self._iid
		self._open = True
		return self._browser

	def _quit(self):
		if self._iid is not None:
			try:
				os.unlink(os.path.join('iids', self._iid))
			except Exception as e:
				pass
		if self._open:
			pid = self._browser.service.process.pid
			self._browser.quit()
			try:
				os.kill(pid, signal.SIGTERM)
			except Exception as e:
				pass
			self._open = False

	def __exit__(self, type, value, traceback):
		self._quit()

	def __del__(self):
		self._quit()

def tk_ask_input(mode="file"):
	root = Tk()
	# root = tk.Tk()
	root.withdraw()

	# Make it almost invisible - no decorations, 0 size, top left corner.
	root.overrideredirect(True)
	root.geometry('0x0+0+0')
	root.wm_attributes('-topmost', 1)
	root.deiconify()
	root.lift()
	root.focus_force()

	if mode == "file":
		ret = filedialog.askopenfilename(parent=root) # Or some other dialog
	elif mode == "folder":
		ret = str(filedialog.askdirectory(parent=root)) # Or some other dialog
	elif mode == 'files':
		ret = filedialog.askopenfilenames(parent=root) # Or some other dialog
	elif mode == 'saveas':
		ret = filedialog.asksaveasfilename(parent=root)

	root.destroy()
	return ret

# Read from this point onwards only
# ####################################
def launch():

	controller = Controller()
	

	if not controller.cape_accessible():
		print("Cape not accessible")
		return

	if not controller.fog_accessible():
		print("Fog not accessible")			
		return			

	with Browser(headless=False) as browser:

		browser.install_addon(os.path.join(os.getcwd(), "dependencies/ignore_x_frame_options_header-1.6.9-an+fx.xpi"), temporary=True)
		controller.set_web_driver(browser)

		make_browser_navless(browser)
		browser.get("file://"+os.getcwd()+"/ui/index.html")
		browser.set_script_timeout(2147483647)


		# try:
		#     myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
		#     print "Page is ready!"
		# except TimeoutException:
		#     print "Loading took too much time!"

		controller.start()

		# Constantly loop and check if any of the javascript variables are set to true. 
		while 1:
			try:	
				needs_update = BoolDict(browser.execute_async_script("""
					var callback = arguments[0];
					(function fn() {
						if (!(typeof needsUpdate === 'undefined')) {
							var t = false;
							for (var k in needsUpdate) if (needsUpdate[k]) t = true; 
							if (t) {
								var u = {};
								for (var k in needsUpdate) {
									u[k] = needsUpdate[k];
									needsUpdate[k] = false;
								}
								return callback(u);
							}
						}
						setTimeout(fn, 60);
					})();
				"""))
				if needs_update is None:
					break
				
				if needs_update['getMachineNames']:

					machines_name = controller.get_machines_name()

					cout << "Machines name: " << machines_name

					if machines_name:
						browser.execute_script("data.machineNames = {};".format(json.dumps(machines_name)))
						browser.execute_script("layout.submit.setMachinesSelect();")
					else:
						cout << "Cant browser execute script"
				if needs_update['submitPromptFile']:
					try:
						sample_path = tk_ask_input("file")
					except:
						sample_path = None

					cout << "Sample_Path " << sample_path

					if sample_path:
						browser.execute_script("layout.submit.setFileLabel('{}');".format(sample_path))


				if needs_update['submitSendFile']:
					# browser.execute_script("layout.submit.getFileLabel();")

					sample_path = browser.execute_script("return layout.submit.getFileLabel();")
					machine_name = browser.execute_script("return data.chosenMachine; data.chosenMachine ='';")

					cout << "machine name: " << machine_name << '\n'

					if machine_name not in controller.get_machines_name():
						browser.execute_script("showError('Machine not valid')")
						continue

					cout << "Received sample path: " << sample_path

					if not os.path.isfile(sample_path):
						browser.execute_script("showError('File {} does not exist.');".format(sample_path))
						continue

					controller.add_task(sample_path, machine_name)
					browser.execute_script("showSuccess('Added {} to the task queue.');".format(sample_path))


				if needs_update['homeRetrieveSubmissions']:
					cout << "---Attempting to get submissions data---\n"
					

					submission_data = controller.get_submissions_info()

					if submission_data is None:
						browser.execute_script("showError('Failed to retrive submissions info');")
						continue
					else:
						cout << "submission_data: " << submission_data << "\n"
						browser.execute_script("data.homeSubmissionsData = {};".format(json.dumps(submission_data)))
						
						browser.execute_script("layout.home.updateSubmissionTable();")
						browser.execute_script("showSuccess('Sucessfully retrived submissions info');")

					cout << "submission_data: " << submission_data

				if needs_update['machinesRetrieveData']:
					cout << "---Retrieving all machine info---"

					machines_info = controller.get_machines_info()
					cout << "machines_info: " << machines_info

					if machines_info is None:
						browser.execute_script("showError('Failed to retrive machines info');")
						continue
					else:
						browser.execute_script("data.machinesTableData = {};".format(json.dumps(machines_info)))
						browser.execute_script("layout.machines.updateMachinesTable();")

						browser.execute_script("showSuccess('Updated machines info');")

				if needs_update['taskLoadTaskData']:
					cout << "Load task details by id\n"

					task_id = browser.execute_script("return data['taskGetId'];")
					cout << "task_id: " << task_id <<  " " << type(task_id) << "  \n"
					browser.execute_script("data.taskGetId = '';")

					task_details = controller.get_task_info(task_id)

					cout << "task_details : " << task_details << "\n"
					# print("task_details", task_details)

					if task_details:
						cout << "Success load task data\n"
						browser.execute_script("data.taskTableDetails = {};".format(json.dumps(task_details)))

						browser.execute_script("layout.task.setTaskTableData(data.taskTableDetails); ")
						browser.execute_script("layout.task.loadIframe('{}')".format(task_id))
					else:
						cout << "Failed load task data\n"
						browser.execute_script("showError('Unable to get task details');")

				if needs_update['taskDisableResubmission']:
					cout << "---taskDisableResubmission: \n"
					task_id = browser.execute_script("return data.taskTableDetails.id;")
					cout << "task_id: " << task_id << "\n"
					controller.stop_task_resubmit(task_id)

				if needs_update['taskEnableResubmission']:
					cout << "---taskEnableResubmission: \n"
					task_id = browser.execute_script("return data.taskTableDetails.id;")
					cout << "task_id: " << task_id << "\n"
					controller.enable_task_resubmit(task_id)

				if needs_update['taskForceResubmit']:
					cout << "Force resubmit an ID" << "\n"
					task_id = browser.execute_script("return data.taskResubmitId;")
					browser.execute_script("data.taskResubmitId ='';")
					cout << "Task_id: " <<  task_id << "\n"

					if task_id:
						controller.force_resubmit_task(task_id)

			except Exception as e:
				cout << "portable exception\n"
				controller.stop_threads()
				raise

launch()