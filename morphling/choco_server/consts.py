import winreg

# Stuff for capturing difference
ROOT_KEY_STR = {
    winreg.HKEY_CLASSES_ROOT:"HKCR",
    winreg.HKEY_CURRENT_USER:"HKCU",
    winreg.HKEY_LOCAL_MACHINE:"HKLM",
    winreg.HKEY_USERS:"HKU",
    winreg.HKEY_CURRENT_CONFIG:"HKCC"
}

ROOT_SUBKEYS = {
	"HKLM" : [
		"Hardware"
		, "Sam"
		, "Security"
		, "Software"
		, "System"
	]
	, "HKCU" : [
		"AppEvents"
		, "Console"
		, "Control Panel"
		, "Environment"
		, "EUDC"
		, "Keyboard Layout"
		, "Network"
		, "Printers"
		, "Software"
		, "System"
		, "Uninstall"
		, "Volatile Environment"
	]
}

# Stuff required for internalizer