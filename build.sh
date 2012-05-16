#!/bin/bash

version=0.0.1

python setup.py sdist
cd dist
sudo pip-2.7 install nagator-0.0.1.tar.gz
