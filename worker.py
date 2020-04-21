from common import convert_datetime
from colorama import Fore, Style
from versionrangeparser import NodeVersionRangeParser
from npm.file import get_dependencies as npm_get_dependencies, save as npm_save
from npm.operations import get_times as npm_get_times


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
def get_times(times, date):

    versions = []
    date = convert_datetime(date)
    for version_info in times:
        version, v_date = version_info

        if convert_datetime(v_date) <= date:
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


# get only the versions that are equal or greater
# get all package.json and get the maximum version of specify range version
def resolve_version(dependency, version, date, pck_mng):
    times = None

    if pck_mng.__eq__('npm'):
        times = npm_get_times(dependency)

    if not times:
        return version

    # removes all version after that specify date
    versions = get_times(times, date)
    print(versions)
    # resolve the range
    nvrp = NodeVersionRangeParser()
    svr = nvrp.parse(version)
    # get the best satisfied range
    new_version = get_version(dependency, versions, svr)

    # if one version satisfies
    if new_version:
        return str(new_version)
    else:
        return version


# change all range versions in specify dependency
def worker_dependencies(dependencies, date, pck_mng):

    for dependency in dependencies:

        dep_name = dependency[0]
        dep_version = dependency[1]
        if not is_range(dep_version):
            continue

        # resolve version
        try:
            new_version = resolve_version(dep_name, dep_version, date, pck_mng)
            color = ''
        except Exception:
            new_version = dep_version
            color = Fore.RED

        print(color + '{0}@{1}'.format(dep_name, dep_version) + ' -> ' + new_version + Style.RESET_ALL)
        dependency[1] = new_version


def worker(file_obj, date, path, pck_mng):
    """
    Resolve all ranges in specify date from the package
    :param file_obj: the object file (e.g., json object for package.json)
    :param date: the specify date
    :param path: the path of file (e.g., path/to/package.json)
    :param pck_mng: the package manager specify in the lampy.py->languagesConfiguration (e.g., 'npm', 'gem')
    """
    if pck_mng.__eq__('npm'):
        dependencies = npm_get_dependencies(file_obj)
        worker_dependencies(dependencies, date, pck_mng)
        npm_save(file_obj, dependencies, path)