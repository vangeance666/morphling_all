import inspect
import pkgutil

def import_plugin(name):
	try:
		module = __import__(name, globals(), locals(), ["dummy"])
	except (ImportError, SyntaxError) as e:
		print('Unable to import plugin "{0}": {1}'.format(name, e))
		return
	else:
		# ToDo remove for release
		try:
			load_plugins(module)
		except Exception as e:
			print(e, sys.exc_info())


def import_package(package):
	prefix = package.__name__ + "."
	for _, name, ispkg in pkgutil.iter_modules(package.__path__, prefix):
		if ispkg:
			continue

		# Disable initialization of disabled plugins, performance++
		_, category, module_name = name.split(".")
		if category in config_mapper and module_name in config_mapper[category].fullconfig and config_mapper[category].get(module_name).get("enabled", False) is False:
			continue

		try:
			import_plugin(name)
		except Exception as e:
			print(e)


def load_plugins(module):
	for _, value in inspect.getmembers(module):
		if inspect.isclass(value):
			if issubclass(value, Auxiliary) and value is not Auxiliary:
				register_plugin("auxiliary", value)
			elif issubclass(value, Machinery) and value is not Machinery and value is not LibVirtMachinery:
				register_plugin("machinery", value)
			elif issubclass(value, Processing) and value is not Processing:
				register_plugin("processing", value)
			elif issubclass(value, Report) and value is not Report:
				register_plugin("reporting", value)
			elif issubclass(value, Signature) and value is not Signature:
				register_plugin("signatures", value)
			elif issubclass(value, Feed) and value is not Feed:
				register_plugin("feeds", value)


def register_plugin(group, name):
	global _modules
	group = _modules.setdefault(group, [])
	group.append(name)


def list_plugins(group=None):
	if group:
		return _modules[group]
	else:
		return _modules
def import_plugin(name):
	try:
		module = __import__(name, globals(), locals(), ["dummy"])
	except (ImportError, SyntaxError) as e:
		print('Unable to import plugin "{0}": {1}'.format(name, e))
		return
	else:
		# ToDo remove for release
		try:
			load_plugins(module)
		except Exception as e:
			print(e, sys.exc_info())


def import_package(package):
	prefix = package.__name__ + "."
	for _, name, ispkg in pkgutil.iter_modules(package.__path__, prefix):
		print("name", name)
		if ispkg:
			continue

		# Disable initialization of disabled plugins, performance++
		category, module_name = name.split(".")
		if category in config_mapper and module_name in config_mapper[category].fullconfig and config_mapper[category].get(module_name).get("enabled", False) is False:
			continue

		try:
			import_plugin(name)
		except Exception as e:
			print(e)


def load_plugins(module):
	for _, value in inspect.getmembers(module):
		if inspect.isclass(value):
			if issubclass(value, Auxiliary) and value is not Auxiliary:
				register_plugin("auxiliary", value)
			elif issubclass(value, Machinery) and value is not Machinery and value is not LibVirtMachinery:
				register_plugin("machinery", value)
			elif issubclass(value, Processing) and value is not Processing:
				register_plugin("processing", value)
			elif issubclass(value, Report) and value is not Report:
				register_plugin("reporting", value)
			elif issubclass(value, Signature) and value is not Signature:
				register_plugin("signatures", value)
			elif issubclass(value, Feed) and value is not Feed:
				register_plugin("feeds", value)


def register_plugin(group, name):
	global _modules
	group = _modules.setdefault(group, [])
	group.append(name)


def list_plugins(group=None):
	if group:
		return _modules[group]
	else:
		return _modules