# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import datetime
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

autoclass_content = "both"
autodoc_typehints = "signature"
autodoc_typehints_format = "short"

# -- Project information -----------------------------------------------------

project = "Piccolo Admin"
year = datetime.datetime.now().strftime("%Y")
author = "Daniel Townsend"
copyright = f"{year}, {author}"


import piccolo_admin  # noqa

version = ".".join(piccolo_admin.version.__VERSION__.split(".")[:3])
release = piccolo_admin.version.__VERSION__

# -- General configuration ---------------------------------------------------

master_doc = "index"

extensions = ["sphinx.ext.autodoc"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# -- Options for HTML output -------------------------------------------------

html_theme = "piccolo_theme"

# -- Intersphinx -------------------------------------------------------------

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
extensions += ["sphinx.ext.intersphinx"]
