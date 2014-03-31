#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.md').read()

setup(
    name='quickD3map',
    version='0.1.4',
    description='Generate quick d3 maps from location data in pandas',
    long_description=readme + '\n\n' + history,
    author='zach powers',
    author_email='zcharlop@rockefeller.edu',
    url='https://github.com/zachcp/quickD3map',
    packages=[
        'quickD3map',
    ],
    package_dir={'quickD3map': 'quickD3map'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='quickD3map',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)