#!/bin/bash

SOURCES="piccolo_admin tests"

isort $SOURCES
black $SOURCES
flake8 $SOURCES
# mypy $SOURCES
