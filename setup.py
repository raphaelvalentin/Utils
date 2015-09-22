#!/usr/bin/env python
from setuptools import setup, find_packages
from distutils.extension import Extension

setup(
    name = "xytech-utils-collection",
    version = "0.0.1",
    author = "Raphael Valentin",
    author_email = "raphael@xytech-consulting.com",
    description = ("suite of utility tools."),
    package_data = {'': ['*.xml']},
    packages = find_packages(),
    ext_modules = [Extension("fast/_nearest", ["fast/_nearest.c"])],
    zip_safe = True
)

