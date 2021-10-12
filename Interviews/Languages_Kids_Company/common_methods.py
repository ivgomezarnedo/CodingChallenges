# Author: Iván Gómez
# Last modification: 01-09-2021
"""COMMON METHODS USED IN SEVERAL SCRIPTS

This file contains methods used in different scripts to avoid code redundancy.
"""

import configparser


def read_properties_file(file_path):
    config_file = configparser.ConfigParser()
    config_file.read(file_path)
    return config_file
