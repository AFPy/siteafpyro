#!/bin/sh

cd docs
sphinx-build -b html -d _build/doctrees source _build/html
