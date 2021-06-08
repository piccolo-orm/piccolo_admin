#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

from piccolo_admin.version import __VERSION__ as VERSION


directory = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(directory, "requirements.txt")) as f:
    contents = f.read()
    REQUIREMENTS = [i.strip() for i in contents.strip().split("\n")]


with open(os.path.join(directory, "README.md")) as f:
    LONG_DESCRIPTION = f.read()


setup(
    name="piccolo_admin",
    version=VERSION,
    description="A simple and powerful admin for Piccolo models, using ASGI.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Daniel Townsend",
    author_email="dan@dantownsend.co.uk",
    python_requires=">=3.7.0",
    url="https://github.com/piccolo-orm/piccolo_admin",
    packages=find_packages(exclude=("tests",)),
    install_requires=REQUIREMENTS,
    extras_require={"faker": ["faker==6.5.0"]},
    license="MIT",
    include_package_data=True,
    entry_points={
        "console_scripts": ["admin_demo = piccolo_admin.example:main"],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database",
    ],
)
