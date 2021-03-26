#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
	name = 'nagator',
	version = '0.1.0',
	author = "toxinu",
	author_email = "toxinu@gmail.com",
	description = "Nagios configuration viewer",
	long_description=open('README.rst').read() + '\n\n' +
					 open('HISTORY.rst').read(),
	license=open("LICENSE").read(),
	keywords = "nagios cli parser viewer",
	url = "https://github.com/toxinu/nagator",
	data_files=[('/etc', ['conf/nagator.cfg'])],
	packages = ['nagator', 'nagator.views'],
	scripts = ['scripts/nagator'],
	install_requires=['pynag', 'clint']
)
