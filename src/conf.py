#!/usr/bin/env python3


import os
import os.path
import configparser


__author__ = "Florian Weber (FJW)"
__license__ = "GPL-3.0+"
__version__ = "0.1"


config_file_name = "/cppassi.conf"
config_options = ["guard_prefix", "default_namespace"]

_default_config = {option: "" for option in config_options}


def _enumerate_parent_dirs():
    parents = os.getcwd().split('/')
    for i in range(len(parents), 0, -1):
        yield "/".join(parents[0:i])


def _get_config_file_path():
    for dir in _enumerate_parent_dirs():
        if os.path.isfile(dir + config_file_name):
            return dir + config_file_name
    return None


def read_config():
    config = _default_config.copy()
    config_file = _get_config_file_path()

    if config_file is None:
        return config

    configuration = configparser.ConfigParser()
    configuration.read(config_file)

    # why can't it just support not having sections?...
    module_configuration = configuration["config"]

    for option in config_options:
        if option in module_configuration:
            config[option] = module_configuration[option]

    return config
