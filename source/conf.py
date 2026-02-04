# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os

# Configure py_rodo backend before importing it
import py_rodo.config

backend = os.environ.get("PY_RODO_TEST_BACKEND", "pydantic")
py_rodo.config.set_backend(backend)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "py-rabbit-opensuse-org"
copyright = "Dan Čermák"
author = "Dan Čermák"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

nitpicky = True
nitpick_ignore = [
    ("py:class", "py_rodo.backends.pydantic.ObsMessageBusPayloadBase"),
    ("py:class", "py_rodo.backend.ObsMessageBusPayloadBase"),
]
