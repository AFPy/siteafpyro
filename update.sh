#!/bin/sh
cd /home/hg/repos/main/siteafpyro
hg up
cd docs
../bin/sphinx-build -b html -d _build/doctrees source _build/html
cd ..
bin/supervisorctl restart all
