#!/usr/bin/env python3


import re

__author__ = "Florian Weber (FJW)"
__license__ = "GPL-3.0+"
__version__ = "0.1"


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
