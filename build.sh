#!/bin/bash

version=0.0.1

python setup.py sdist
sudo pip-2.7 uninstall nagator
sudo pip-2.7 install dist/nagator-$version.tar.gz
