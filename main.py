#!/usr/bin/env python3

"""
cppassi - C++-assistant

Ths program is a small helper for the creation of C++ files. Basically
what your IDE would do but without the IDE on the commandline.

This tool assumes a certain C++-style and has no intentions to enable
not following it. On the contrary, future versions may contain non-optional
checks on them (things like indentation with tabs or use of snake_case).
"""


import os
import os.path
import re
import sys
import configparser


__author__ = "Florian Weber (FJW)"
__license__ = "GPL-3.0+"
__version__ = "0.1"


config_file_name = "/cppassi.conf"
default_config = {"guard_prefix": ""}


def enumerate_parent_dirs():
    parents = os.getcwd().split('/')
    for i in range(len(parents), 0, -1):
        yield "/".join(parents[0:i])


def get_config_file():
    for dir in enumerate_parent_dirs():
        if os.path.isfile(dir + config_file_name):
            return dir + config_file_name
    return None


def read_config():
    config = default_config.copy()
    config_file = get_config_file()

    if config_file is None:
        return config

    configuration = configparser.ConfigParser()
    configuration.read(config_file)

    module_configuration = configuration["modules"]

    for option in ["guard_prefix", "default_namespaces"]:
        if option in module_configuration:
            config[option] = module_configuration[option]

    return config


class BadIdentifierName(Exception):
    def __init__(self, what, identifier):
        self.what = what
        self.identifier = identifier

    def __str__(self):
        return "“{}” {}".format(self.identifier, self.what)


class BadGuardName(BadIdentifierName):
    pass


def enforce_valid_identifier(name):
    if not re.match("^[A-Za-z_][A-Za-z0-9_]*", name):
        raise BadIdentifierName("doesn't match the basic format", name)
    if name.find("__") != -1:
        raise BadIdentifierName("contains double underscores", name)


def enforce_valid_guard_name(name):
    enforce_valid_identifier(name)
    if name[0] == "_":
        raise BadGuardName("starts with an underscore", name)
    if not name.isupper():
        raise BadGuardName("contains non-upercase letters", name)


class ClassData:
    def __init__(self, name, parents=[], empty_class=False):
        self.name = name
        self.parents = parents
        self.empty_class = empty_class


def print_class(output, class_data, config):
    output.write("class " + class_data.name)
    if class_data.parents != []:
        prefix = ": "
        for parent in class_data.parents:
            output.write(prefix + "public " + parent)
            prefix = ", "
    if class_data.empty_class:
        output.write(" {};\n\n\n")
        return
    output.write(" {\npublic:\n\t\nprivate:\n\t\n};\n\n\n")


def open_namespaces(output, namespaces):
    for namespace in namespaces:
        output.write("namespace {} {{\n".format(namespace))
    if namespaces != []:
        output.write("\n\n")


def close_namespaces(output, namespaces):
    for namespace in reversed(namespaces):
        output.write("}} // namespace {}\n".format(namespace))
    if namespaces != []:
        output.write("\n")


def create_header(filename, config, namespaces=[], classes=[]):
    guardname = config["guard_prefix"] \
        + filename.split('/')[-1].upper().replace(".", "_")
    enforce_valid_guard_name(guardname)
    file = open(filename, "w")
    file.write("#ifndef {0}\n#define {0}\n\n\n".format(guardname))
    open_namespaces(file, namespaces)

    for c in classes:
        print_class(file, c, config)

    close_namespaces(file, namespaces)
    file.write("#endif // {}\n".format(guardname))
    file.close()


def create_implementation(filename, config, header=None, namespaces=[]):
    file = open(filename, "w")
    if header:
        file.write("#include \"{}\"\n".format(
            os.path.relpath(header, os.path.dirname(filename))))
    file.write("\n\n")
    open_namespaces(file, namespaces)
    close_namespaces(file, namespaces)
    file.close()


def get_filenames(filename):
    header = None
    implementation = None
    if filename.endswith(".hpp"):
        header = filename
    elif filename.endswith(".cpp"):
        implementation = filename
    else:
        header = filename + ".hpp"
        implementation = filename + ".cpp"
    return header, implementation


def get_namespaces(arg, config):
    tmp = []
    if "default_namespaces" in config:
        tmp = config["default_namespaces"]
    return tmp + [x for x in filter(None, arg.split("::"))]


def get_classes(strings):
    retval = []
    for s in strings:
        parts = s.split("<")
        classname = parts[0]
        base_classes = parts[1:]
        empty_class = False
        if classname.endswith("{}"):
            classname = classname[0:-2]
            empty_class = True
        retval.append(ClassData(classname, base_classes, empty_class))

    return retval


def main(args):
    config = read_config()
    if len(args) < 2:
        return 1
    header, implementation = get_filenames(args[1])

    namespaces = []
    if len(args) >= 3:
        namespaces = get_namespaces(args[2])

    classes = get_classes(args[3:])

    if header:
        create_header(header, config, namespaces, classes)
    if implementation:
        create_implementation(implementation, config, header, namespaces)


if __name__ == "__main__":
    main(sys.argv)
