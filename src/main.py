#!/usr/bin/env python3

"""
cppassi - C++-assistant

Ths program is a small helper for the creation of C++ files. Basically
what your IDE would do but without the IDE on the commandline.

This tool assumes a certain C++-style and has no intentions to enable
not following it. On the contrary, future versions may contain non-optional
checks on them (things like indentation with tabs or use of snake_case).
"""


import sys

import conf
import writer
import class_data

__author__ = "Florian Weber (FJW)"
__license__ = "GPL-3.0+"
__version__ = "0.1"


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
    def parse_namespace(s):
        return [n for n in filter(None, s.split("::"))]
    tmp = []
    if "default_namespaces" in config:
        tmp = parse_namespace(config["default_namespace"])
    return tmp + parse_namespace(arg)


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
        retval.append(class_data.ClassData(classname, base_classes,
                                           empty_class))

    return retval


def main(args):
    config = conf.read_config()
    if len(args) < 2:
        return 1
    header, implementation = get_filenames(args[1])

    namespaces = []
    if len(args) >= 3:
        namespaces = get_namespaces(args[2], config)

    classes = get_classes(args[3:])

    if header:
        writer.create_header(header, config, namespaces, classes)
    if implementation:
        writer.create_implementation(implementation, config,
                                     header, namespaces)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
