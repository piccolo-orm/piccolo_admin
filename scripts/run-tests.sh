#!/bin/bash
# To run all in a folder tests/
# To run all in a file tests/test_foo.py
# To run all in a class tests/test_foo.py::TestFoo
# To run a single test tests/test_foo.py::TestFoo::test_foo

export PICCOLO_CONF="tests.piccolo_conf"
mkdir -p piccolo_admin/dist/css
mkdir -p piccolo_admin/dist/js
touch piccolo_admin/dist/index.html

python -m pytest --ignore=e2e --cov=piccolo_admin --cov-report xml --cov-report html --cov-fail-under 85 -s $@
