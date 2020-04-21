import logging
import requests
from colorama import Fore
from datetime import datetime

logging.basicConfig(format='%(message)s', level=logging.INFO)


def open_file(path, mode='r'):
    try:
        return open(path, mode)
    except FileNotFoundError:
        logging.error(Fore.RED + 'Error: file {} not found'.format(path))
        exit(1)


#########
# NETWORK
#########

def get(url):
    response = requests.request('GET', url, timeout=3)

    if response.status_code == 404:
        raise Exception()
    else:
        return response


def exists(url_version):
    response = requests.request('HEAD', url_version, timeout=3)
    return not response.status_code == 404


#################
# TIME OPERATIONS
#################

def get_time_hour(time):
    try:
        return int(time.split(':')[0])
    except:
        return 0


def get_time_minutes(time):
    try:
        return int(time.split(':')[1])
    except:
        return 0


def get_time_seconds(time):
    try:
        return int(time.split(':')[2].split('.')[0])
    except:
        return 0


def get_time_microsecond(time):
    try:
        return int(time.split(':')[2].split('.')[0])
    except:
        return 0


# from a '2015-03-09T03:09:05.477Z' returns a object
def convert_datetime(date):
    pieces = date.split('T')
    req = pieces[0]  # '2015-03-09'

    # convert the strings to int
    y, m, d = map(lambda x: int(x), req.split('-'))

    # there is no 03:09:05.477Z
    if len(pieces) == 1:
        return datetime(y, m, d)

    h = get_time_hour(pieces[1])
    mn = get_time_minutes(pieces[1])
    s = get_time_seconds(pieces[1])
    ms = get_time_microsecond(pieces[1])

    return datetime(y, m, d, h, mn, s, ms)