#!/bin/bash

SOURCES="piccolo_admin tests e2e"

isort $SOURCES
black $SOURCES
flake8 $SOURCES
mypy $SOURCES
