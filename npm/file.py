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


# get all dependencies in package.json
def get_dependencies(file_obj):
    dependencyTypes = ['dependencies',
                         'devDependencies',
                         'peerDependencies',
                         'optionalDependencies',
                         'globalDependencies']

    dependencies = []
    for dep_type in dependencyTypes:
        # get all dependencies for, e.g., devDependencies
        try:
            for dependency_name in list(file_obj[dep_type].keys()):
                # e.g., (mongoose, ^4.5.9, devDependencies)
                dependencies.append((dependency_name, file_obj[dep_type][dependency_name], dep_type))
        except KeyError:
            # if, e.g., peerDependencies does not exist in package.json
            continue

    return dependencies

# insert in the file_obj all resolved dependencies
def insert_dependencies(file_obj, dependencies):
    for dep in dependencies:
        dep_name = dep[0]
        resolved_version = dep[1]   # dependencies, devDependencies, peerDependencies, ...
        field = dep[2]

        file_obj[field][dep_name] = resolved_version

    return file_obj

# save package.json
def save(file_obj, dependencies, path):
    file_obj = insert_dependencies(file_obj, dependencies)

    json.dump(file_obj, open_file(path, 'w'), indent=2)
