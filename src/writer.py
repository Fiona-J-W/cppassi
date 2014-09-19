#!/usr/bin/env python3


import os
import os.path
import name_validation


__author__ = "Florian Weber (FJW)"
__license__ = "GPL-3.0+"
__version__ = "0.1"


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
    name_validation.enforce_valid_guard_name(guardname)
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

