#!/bin/bash
# Run end-to-end tests

extraArgs=$@

pytest --ignore=tests -s $extraArgs
