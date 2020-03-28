# THIS FILE SHOULDN'T BE IMPORTED
# IMPORT AND USE THE FUNCTIONS IN lamp.py INSTEAD

# This file reads the call arguments from the system
# Then, verifies if the file arguments is all ok
# For the last, call the lampy.py to start work

import re
import sys
# import lamp
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)

languagesConfiguration = {
	'npm': ['package.json'],
	# will be supported, in future
	# 'pip': ['requirements.txt', 'pipfile', 'pyproject.toml'],
	# 'gem': ['gemfile', 'foo.gemspec']
}


def print_helper():
	pass


# get the arguments and split into a file and options
def split_arguments(arguments):
	files = []
	options = []

	for argument in arguments:
		if argument.startswith('-'):
			options.append(argument)
		else:
			files.append(argument.lower())	# Gemfile and gemfile are the same

	return files, options


# verify the filename in languagesConfiguration
# returns the ('filename', 'language')
# raise an error if filename doesn't match
def search_language(file):
	# search in each language
	for language in list(languagesConfiguration):
		if file in languagesConfiguration[language]:
			return language, file

	logging.error('Error: file \'{}\' unknown language file.'.format(file))
	exit(1)


# get the filenames and verify in languagesConfiguration
# for each filename, return the
def get_language_by_filename(files):
	info_files = []
	# verify each file
	for file in files:
		info_files.append(search_language(file))

	return info_files


# the first argument is the file name, that is, main.py
# the second one may be the versioning_file
# the third one may be the option --language= (unused for now)
# one of those may be the option --help
arguments = sys.argv[1:]
# for now, options will be ignored
files, options = split_arguments(arguments)

print(get_language_by_filename(files))