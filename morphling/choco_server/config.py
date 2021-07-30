import winreg

# All packages will be choco push to this location
CHOCO_PUSH_SOURCE = "http://192.168.180.135/chocolatey/"

# Default installation path for chocolatey server local repository to store package dependencies
REPO_DEPENDENCIES_PATH = "C:\\tools\\chocolatey.server\\repo"

# Base path used when refactoring nupkg packages powershell files.
DEPENDENCIES_REPOINT_PATH = "http://192.168.180.135/repo"

# Default installation path for chocolatey server local repository
PUSHED_PACKAGES_PATH = "C:\\tools\\chocolatey.server\\App_Data\\Packages"
DOWNLOAD_DUMP_FOLDER = "C:\\Users\\Administrator\\Desktop\\testinternalize"


# RegCapture registry keys to capture difference
# Format should be as shown below. 
# For types of root key, https://docs.python.org/3/library/winreg.html#hkey-constants
REG_KEYS_TO_CHECK = [
    {'name': 'HKLM_Uninstall'
        , "root_key": winreg.HKEY_LOCAL_MACHINE
        , "key":"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
    }, 
    {'name': '64-bit-machine'
        , "root_key": winreg.HKEY_LOCAL_MACHINE
        , "key":"Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
    }
]

SIG_PORT = 5511 # Port to retrieve sig from choco server using SSH

# For File capture
FILE_ALL = "C:\\"
FILE_FLDR_32 = "C:\\Program Files (x86)\\"
FILE_FLDR_64 = "C:\\Program Files\\"
FILE_FLDR_APP_DATA = "C:\\Users\\User\\AppData\\"
FILE_FLDR_PROG_DATA = "C:\\ProgramData\\"
# FileCapture folders to monitor difference
FILE_FLDRS_TO_CHECK = [FILE_FLDR_32, FILE_FLDR_64, FILE_FLDR_APP_DATA, FILE_FLDR_PROG_DATA]

SYNC_MINS_COOLDOWN = 2

# Folder to dump generated signatures for CAPE to retrieve
SIG_FLDR = "C:\\Users\\Administrator\\Desktop\\signatures\\"
SIG_FILE_PATH = SIG_FLDR + "files.json" 
SIG_REG_PATH = SIG_FLDR + "registry.json"
SIG_SHA256_PATH = SIG_FLDR + "hash_256.json"

#Ignore
DEMO_PACKAGES_INFO = [
	{'name': 'nmap', 'version': '7.80'}
	, {'name': 'filezilla', 'version': '3.53.1'}
	, {'name': 'vlc', 'version': "3.0.14"}
	, {'name': 'opera', 'version': "76.0.4017.177"}
]


