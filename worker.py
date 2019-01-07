import json
import semver
import network as ntw


# save the package.json
def save(package, path):
    json.dump(package, open(path, 'w'), sort_keys=True, indent=2)


# verify if this is a range version
def is_range(version):
    return version.__contains__('^') or \
           version.__contains__('~') or \
           version.__contains__('>') or \
           version.__contains__('<')


# get all versions until the specify date
def get_times(time, date):

    new_time = {}
    for version in list(time.keys()):
        if time[version] <= date:
            new_time[version] = time[version]

    return new_time


# get all package.json's and get the maximum version of specify range version
def resolve_version(dependency, version, date):

    time = ntw.get(dependency)['time']
    time = get_times(time, date)
    exit(0)
    #print('time: ', time)


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