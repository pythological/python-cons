#!/usr/bin/env python
from os.path import exists

from setuptools import find_packages, setup

import versioneer

setup(
    name="cons",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=["logical-unification>=0.4.0"],
    packages=find_packages(exclude=["tests"]),
    tests_require=["pytest"],
    author="Brandon T. Willard",
    author_email="brandonwillard+cons@gmail.com",
    description="""An implementation of Lisp/Scheme-like cons in Python.""",
    long_description=open("README.md").read() if exists("README.md") else "",
    long_description_content_type="text/markdown",
    license="LGPL-3",
    url="https://github.com/pythological/python-cons",
    platforms=["any"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: DFSG approved",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",  # noqa: E501
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
    ],
)
