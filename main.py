# THIS FILE SHOULDN'T BE IMPORTED
# IMPORT AND USE THE FUNCTIONS IN lamp.py INSTEAD

# This file reads the call arguments from the system
# Then, verifies if the file arguments is all ok
# For the last, call the lampy.py to start work

import sys
from lamp import lamp
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)


# get the arguments and returns the files
def get_files_from_arguments(arguments):
    files = []

    for argument in arguments:
        if not argument.startswith('-'):
            files.append(argument.lower())	# Gemfile and gemfile are the same

    return files


# the first argument is the file name, that is, main.py
# the second one may be the versioning_file
# the third one may be the option --language= (unused for now)
# one of those may be the option --help
arguments = sys.argv[1:]
# for now, options will be ignored
files = get_files_from_arguments(arguments)
# execute lamp
lamp(files)