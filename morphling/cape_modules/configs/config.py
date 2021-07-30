import os

# Refer to setup guide on how to generate FOG's API Token
# For FOG API to work
FOG_IP = "192.168.180.129"
FOG_USER_TOKEN = "NGU3NWUxOWRmY2ZkOWQ3ODM0MThjMWI4ODRlMTFlZTdkYzYyYmI0ODI0MzkwM2FhMGZjMmE5NjcyNWMwMDZiYmVmZGZiMTYxODJlNzE1MjY5ODIwYzcyYTFlYTRlZGJjZGQwNmRhZThiMTI1MWE4ZTM4ZTliMmQzNDM4YmQwM2Q"
FOG_API_TOKEN = "OWRjMTIxNzU0OGEzOGI5YjU1MTcwOTRhNmY5ZTE3MTNiNDgyNjA1OTRlNmEzODcxMGU0ZWNiZTYzOTllYmUxYTdkNjQ3ZWYxY2MwZTI4MTUyYjQ0MGRhN2I0YThhMGY1ZTM1MzcxNDYwYzdiOWRmMjBlYTVjYTMxZDY0OWI2ZTA"

# Default location of CAPEv2 Analysis Folder	
CAPE_ANALYSIS_FOLDER = "/opt/CAPEv2/storage/analyses"

# For remotely executing choco installation commands on analysis machines
# Include address of the chocolatey server
LOCAL_REPO_SRC = "http://192.168.180.135/chocolatey"

# Values required by CAPEv2 rest API
# https://capev2.readthedocs.io/en/latest/usage/api.html
# Default Username & Password that is configured during the whole architecture setup
# Refer to architecture setup guide on how to generate CAPE's API Token 
SUPER_USER_NAME = "cape"
SUPER_USER_PASSWORD = "toor"
SUPER_USER_AUTH_TOKEN = "Token 4488a1c8fcf70297bf0ef5299636e6434722dba7"

# Default URL to execute all CAPE rest API functions
CAPE_API_BASE_URL = "http://127.0.0.1:8000/apiv2/"

# Configuartion files of all analysis machines.
CONF_MACHINES_PATH = "/opt/CAPEv2/conf/physical.conf"

# 
INNER_CHOCO_IP = "192.168.180.135"

# 
SIG_GEN_USER_NAME = "Administrator"
SIG_GEN_HOSTNAME = "192.168.180.135"


# File paths of signatures generated at Choco Server side which will be synced into this PC
CHOCO_SIG_FOLDER = "C:/Users/Administrator/Desktop/signatures/"
CHOCO_SIG_FILE_PATH = CHOCO_SIG_FOLDER + "files.json"
CHOCO_SIG_REG_PATH = CHOCO_SIG_FOLDER + "registry.json"
CHOCO_SIG_SHA256_PATH = CHOCO_SIG_FOLDER + "hash_256.json"


# Save path of all the signatures 
LOCAL_SIG_FOLDER = "/home/cape/Desktop/signatures/"
LOCAL_SIG_FILE_PATH = LOCAL_SIG_FOLDER + "files.json"
LOCAL_SIG_REG_PATH = LOCAL_SIG_FOLDER + "registry.json"
LOCAL_SIG_SHA256_PATH = LOCAL_SIG_FOLDER + "hash_256.json"


# All submissions with their tasks will saved into this file path 
# serving as a form of "database to keep track"
# Submission data will be put into the working directory of cape_modules folder
# Can be customized to any path
DB_SUBMISSIONS_PATH = os.path.join(os.getcwd()+"/storage/submissions.data"







