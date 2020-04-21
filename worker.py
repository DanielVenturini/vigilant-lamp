import json
import network as ntw
from colorama import Fore, Style
from versionrangeparser import NodeVersionRangeParser
from npm.file import get_dependencies as npm_get_dependencies, save as npm_save


# save the package.json
def save(package, path):
    json.dump(package, open(path, 'w'), indent=2)


# verify if this is a range version
def is_range(version):
    return version.__contains__('^') or \
           version.__contains__('~') or \
           version.__contains__('>') or \
           version.__contains__('<') or \
           version.__contains__('*') or \
           version.__contains__('.x') or \
           version.__contains__('latest') or \
           version.__contains__('||') or \
           version.__contains__('next') or \
           version.__eq__('')


# get all versions until the specify date
def get_times(time, date):

    versions = []
    for version in list(time.keys()):
        if version.__eq__('created') or version.__eq__('modified'):
            continue

        if time[version] <= date:
            versions.append(version)

    return versions


# get the resolved version and verify if exists
def get_version(dependency, versions, svr):
    if not len(versions):
        return None

    resolved_version = svr.best_satisfies(versions)
    # verify if resolved_version exists
    if ntw.exists(dependency, resolved_version):
        return resolved_version
    else:
        versions.remove(str(resolved_version))
        return get_version(dependency, versions, svr)


# get only the versions that is major
# get all package.json's and get the maximum version of specify range version
def resolve_version(dependency, version, date):

    time = ntw.get(dependency)['time']
    versions = get_times(time, date)
    # resolve the range
    nvrp = NodeVersionRangeParser()
    svr = nvrp.parse(version)
    # get the best satisfies range
    new_version = get_version(dependency, versions, svr)

    # if one version satisfies
    if new_version:
        return str(new_version)
    else:
        return version


# change all range versions in specify dependency
def worker_dependencies(dependencies, date):

    for dependency in dependencies:

        # get the version
        version = dependencies[dependency]
        if not is_range(version):
            continue

        # resolve version
        try:
            new_version = resolve_version(dependency, version, date)
        except Exception:
            new_version = version

        if new_version.__eq__(version):
            color = Fore.RED
        else:
            color = ''

        print(color + '{0}@{1}'.format(dependency, dependencies[dependency]) + ' -> ' + new_version + Style.RESET_ALL)
        dependencies[dependency] = new_version


def worker(file_obj, date, path, pck_mng):
    """
    Resolve all ranges in specify date from the package
    :param file_obj: the object file (e.g., json object for package.json)
    :param date: the specify date
    :param path: the path of file (e.g., path/to/package.json)
    :param pck_mng: the package manager specify in the lampy.py->languagesConfiguration (e.g., 'npm', 'gem')
    """

    if (pck_mng.__eq__('npm')):
        dependencies = npm_get_dependencies(file_obj)
        worker_dependencies(dependencies, date)
        npm_save(file_obj, dependencies, path)