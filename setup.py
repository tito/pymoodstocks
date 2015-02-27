#!/usr/bin/env python

from os.path import dirname, join

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

curdir = dirname(__file__)
packages = [
    "pymoodstocks",
]

setup(
    name="pymoodstocks",
    version="0.1",
    description="Kivy/Python wrapper on the Moodstocks iOS and Android SDK",
    long_description=open(join(curdir, "README.md")).read(),
    author="Mathieu Virbel",
    author_email="mat@meltingrocks.com",
    url="https://github.com/tito/pymoodstocks",
    packages=packages,
    package_data={"": ["LICENSE", "README.rst"]},
    package_dir={"pymoodstocks": "pymoodstocks"},
    include_package_data=True,
    license=open(join(curdir, "LICENSE")).read(),
    zip_safe=False,
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",

    ),
)
