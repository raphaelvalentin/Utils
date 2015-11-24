#!/usr/bin/env python
from setuptools import setup, find_packages
from distutils.extension import Extension
from __init__ import __version__

setup(
    name = "xytech-utils-collection",
    version = __version__,
    author = "Raphael Valentin",
    author_email = "raphael@xytech-consulting.com",
    description = ("suite of utility tools."),
    package_data = {'': ['*.xml']},
    packages = find_packages(),
    ext_modules = [Extension("fast/_nearest", ["fast/_nearest.c"])],
    zip_safe = True
)

