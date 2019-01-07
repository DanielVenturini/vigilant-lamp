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


# change all range versions in specify dependency
def worker_dependeny(dependencies, date):

    for dependency in dependencies:

        # get the version
        version = dependencies[dependency]
        if not is_range(version):
            continue

        print('dep: ', dependency, 'version: ', dependencies[dependency])
        #dependencies[dependency] = 'venturini'


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