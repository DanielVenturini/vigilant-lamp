import json
import semver
import network as ntw
from versionrangeparser import NodeVersionRangeParser


# save the package.json
def save(package, path):
    json.dump(package, open(path, 'w'), sort_keys=True, indent=2)


# verify if this is a range version
def is_range(version):
    return version.__contains__('^') or \
           version.__contains__('~') or \
           version.__contains__('>') or \
           version.__contains__('<') or \
           version.__contains__('*') or \
           version.__contains__('.x')


# get all versions until the specify date
def get_times(time, date):

    versions = []
    for version in list(time.keys()):
        if version.__eq__('created') or version.__eq__('modified'):
            continue

        if time[version] <= date:
            versions.append(version)

    return versions


# get only the versions that is major
# get all package.json's and get the maximum version of specify range version
def resolve_version(dependency, version, date):

    time = ntw.get(dependency)['time']
    versions = get_times(time, date)
    # resolve the range
    nvrp = NodeVersionRangeParser()
    svr = nvrp.parse(version)
    # get the best satisfies range
    new_version = svr.best_satisfies(versions)

    # if one version satisfies
    if new_version:
        return str(new_version)
    else:
        return version


# change all range versions in specify dependency
def worker_dependeny(dependencies, date):

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

        print('{0}@{1}'.format(dependency, dependencies[dependency]) + ' -> ' + new_version)
        dependencies[dependency] = new_version



# change all range versions in package.json
def worker(package, date, path):

    # all types of dependencies to NPM
    typesDependencies = ['dependencies',         \
                         'devDependencies',      \
                         'peerDependencies',     \
                         'optionalDependencies', \
                         'globalDependencies']

    for types in typesDependencies:
        try:

            # get all dependencies
            dependencies = package[types]
            worker_dependeny(dependencies, date)

        except KeyError:
            continue

    save(package, path)