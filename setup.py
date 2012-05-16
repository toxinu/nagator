#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
from setuptools import setup

setup(
    name = 'nagator',
    version = '0.0.1',
    author = "Socketubs",
    author_email = "geoffrey@lehee.name",
    description = "Nagios configuration viewer",
    license = "No Licence",
    keywords = "nagios cli parser viewer",
    url = "https://github.com/Socketubs/Nagator",
	data_files=[('/etc', ['conf/nagator.cfg'])],
    packages = ['nagator'],
    scripts = ['bin/nagator'],
    install_requires=['pynag', 'clint']
)
