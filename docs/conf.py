# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Shepherd DevLog"
copyright = "2021-2025, Networked Embedded Systems Lab, TU Dresden / TU Darmstadt"
author = "Ingmar Splitt"
release = "2025"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx_sitemap",
    "sphinx_rtd_theme",
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["Thumbs.db", ".DS_Store"]

myst_enable_extensions = ["colon_fence"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ["_static"]

html_title = project
html_collapsible_definitions = True
html_copy_source = False

html_permalinks_icon = "<span>#</span>"

html_theme = "sphinx_rtd_theme"
html_theme_options = {}
github_url = "https://github.com/orgua/shepherd-v2-planning"

html_baseurl = "https://orgua.github.io/shepherd-v2-planning/"
html_extra_path = ["robots.txt"]
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

sitemap_url_scheme = "{link}"
