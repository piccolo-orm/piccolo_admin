#!/bin/bash
cd admin_ui && npm run build && cd ..
rm -rf ./build/*
rm -rf ./dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
