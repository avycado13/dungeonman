# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
from pathlib import Path

# Import the package directly from the src layout, even without an editable install.
sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))

project = 'dungeonman'
copyright = '2026, avycado13'
author = 'avycado13'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

# Parse Google-style Args, Returns, and Attributes sections in docstrings.
napoleon_google_docstring = True
napoleon_numpy_docstring = False
# Avoid duplicate entries for dataclass fields documented in Attributes sections.
napoleon_use_ivar = True

templates_path = ['_templates']
exclude_patterns = ['_build', '.venv', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
