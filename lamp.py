import sys
import json
import worker as wk
from sys import exit


# get the path/to/package.json
def resolve_package(package_path):

    try:
        return json.load(open(package_path))
    except Exception as ex:
        print('ERR: ' + str(ex))
        exit(1)


# verify 'date' key in package.json
def verify_date(package):

    try:
        return package['date']
    except:
        print('ERR: package hasn\'t `date´ key.')
        exit(1)


'''
    L A M P
'''


# check the call
if sys.argv.__len__() != 2:
    print('USE:')
    print('    lamp package.json')
    print('or')
    print('    lamp path/to/package.json')
    exit(0)

path = sys.argv[1]
# get package.json
package = resolve_package(path)

# verify if package.json has 'date' key
date = verify_date(package)

# resolve all range versions
wk.worker(package, date, path)