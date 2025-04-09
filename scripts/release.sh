#!/bin/bash
cd admin_ui && npm i && npm run build-only && cd ..
rm -rf ./build/*
rm -rf ./dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
