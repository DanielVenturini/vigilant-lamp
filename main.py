# THIS FILE SHOULDN'T BE IMPORTED
# IMPORT AND USE THE FUNCTIONS IN lamp.py INSTEAD

# This file reads the call arguments from the system
# Then, verifies if the file arguments is all ok
# For the last, call the lampy.py to start work

import sys
from lamp import lamp
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)


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


# the first argument is the file name, that is, main.py
# the second one may be the versioning_file
# the third one may be the option --language= (unused for now)
# one of those may be the option --help
arguments = sys.argv[1:]
# for now, options will be ignored
files, options = split_arguments(arguments)
# execute lamp
lamp(files)