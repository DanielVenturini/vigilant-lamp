import worker as wk
from colorama import Fore
import logging
import sys
import os

from npm.file import get_file as npm_get_file, verify_date as npm_verify_date

logging.basicConfig(format='%(message)s', level=logging.INFO)

languagesConfiguration = {
    'npm': ['package.json'],
    # will be supported, in future
    # 'pip': ['requirements.txt', 'pipfile', 'pyproject.toml'],
    # 'gem': ['gemfile', 'foo.gemspec']
}


# verify the filename in languagesConfiguration
# returns the ('versioning_file', 'package manager'), eg. ('package.json', 'npm')
# raise an error if filename doesn't match
def search_language(path):
    file = os.path.split(path)[-1]  # path/to/package.json => package.json
    # search in each language
    for language in list(languagesConfiguration):
        if file in languagesConfiguration[language]:
            return path, language

    logging.error(Fore.RED + 'Error: unknown \'{}\' package manager.'.format(file))
    exit(1)


'''
    L A M P
'''


def verify_file(path, pck_mng):
    """
    This function just call the specify 'open file' and 'verify date' for specify package manager
    :param path: the path of versioning file
    :param pck_mng: package manager
    :return: The file object and its specified date: npm -> .json
    """
    file_obj, date = None, None

    if pck_mng.__eq__('npm'):
        file_obj = npm_get_file(path)
        date = npm_verify_date(file_obj)

    return file_obj, date


def lamp(files):
    """
    This function starts to solve the versioning files
    This function verifies if each file is supported, that is, has a package manager specified in languagesConfiguration
    Then, verifies if each file exists and has a 'date' key
    :param files: the versioning files path
    :return: None
    """
    for file in files:
        path, pck_mng = search_language(file)

        try:
            file_obj, date = verify_file(path, pck_mng)
        except:
            logging.error(Fore.RED + 'The file \'{}\' will not be executed'.format(file))
            continue    # doesn't execute this file

        # resolve all range versions
        wk.worker(file_obj, date, path, pck_mng)


# THIS FILE SHOULDN'T BE EXECUTED DIRECTLY
# execute main.py instead
# but, if it will, ignore the options
if __name__ == '__main__':
    files = []
    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            files.append(arg)

    lamp(files)
