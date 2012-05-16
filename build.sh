#!/bin/bash

version=0.0.1

cd /root
tar cvpzf nagator-$version.tar.gz nagator-$version
pip install nagator-$version.tar.gz
cd /root/nagator-$version
