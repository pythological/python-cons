#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="cons",
    version="0.0.1",
    install_requires=[
        'toolz',
        'multipledispatch',
        'unification'
    ],
    packages=find_packages(exclude=['tests']),
    tests_require=[
        'pytest'
    ],
    author="Brandon T. Willard",
    author_email="brandonwillard+cons@gmail.com",
    long_description="""An implementation of Lisp/Scheme-like cons in Python.""",
    license="LGPL-3",
    url="https://github.com/brandonwillard/python-cons",
    platforms=['any'],
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: DFSG approved",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
    ]
)
