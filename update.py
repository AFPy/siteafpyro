#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sys
import os

pwd = os.getcwd()
subprocess.call('hg up', shell=True)
subprocess.call('bin/buildout', shell=True)
os.chdir('docs')
subprocess.call('../bin/sphinx-build -b html -d _build/doctrees source _build/html', shell=True)
os.chdir(pwd)
if '-s' in sys.argv:
    subprocess.call('bin/paster serve --reload development.ini', shell=True)

