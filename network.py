import requests

'''
	request to http://registry.npmjs.org/ and get all package.json
	from a specify package

	interface:
		get(package_name)
'''

def get(package_name):

	response = requests.get('http://registry.npmjs.org/' + package_name)

	if response.status_code == 404:
		print('package `{0}´ not found.'.format(package_name))
		raise Exception()
	else:
		return response.json()