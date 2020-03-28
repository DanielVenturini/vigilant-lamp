import json
import logging
from colorama import Fore
from common import open_file

logging.basicConfig(format='%(message)s', level=logging.INFO)


# get the path/to/package.json
def get_file(package_path):
    try:
        return json.load(open_file(package_path))
    except Exception as ex:
        logging.error(Fore.RED + 'ERR: ' + str(ex))
        raise


# verify 'date' key in package.json
def verify_date(package):
    try:
        return package['date']
    except KeyError:
        logging.error(Fore.RED + 'ERR: file {} hasn\'t `date´ key.')
        raise


# save package.json
def save_package(package, path):
    json.dump(package, open_file(path, 'w'), indent=2)
