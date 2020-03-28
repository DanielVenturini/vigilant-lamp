import logging
from colorama import Fore

logging.basicConfig(format='%(message)s', level=logging.INFO)


def open_file(path, mode='r'):
    try:
        return open(path, mode)
    except FileNotFoundError:
        logging.error(Fore.RED + 'Error: file {} not found'.format(path))
        exit(1)
