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

extensions = []

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

# -- Options for HTML output -------------------------------------------------

html_theme = "piccolo_theme"
html_short_title = "Piccolo Admin"
html_theme_options = {
    "source_url": "https://github.com/piccolo-orm/piccolo_admin/"
}

# -- Autodoc -----------------------------------------------------------------

extensions += ["sphinx.ext.autodoc"]
autodoc_typehints = "signature"
autodoc_typehints_format = "short"
autoclass_content = "both"
autodoc_preserve_defaults = True

# -- Viewcode -------------------------------------------------------------

extensions += ["sphinx.ext.viewcode"]

# -- Intersphinx -------------------------------------------------------------

extensions += ["sphinx.ext.intersphinx"]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "piccolo": ("https://piccolo-orm.readthedocs.io/en/latest/", None),
    "piccolo_api": ("https://piccolo-api.readthedocs.io/en/latest/", None),
}
