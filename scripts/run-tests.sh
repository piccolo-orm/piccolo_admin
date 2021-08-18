#!/bin/bash
# To run all in a folder tests/
# To run all in a file tests/test_foo.py
# To run all in a class tests/test_foo.py::TestFoo
# To run a single test tests/test_foo.py::TestFoo::test_foo

export PICCOLO_CONF="tests.piccolo_conf"
cd admin_ui
npm install
npm run build
rm -rf node_modules
cd ..
python -m pytest --cov=piccolo_admin --cov-report xml --cov-report html --cov-fail-under 85 -s $@
cd piccolo_admin
rm -rf dist