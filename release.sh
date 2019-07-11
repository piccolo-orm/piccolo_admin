#!/bin/bash
cd ./admin_ui && npm run build && cd ..
rm ./dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
