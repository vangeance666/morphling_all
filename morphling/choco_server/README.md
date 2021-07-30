# 🍫 Introduction

This folder constitutes the following to facilitate "morphling" sandbox analysis workflow. 

| Modules | Purpose | 
| --- | --- |
| Internalizer | Cache and internalize desired packages into your local chocolatey server with required dependencies | 
| Updater | Verify local repository stored packages are synced up-to-date with the Chocolatey Community Repository  |
| File+Registry Snapshotter | Capture differences made within two points of capture | 
| Signature Generator | Generates signatures each chocolatey package will make upon installation |
| Signature Converter | Sanitizes and converts package signature into CAPEv2 compatible format |

<p align="center"><img src="https://github.com/vangeance666/morphling/blob/main/choco_server/images/chocolatey.png?raw=true" width=30% height=30%></p>

<p align="center">
<img alt="Issues" src="https://img.shields.io/badge/Windows-Supported-brightgreen?style=flat&logo=Windows">
<img alt="Issues" src="https://img.shields.io/badge/Automated%20Software%20Manager-Chocolatey-blue?style=flat&logo=chocolatey">
<img alt="Issues" src="https://img.shields.io/badge/Python-v3.8.10-informational?style=flat&logo=python">
<img alt="Issues" src="https://img.shields.io/badge/Powershell-informational?style=flat&logo=powershell">

# 📜 Software/Technologies Requirements
* [Python Version 3.7 and above](https://www.python.org/downloads/)
* [Chocolatey Server](https://docs.chocolatey.org/en-us/guides/organizations/set-up-chocolatey-server)

## 🐬 Prerequisites 
1. Chocolatey server functionality needs to be up. Follow this guide [chocolatey server installation guide](https://drive.google.com/file/d/14n9SaVEjGegMRZXRYpxO5Jy1cwDilGeK/view?usp=sharing)
2. Install all dependencies `pip3 install -r requirements.txt`

## ⚡ Usage

1. Fill in the required configurations fields within `config.py`
```
# This is the repo source location
CHOCO_PUSH_SOURCE = "http://<CHOCOLATEY_IP_ADDRESS>/chocolatey/"

# Default installation path for chocolatey server local repository to store package dependencies
REPO_DEPENDENCIES_PATH = "C:\\tools\\chocolatey.server\\repo"

DEPENDENCIES_REPOINT_PATH = "http://<CHOCOLATEY_IP_ADDRESS>/repo"

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

# Port that is configured to retrieve signatures from Chocolatey using SSH
# Winexe needs to be configured
# Refer to architecture setup guide for more information
SIG_PORT = <SSH PORT> 

# For File capture
FILE_FLDR_32 = "C:\\Program Files (x86)\\"
FILE_FLDR_64 = "C:\\Program Files\\"
FILE_FLDR_APP_DATA = "C:\\Users\\User\\AppData\\"
FILE_FLDR_PROG_DATA = "C:\\ProgramData\\"
# FileCapture folders to monitor difference
FILE_FLDRS_TO_CHECK = [FILE_FLDR_32, FILE_FLDR_64, FILE_FLDR_APP_DATA, FILE_FLDR_PROG_DATA]

SYNC_MINS_COOLDOWN = 2

# Folder to dump generated signatures for CAPE to retrieve
# TAKE NOTE: Create a folder called "signatures" in the Desktop Folder
SIG_FLDR = "C:\\Users\\Administrator\\Desktop\\signatures\\"
SIG_FILE_PATH = SIG_FLDR + "files.json" 
SIG_REG_PATH = SIG_FLDR + "registry.json"
SIG_SHA256_PATH = SIG_FLDR + "hash_256.json"
```
2. Refer to the [chocolatey usage guide](https://drive.google.com/file/d/17ax51viafkSvm99SXrECSau2iqnoD-P_/view?usp=sharing) on how to use chocolatey and run the custom program syntax correctly.
