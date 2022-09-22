#!/bin/bash
# Run end-to-end tests

export PICCOLO_CONF="e2e.piccolo_conf"

python -m pytest e2e 