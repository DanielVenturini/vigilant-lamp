import semantic_version
import traceback
import time
import bisect


class SemanticVersionRange(set):
    wildcards = ('x', 'X', '*', 'latest')
    def addComparatorToRange(self, comparator):
        try:
            comp1, comp2 = SemanticVersionComparatorFacade().simpleComparators(comparator)

            self.add(comp1)
            self.add(comp2)
        except KeyError:
            try:
                comp1, comp2 = SemanticVersionComparatorFacade().hyphenComparators(comparator)

                self.add(comp1)
                self.add(comp2)
            except KeyError as ke:
                raise KeyError("bad comparator format, cannot add comparator '{}' to range '{}'".format(str(comparator),
                                                                                                        str(self)))

    def __formatSpecStrComposed(self):
        if self.__len__() == 0:
            return ">=0.0.0"

        spec_str = ""
        for comparator in self:
            operator, version, pre_release, build, raw_string = comparator.unpack()

            if build not in (None, ""):
                if pre_release not in (None, ""):
                    spec_str = spec_str + "," + "{}{}-{}+{}".format(operator, version, pre_release, build)
                else:
                    spec_str = spec_str + "," + "{}{}+{}".format(operator, version, build)
            elif pre_release not in (None, ""):
                spec_str = spec_str + "," + "{}{}-{}".format(operator, version, pre_release)
            else:
                spec_str = spec_str + "," + "{}{}".format(operator, version)

        return spec_str[1:]

    # TODO: optimize from O(|comparator|*|version|)
    # TODO: simple optimize checking if there are overlaping comparators
    def satisfies(self, versions_to_match):
        spec_str = self.__formatSpecStrComposed()
        spec = semantic_version.Spec(spec_str)

        vs = []
        for version in versions_to_match:
            try:
                vs.append(semantic_version.Version(version, partial=False))
            except ValueError:
                #print("can't parse version string '%s'", version)
                pass

        # TODO: evaluate diff in performance from spec.filter() and the for below (v in versions)
        # satisfies = []
        # for v in versions:
        #   sem_ver = semantic_version.Version(v, partial=True)
        #
        #   if sem_ver in spec:
        #      satisfies.append(sem_ver)
        #
        # return satisfies

        return spec.filter(vs)

    def __formatSpecStr(self, comparator):
        operator, version, pre_release, build, raw_string = comparator.unpack()

        if build not in (None, ""):
            if pre_release not in (None, ""):
                spec_str = "{}{}-{}".format(operator, version, pre_release)
            else:
                spec_str = "{}{}".format(operator, version)
        elif pre_release not in (None, ""):
            spec_str = "{}{}-{}".format(operator, version, pre_release)
        else:
            spec_str = "{}{}".format(operator, version)

        return spec_str

    def best_satisfies(self, versions_to_match):
        versions = []
        for version in versions_to_match:
            try:
                versions.append(semantic_version.Version(version, partial=False))
            except ValueError:
                #print("can't parse version string '%s'", version)
                pass

        if self.__len__() == 0:
            spec = semantic_version.Spec(">=0.0.0")
            max_in_range = spec.select(versions)

            return max_in_range

        ranges = list()
        for range in self:
            try:
                ranges[range["logical_or"]].append(range)
            except IndexError:
                ranges.insert(range["logical_or"], [range])

        max_satisfy = None
        for range in ranges:
            spec_str = ""
            for comparator in range:
                spec_str = spec_str + "," + self.__formatSpecStr(comparator)
            spec_str = spec_str[1:]

            spec = semantic_version.Spec(spec_str)
            max_in_range = spec.select(versions)

            if max_in_range is None:
                continue

            if max_satisfy is not None:
                if max_in_range > max_satisfy:
                    max_satisfy = max_in_range
            else:
                max_satisfy = max_in_range

        return max_satisfy

    def max_satisfies(self, versions_to_match):
        versions = []
        for version in versions_to_match:
            versions.append(semantic_version.Version(version, partial=False))

        matches = set(versions)
        sorted_matches = []
        for comparator in self:
            matches_per_comparator = set()

            spec = semantic_version.Spec(self.__formatSpecStr(comparator))
            for version in spec.filter(versions):
                matches_per_comparator.add(version)

                try:
                    if version not in sorted_matches:
                        bisect.insort(sorted_matches, version)
                except ValueError:
                    #print("can't parse version string '%s'", version)
                    pass

            matches = matches.intersection(matches_per_comparator)

        return [version for version in sorted_matches if version in matches]


class SemanticVersionComparatorFacade():
    wildcards = ('x', 'X', '*', 'latest')

    def __unpackWildcards(self, version, pre, build, logical_or, raw_string):
        major, minor, patch = self.__becomeWildcardVersion(version)

        if major in self.wildcards:
            major, minor, patch = 0, 0, 0

            v1 = "{}.{}.{}".format(major, minor, patch)

            comp1 = SemanticVersionComparator(
                {"operator": ">=", "version": v1, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})

            return comp1, comp1
        elif minor in self.wildcards:
            minor, patch = 0, 0

            v1 = "{}.{}.{}".format(major, minor, patch)

            major = int(major) + 1
            major = str(major)

            v2 = "{}.{}.{}".format(major, minor, patch)

            comp1 = SemanticVersionComparator(
                {"operator": ">=", "version": v1, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})
            comp2 = SemanticVersionComparator(
                {"operator": "<", "version": v2, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})

            return comp1, comp2
        elif patch in self.wildcards:
            patch = 0

            v1 = "{}.{}.{}".format(major, minor, patch)

            minor = int(minor) + 1
            minor = str(minor)

            v2 = "{}.{}.{}".format(major, minor, patch)

            comp1 = SemanticVersionComparator(
                {"operator": ">=", "version": v1, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})
            comp2 = SemanticVersionComparator(
                {"operator": "<", "version": v2, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})

            return comp1, comp2
        else:
            raise ValueError("no wildcards to unpack on string '{}'".format(raw_string))

    def __unpackTilde(self, version, pre, build, logical_or, raw_string):
        # version can be splited with "." ?
        major, minor, patch = self.__becomeWildcardVersion(version)

        if major in self.wildcards:
            v1 = "{}.{}.{}".format(0, 0, 0)

            comp1 = SemanticVersionComparator(
                {"operator": ">=", "version": v1, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})

            return comp1, comp1

        elif minor in self.wildcards:
            v1 = "{}.{}.{}".format(major, 0, 0)

            if int(major) > 0:
                m = int(major) + 1
                m = str(m)

                v2 = "{}.{}.{}".format(m, 0, 0)
            else:
                v2 = "{}.{}.{}".format(1, 0, 0)
        elif patch in self.wildcards:
            v1 = "{}.{}.{}".format(major, minor, 0)

            m = int(minor) + 1
            m = str(m)

            v2 = "{}.{}.{}".format(major, m, 0)
        else:
            v1 = "{}.{}.{}".format(major, minor, patch)

            m = int(minor) + 1
            m = str(m)

            v2 = "{}.{}.{}".format(major, m, 0)

        comp1 = SemanticVersionComparator(
            {"operator": ">=", "version": v1, "pre_release": pre, "build": build,
             "logical_or": logical_or, "raw_string": raw_string})
        comp2 = SemanticVersionComparator(
            {"operator": "<", "version": v2, "pre_release": pre, "build": build,
             "logical_or": logical_or, "raw_string": raw_string})

        return comp1, comp2

    def __becomeWildcardVersion(self, version):
        try:
            # can version be splited with 3 "." ?
            major, minor, patch = version.split(".")

            if major in self.wildcards:
                minor, patch = ("x", "x")
            elif minor in self.wildcards:
                patch = "x"
        except ValueError:
            # if v1 cannot be splited with 2 "."
            patch = "x"
            try:
                major, minor = version.split(".")

                if major in self.wildcards:
                    minor = "x"
            except ValueError:
                # if version cannot be splited with 1 "."
                minor = "x"
                major = version

        return major, minor, patch

    def hyphenComparators(self, comparator):
        try:
            comparator["hyphen"]
            v1 = comparator["part1"]
            v2 = comparator["part2"]

            try:
                comp1, comp2_trash = self.__unpackWildcards(v1, "", "", comparator["logical_or"], comparator["hyphen"])
            except ValueError:
                comp1 = None

            comp2 = None

            v2_operator = "<="
            try:
                major, minor, patch = v2.split(".")
            except ValueError:
                # if v1 cannot be splited with 2 "."
                patch = 0
                v2_operator = "<"

                try:
                    major, minor = v2.split(".")
                    try:
                        minor = int(minor) + 1
                        minor = str(minor)
                    except ValueError as ve:
                        try:
                            comp1_trash, comp2 = self.__unpackWildcards(v2, "", "", comparator["logical_or"], comparator["hyphen"])
                        except:
                            raise ve
                except ValueError:
                    minor = 0
                    major = v2
                    v2_operator = "<"

                    try:
                        major = int(major) + 1
                        major = str(major)
                    except ValueError as ve:
                        try:
                            comp1_trash, comp2 = self.__unpackWildcards(v2, "", "", comparator["logical_or"], comparator["hyphen"])
                        except:
                            raise ve

            v2 = "{}.{}.{}".format(major, minor, patch)

            # TODO: pre_release and build informations are lost here when the range string is a hyphen range
            if comp1 is None:
                comp1 = SemanticVersionComparator(
                    {"operator": ">=", "version": v1, "pre_release": "", "build": "",
                     "logical_or": comparator["logical_or"], "raw_string": comparator["hyphen"]})
            if comp2 is None:
                comp2 = SemanticVersionComparator(
                    {"operator": v2_operator, "version": v2, "pre_release": "", "build": "",
                     "logical_or": comparator["logical_or"], "raw_string": comparator["hyphen"]})

            return comp1, comp2
        except KeyError:
            raise KeyError(
                "bad comparator format, must be a dictionary with fields 'hyphen', 'part1' and 'part2', but found {}:'{}'".format(
                    type(comparator), str(comparator)))

    def __unpackExact(self, version, pre, build, logical_or, raw_string):
        # version can be splited with "." ?
        major, minor, patch = self.__becomeWildcardVersion(version)

        if major in self.wildcards:
            v1 = "{}.{}.{}".format(0, 0, 0)

            comp1 = SemanticVersionComparator(
                {"operator": ">=", "version": v1, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})

            return comp1, comp1

        elif minor in self.wildcards:
            v1 = "{}.{}.{}".format(major, 0, 0)
            v2 = "{}.{}.{}".format(str(int(major) + 1), 0, 0)

            comp1 = SemanticVersionComparator(
                {"operator": ">=", "version": v1, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})

            comp2 = SemanticVersionComparator(
                {"operator": "<", "version": v2, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})

            return comp1, comp2

        elif patch in self.wildcards:
            v1 = "{}.{}.{}".format(major, minor, 0)
            v2 = "{}.{}.{}".format(major, str(int(minor) + 1), 0)

            comp1 = SemanticVersionComparator(
                {"operator": ">=", "version": v1, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})

            comp2 = SemanticVersionComparator(
                {"operator": "<", "version": v2, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})

            return comp1, comp2

        else:
            v1 = "{}.{}.{}".format(major, minor, patch)

            comp1 = SemanticVersionComparator(
                {"operator": "==", "version": v1, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})

            return comp1, comp1


    def __unpackCaret(self, version, pre, build, logical_or, raw_string):
        # version can be splited with "." ?
        major, minor, patch = self.__becomeWildcardVersion(version)

        if major in self.wildcards:
            v1 = "{}.{}.{}".format(0, 0, 0)

            comp1 = SemanticVersionComparator( \
                {"operator": ">=", "version": v1, "pre_release": pre, "build": build,
                 "logical_or": logical_or, "raw_string": raw_string})

            return comp1, comp1

        elif minor in self.wildcards:
            v1 = "{}.{}.{}".format(major, 0, 0)

            if int(major) > 0:
                m = int(major) + 1
                m = str(m)

                v2 = "{}.{}.{}".format(m, 0, 0)
            else:
                v2 = "{}.{}.{}".format(1, 0, 0)

        elif patch in self.wildcards:
            v1 = "{}.{}.{}".format(major, minor, 0)

            if int(major) > 0:
                m = int(major) + 1
                m = str(m)

                v2 = "{}.{}.{}".format(m, 0, 0)
            else:
                if int(minor) > 0:
                    m = int(minor) + 1
                    m = str(m)

                    v2 = "{}.{}.{}".format(0, m, 0)
                else:
                    v2 = "{}.{}.{}".format(0, 1, 0)

        else:
            v1 = "{}.{}.{}".format(major, minor, patch)

            if int(major) > 0:
                m = int(major) + 1
                m = str(m)

                v2 = "{}.{}.{}".format(m, 0, 0)
            else:
                if int(minor) > 0:
                    m = int(minor) + 1
                    m = str(m)

                    v2 = "{}.{}.{}".format(0, m, 0)
                else:
                    if int(patch) > 0:

                        m = int(patch) + 1
                        m = str(m)

                        v2 = "{}.{}.{}".format(0, 0, m)
                    else:
                        v2 = "{}.{}.{}".format(1, 0, 0)

        comp1 = SemanticVersionComparator( \
            {"operator": ">=", "version": v1, "pre_release": pre, "build": build,
             "logical_or": logical_or, "raw_string": raw_string})
        comp2 = SemanticVersionComparator(
            {"operator": "<", "version": v2, "pre_release": pre, "build": build,
             "logical_or": logical_or, "raw_string": raw_string})

        return comp1, comp2

    def __zeroPadVersion(self, version_str):
        try:
            major, minor, patch = version_str.split(".")

            if (major in self.wildcards) or (minor in self.wildcards) or (patch in self.wildcards):
                raise SyntaxError("version '{}' contains wildcards symbols and cannot be zero padded".format(version_str))
        except ValueError:
            patch = 0

            try:
                major, minor = version_str.split(".")

                if (major in self.wildcards) or (minor in self.wildcards):
                    raise SyntaxError(
                        "version '{}' contains wildcards symbols and cannot be zero padded".format(version_str))

            except ValueError:
                minor = 0
                major = version_str

                if (major in self.wildcards):
                    raise SyntaxError(
                        "version '{}' contains wildcards symbols and cannot be zero padded".format(version_str))

        return "{}.{}.{}".format(major, minor, patch)

    def simpleComparators(self, comparator):
        comp_cp = {}
        for k, v in comparator.items():
            if v is not None:
                comp_cp.update({k: v})
            else:
                comp_cp.update({k: ""})

        version = comp_cp["ver_num"]
        pre = comp_cp["pre"]
        build = comp_cp["build"]
        raw_string = comp_cp["simple"]
        logical_or = comparator["logical_or"]
        operator = comp_cp["operator"]

        try:
            if comp_cp["operator"] == "~":
                try:
                    return self.__unpackTilde(version, pre, build, logical_or, raw_string)
                except:
                    pass
            elif comp_cp["operator"] == "^":
                try:
                    return self.__unpackCaret(version, pre, build, logical_or, raw_string)
                except:
                    pass
            elif comp_cp["operator"] in (">", "<", ">=", "<=", "=", ""):
                if comp_cp["operator"] in ("=", ""):
                    comp_cp["operator"] = "=="
                    
                    return self.__unpackExact(version, pre, build, logical_or, raw_string)

                try:
                    comp_cp["ver_num"] = self.__zeroPadVersion(comp_cp["ver_num"])
                except SyntaxError:
                    try:
                        return self.__unpackWildcards(version, pre, build, logical_or, raw_string)
                    except ValueError:
                        pass

            if comp_cp["operator"] in (None, ''):
                comp1 = SemanticVersionComparator(
                    {"operator": comp_cp["operator"], "version": comp_cp["ver_num"],
                     "pre_release": comp_cp["pre"], "build": comp_cp["build"],
                     "logical_or": comparator["logical_or"], "raw_string": comp_cp["simple"]})
            else:
                comp1 = SemanticVersionComparator(
                    {"operator": comp_cp["operator"], "version": comp_cp["ver_num"],
                     "pre_release": comp_cp["pre"], "build": comp_cp["build"],
                     "logical_or": comparator["logical_or"], "raw_string": comp_cp["simple"]})

            return comp1, comp1
        except KeyError:
            raise KeyError(
                "bad comparator format, must be a dictionary with fields 'simple', 'logical_or', 'operator', " +
                "'ver_num', 'pre' and 'build', but found {}:'{}'".format(
                    type(comparator), str(comparator)))


class SemanticVersionComparator(dict):
    # a semantic version comparator is composed of
    # an 'operator' field (>,<,>=,<=,=)
    # a 'version' field (major.minor.patch)
    # a 'pre_release' field (-prerelease)
    # a 'build' field (+build)

    def unpack(self):
        return self["operator"], self["version"], self["pre_release"], self["build"], self["raw_string"]

    def __hash__(self): return hash(id(self))

    def __eq__(self, x): return x is self

    def __ne__(self, x): return x is not self