import requests
from colorama import Fore, Style

'''
	request to http://registry.npmjs.org/ and get all package.json
	from a specify package

	interface:
		get(package_name)
'''
# index 0 is the package_name; index 1 is the version
default_url = 'https://registry.npmjs.org/{0}/-/{0}-{1}.tgz'

def get(package_name):

	response = requests.get('http://registry.npmjs.org/' + package_name)

	if response.status_code == 404:
		print(Fore.RED + 'package `{0}´ not found.'.format(package_name))
		raise Exception()
	else:
		return response.json()

def exists(package_name, resolved_version):
	url_package = default_url.format(package_name, resolved_version)
	response = requests.head(url_package)
	if response.status_code == 404:
		return False
	else:
		return True