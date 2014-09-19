#!/usr/bin/env python3


__author__ = "Florian Weber (FJW)"
__license__ = "GPL-3.0+"
__version__ = "0.1"


class ClassData:
    def __init__(self, name, parents=[], empty_class=False):
        self.name = name
        self.parents = parents
        self.empty_class = empty_class
