#!/bin/bash
# Run end-to-end tests

python -m pytest e2e -s --video=on $@
