#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import os
import typing as t

from setuptools import find_packages, setup

from piccolo_admin.version import __VERSION__ as VERSION

directory = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(directory, "requirements/requirements.txt")) as f:
    contents = f.read()
    REQUIREMENTS = [i.strip() for i in contents.strip().split("\n")]


with open(os.path.join(directory, "README.md")) as f:
    LONG_DESCRIPTION = f.read()


EXTRAS = ["faker", "s3"]


def parse_requirement(req_path: str) -> t.List[str]:
    """
    Parses a requirement file - returning a list of contents.

    Example::

        parse_requirement('requirements.txt')       # requirements/requirements.txt
        parse_requirement('extras/playground.txt')  # requirements/extras/playground.txt

    :returns: A list of requirements specified in the file.

    """  # noqa: E501
    with open(os.path.join(directory, "requirements", req_path)) as f:
        contents = f.read()
        return [i.strip() for i in contents.strip().split("\n")]


def extras_require() -> t.Dict[str, t.List[str]]:
    """
    Parse requirements in requirements/extras directory
    """
    extra_requirements = {
        extra: parse_requirement(os.path.join("extras", f"{extra}.txt"))
        for extra in EXTRAS
    }

    extra_requirements["all"] = list(
        itertools.chain.from_iterable(extra_requirements.values())
    )

    return extra_requirements


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
    extras_require=extras_require(),
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database :: Front-Ends",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",  # noqa: E501
    ],
)
