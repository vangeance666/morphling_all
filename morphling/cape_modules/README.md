# 🍁 Introduction

<p> Morphling is an automated malware analysis platform, which employs the usage of technologies such as CAPE sandbox, FOG server, and Chocolatey to automatically prepare an environment that morphs itself to fit the requirements of evasive malware samples at each analysis cycle. 

<p> Upon completion of the entire analysis process, malware analysts will be assured that the malicious behavior of the evasive malware sample that has been submitted would have been successfully registered and captured in Morphling.

<p align="center"><img src="https://github.com/vangeance666/choco_tools/blob/main/cape_modules/images/Morphling%20icon.png?raw=true" width=30% height=30%></p> <br>

<p align="center">
<img alt="Issues" src="https://img.shields.io/badge/Linux-Supported-brightgreen?style=flat&logo=Linux">
<img alt="Issues" src="https://img.shields.io/badge/Malware%20Analysis%20Sandbox-CAPEv2-blue">
<img alt="Issues" src="https://img.shields.io/badge/Image%20Management%20Server%20-FOG%20Server-blue">
<img alt="Issues" src="https://img.shields.io/badge/Automated%20Software%20Manager-Chocolatey-blue?style=flat&logo=chocolatey">
<br>
<img alt="Issues" src="https://img.shields.io/badge/Python-v3.8.10-informational?style=flat&logo=python">
<img alt="Issues" src="https://img.shields.io/badge/-HTML-blue?style=flat&logo=HTML5">
<img alt="Issues" src="https://img.shields.io/badge/-Javascript-blue?style=flat&logo=javascript">
<img alt="Issues" src="https://img.shields.io/badge/-jQuery-blue?style=flat&logo=jquery">
<img alt="Issues" src="https://img.shields.io/badge/Selenium-informational?style=flat&logo=selenium">
<img alt="Issues" src="https://img.shields.io/badge/Firefox-informational?style=flat&logo=firefox">
 
## 📜 Software/Technologies Requirements
* [Python Version 3.7 and above](https://www.python.org/downloads/)
* [Mozilla FireFox](https://www.mozilla.org/en-GB/firefox/all/#product-desktop-release)
* [CAPEv2 Sandbox](https://github.com/kevoreilly/CAPEv2)
* [FOG Server](https://github.com/FOGProject/fogproject)
* [Chocolatey Server](https://docs.chocolatey.org/en-us/guides/organizations/set-up-chocolatey-server)

## 🐬 Installation Guide
1. Follow the [installation guide](https://docs.google.com/document/d/1-kzPp1hSPoYgpDja6G2PT536xA7I6bhhP93Wu3HMTIc/edit?usp=sharing) to setup and configure all the technologies stated above.
2. Download the Morphling's source code packages from [Github](https://github.com/vangeance666/choco_tools/archive/refs/heads/main.zip)
3. Navigate to root folder and install the python3 dependencies `pip3 install -r requirements.txt`
4. In root folder, execute portable.py `python3 portable.py`

### ⚡ Configuration

Fill in the required configurations fields within the below configuration files before proceeding.

1. ``configs/config.py``

```
# Refer to setup guide on how to generate FOG's API Token
# For FOG API to work
FOG_IP = "<FOG_IP_ADDRESS>"
FOG_USER_TOKEN = "<FOG_USER_API_TOKEN>"
FOG_API_TOKEN = "<FOG_API_TOKEN>"
	
# Default location of CAPEv2 Analysis Folder
CAPE_ANALYSIS_FOLDER = "/opt/CAPEv2/storage/analyses" 

# For remotely executing choco installation commands on analysis machines
# Include address of the chocolatey server
LOCAL_REPO_SRC = "http://<CHOCOLATEY_IP_ADDRESS>/chocolatey"

# Values required by CAPEv2 rest API
# https://capev2.readthedocs.io/en/latest/usage/api.html
# Default Username & Password that is configured during the whole architecture setup
# Refer to architecture setup guide on how to generate CAPE's API Token 
SUPER_USER_NAME = "cape"
SUPER_USER_PASSWORD = "toor"
SUPER_USER_AUTH_TOKEN = "Token <CAPE_USER_AUTH>"

# Default URL to execute all CAPE rest API functions
CAPE_API_BASE_URL = "http://127.0.0.1:8000/apiv2/"

# Default Configuration files of all analysis machines.# Default Configuration files of all analysis machines.
CONF_MACHINES_PATH = "/opt/CAPEv2/conf/physical.conf"

# Chocolatey's IP Address
INNER_CHOCO_IP = "192.168.180.135"

# Chocolatey Server Details to pull required signatures
# Default Username for Windows Server 2019 (Server to retrieve signatures from)
SIG_GEN_USER_NAME = "Administrator"
SIG_GEN_HOSTNAME = "192.168.180.135"

# File paths of signature generated at the chocolatety server
# TAKE NOTE: Ensure it tallys with where you configured the generator to save at
# A folder named "signatures" must be created in Chocolatey's desktop folder
CHOCO_SIG_FOLDER = "C:/Users/Administrator/Desktop/signatures/"
CHOCO_SIG_FILE_PATH = CHOCO_SIG_FOLDER + "files.json"
CHOCO_SIG_REG_PATH = CHOCO_SIG_FOLDER + "registry.json"
CHOCO_SIG_SHA256_PATH = CHOCO_SIG_FOLDER + "hash_256.json"

# Locations of where to save signatures generated by choco server
# A folder named "signatures" must be created in CAPEv2's desktop folder
LOCAL_SIG_FOLDER = "/home/cape/Desktop/signatures/"
LOCAL_SIG_FILE_PATH = LOCAL_SIG_FOLDER + "files.json"
LOCAL_SIG_REG_PATH = LOCAL_SIG_FOLDER + "registry.json"
LOCAL_SIG_SHA256_PATH = LOCAL_SIG_FOLDER + "hash_256.json"

# All submissions with their tasks will saved into this file path 
# serving as a form of "database to keep track"
# Submission data will be put into the working directory of cape_modules folder
# Can be customized to any path
DB_SUBMISSIONS_PATH = os.path.join(os.getcwd()+"/storage/submissions.data"
```

2. ``/opt/CAPEv2/conf/physical.conf``

Machine credentials and details are referenced from CAPE's physical.conf file.
The username, password, and hostname of every analysis machine is required to function normally.

```
<Code Snippet>
 
[<WIN7_MACHINE_REGISTERED_ON_FOG>]
# Specify the label name of the current machine as specified in your
# physical machine configuration.
label = <hostname_registered_on_fog_server>

# Please specify the username and password of the windows 7 machine.
username = <WIN7_USERNAME> 
password = <WIN7_PASSWORD>
# Specify the operating system platform used by current machine
# [windows/darwin/linux].
platform = windows

# Specify the IP address of the current machine. Make sure that the IP address
# is valid and that the host machine is able to reach it. If not, the analysis
# will fail.
ip = <FOG_IP_ADDRESS>
```

3. ``/ui/js/init.js``
```
<Code Snippet>
 
var layout = {};

var baseCapeAnalysisUrl = "http://127.0.0.1:<Port Number of CAPE Web Interface>/analysis/"

var eleClass = {
	navBtn: "nav-btn",
	taskActionBtn: 'task-action-btn', taskPrevTaskBtn: 'task-prev-task-btn',

	homeTaskIdLink: "home-task-id-link"
}
```

# 🔨 Collaborators
| Name                   | GitHub                          |
|------------------------|---------------------------------|
| Patrick Kang Wei Sheng | https://github.com/vangeance666 |
| Jared Tan Jing Jie     | https://github.com/jrdtan       |
| Javier Lim Zheng Hao   | https://github.com/javvylx      |

© 2021, All Rights Reserved
<br>