#!/bin/bash

set -e
set -x

export PYTHONPATH='..':$PYTHONPATH
python -m piccolo_admin.example &
