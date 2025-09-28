"""Simple-SSG.

A lightweight, dependency-minimal static site generator that converts Markdown
content to HTML. It's designed to be simple, understandable, and customizable
while providing all the essential features needed for modern static websites.

This package provides both a command-line interface (CLI) for generating
sites and a programmatic API for integration into other Python projects. The
primary entry point for the API is the `build_site` function.

For more information on how to use Simple-SSG, refer to the project's
documentation.

Attributes:
    __version__ (str): The current version of the package.
    __author__ (str): The author of the package.
"""

__version__ = "0.1.0"
__author__ = "Brady Clarke"

from simple_ssg.builder import build_site  # noqa
