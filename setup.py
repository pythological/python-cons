#!/usr/bin/env python
from os.path import exists
from setuptools import find_packages, setup

setup(
    name="cons",
    version="0.1.3",
    install_requires=[
        'toolz',
        'unification'
    ],
    packages=find_packages(exclude=['tests']),
    tests_require=[
        'pytest'
    ],
    author="Brandon T. Willard",
    author_email="brandonwillard+cons@gmail.com",
    description="""An implementation of Lisp/Scheme-like cons in Python.""",
    long_description=open('README.md').read() if exists("README.md") else "",
    long_description_content_type='text/markdown',
    license="LGPL-3",
    url="https://github.com/brandonwillard/python-cons",
    platforms=['any'],
    python_requires='>=3.5',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: DFSG approved",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
    ]
)
