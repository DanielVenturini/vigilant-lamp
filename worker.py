from common import convert_datetime
from colorama import Fore, Style
from versionrangeparser import NodeVersionRangeParser
from npm.file import get_dependencies as npm_get_dependencies, save as npm_save
from npm.operations import get_times as npm_get_times, version_exists as npm_version_exists


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


# return True if the version is pre-release
def is_pre(version):
    return version.lower().__contains__('-alpha') or \
           version.lower().__contains__('-beta') or \
           version.lower().__contains__('-rc') or \
           version.lower().__contains__('-dev') or \
           version.lower().__contains__('-git') or \
           version.lower().__contains__('-patch') or \
           version.lower().__contains__('-pre')


# if 'version' is not pre-release, remove all pre-releases from 'versions'
def verify_pre(version, versions):
    # keeps the pre-releases; one of them may match the range
    if is_pre(version):
        return versions

    # 'version' is not pre-release, thus remove all pre-releases from version
    return list(filter(lambda v: not is_pre(v), versions))


# get all versions until the specify date
def get_versions(times, date):

    versions = []
    date = convert_datetime(date)
    for version_info in times:
        version, v_date = version_info

        if convert_datetime(v_date) <= date:
            versions.append(version)

    return versions


# get the resolved version and verify if exists
def get_resolved_version(dependency, versions, svr, pck_mng):
    if not len(versions):
        return None

    version_exists = None
    resolved_version = svr.best_satisfies(versions)
    # just get the function pointer for each pkg_mng
    if pck_mng.__eq__('npm'):
        version_exists = npm_version_exists

    # verify if resolved version exists
    if version_exists(dependency, resolved_version):
        return resolved_version
    else:
        versions.remove(str(resolved_version))
        return get_resolved_version(dependency, versions, svr, pck_mng)


# get only the versions that are equal or greater
# get all package.json and get the maximum version of specify range version
def resolve_version(dependency, version, date, pck_mng):
    times = None

    if pck_mng.__eq__('npm'):
        times = npm_get_times(dependency)

    if not times:
        return version

    # removes all version after that specify date
    versions = get_versions(times, date)
    versions = verify_pre(version, versions)
    # resolve the range
    nvrp = NodeVersionRangeParser()
    svr = nvrp.parse(version)
    # get the best satisfied range
    new_version = get_resolved_version(dependency, versions, svr, pck_mng)

    # if one version satisfies
    if new_version:
        return str(new_version)
    else:
        return version


# change all range versions in specify dependency
def worker_dependencies(dependencies, date, pck_mng):

    new_dependencies = []
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
        new_dependencies.append((dep_name, new_version, dependency[2]))

    return new_dependencies

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
        dependencies = worker_dependencies(dependencies, date, pck_mng)
        npm_save(file_obj, dependencies, path)