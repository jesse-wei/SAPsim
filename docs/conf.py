# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

#########################################
# THIS IS IMPORTANT!
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
#########################################

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "SAPsim"
copyright = "2023, Jesse Wei"
author = "Jesse Wei"
release = ""

# Parse release version from setup.py to avoid maintaining two variables
with open("../setup.py", "r") as f:
    for line in f:
        if line.strip().startswith("version"):
            release = line.split('"')[1]
            break

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    # For parsing Markdown
    "m2r2",
    "sphinx.ext.autosectionlabel",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
source_suffix = [".rst", ".md", ".markdown"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Good themes: sphinx_rtd_theme (has ads), python_docs_theme, alabaster
html_theme = "sphinx_rtd_theme"

# Source: https://stackoverflow.com/questions/59215996/how-to-add-a-logo-to-my-readthedocs-logo-rendering-at-0px-wide
html_static_path = ["_static"]
html_favicon = "sap.ico"
html_logo = "_static/sap.jpg"

# Prevents __init__ from being ignored
# Source: https://stackoverflow.com/questions/5599254/how-to-use-sphinxs-autodoc-to-document-a-classs-init-self-method
# def skip(app, what, name, obj, would_skip, options):
#     if name == "__init__":
#         return False
#     return would_skip


# def setup(app):
#     app.connect("autodoc-skip-member", skip)
