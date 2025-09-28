"""Command-line interface for Simple-SSG.

This module provides the command-line interface (CLI) for Simple-SSG. It allows
users to build their static site, serve it locally for development, and
initialize a new project structure from the command line.

The CLI is built using Python's `argparse` module and provides the following
commands:
- `build`: Generates the static site from content files.
- `serve`: Starts a local development server to preview the site.
- `init`: Creates a new project with a default directory structure and files.

This module maps command-line arguments to the core functionalities provided
by the `simple_ssg.builder` and `simple_ssg.enhancers` modules.
"""

import os
import sys
import argparse
import json
from typing import Any
import yaml
from simple_ssg.builder import build_site
from simple_ssg.enhancers.server import serve
from simple_ssg import __version__


def main() -> None:
    """Parses command-line arguments and executes the corresponding command.

    This function sets up the main parser and subparsers for the `build`,
    `serve`, and `init` commands. It dispatches to the appropriate `run_*`
    function based on the user's input.
    """
    parser = argparse.ArgumentParser(
        description="Simple-SSG - A Minimalist Static Site Generator",
        epilog="For more information, visit "
        "https://github.com/bradyclarke/simple-ssg",
    )

    # Add version argument
    parser.add_argument(
        "--version", action="version", version=f"Simple-SSG {__version__}"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Build command
    build_parser = subparsers.add_parser("build", help="Build the static site")
    build_parser.add_argument(
        "--config", "-c", help="Path to config file (YAML or JSON)"
    )
    build_parser.add_argument("--content-dir", help="Content directory")
    build_parser.add_argument("--output-dir", help="Output directory")
    build_parser.add_argument("--template", help="Template file")
    build_parser.add_argument("--base-url", help="Base URL for sitemap and links")
    build_parser.add_argument(
        "--no-minify", action="store_true", help="Disable HTML minification"
    )
    build_parser.add_argument(
        "--no-sitemap", action="store_true", help="Disable sitemap generation"
    )
    build_parser.add_argument(
        "--no-robots", action="store_true", help="Disable robots.txt generation"
    )

    # Serve command
    serve_parser = subparsers.add_parser(
        "serve", help="Start a local development server"
    )
    serve_parser.add_argument(
        "directory",
        nargs="?",
        default="build",
        help="Directory to serve (default: build)",
    )
    serve_parser.add_argument(
        "--port", "-p", type=int, default=8000, help="Port to serve on (default: 8000)"
    )
    serve_parser.add_argument(
        "--no-browser", action="store_true", help="Do not open a browser automatically"
    )

    # Init command
    init_parser = subparsers.add_parser(
        "init", help="Initialize a new Simple-SSG project"
    )
    init_parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to initialize (default: current directory)",
    )
    init_parser.add_argument(
        "--template",
        choices=["basic", "blog", "portfolio"],
        default="basic",
        help="Template to use (default: basic)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Execute the appropriate command
    if args.command == "build":
        run_build(args)
    elif args.command == "serve":
        run_serve(args)
    elif args.command == "init":
        run_init(args)
    else:
        parser.print_help()
        sys.exit(1)


def run_build(args: argparse.Namespace) -> None:
    """Runs the site build process based on command-line arguments.

    This function loads the configuration, overrides it with any provided
    command-line arguments, and then calls the main `build_site` function.

    Args:
        args: The parsed command-line arguments from argparse.
    """
    config_dict: dict[str, Any] = {}

    # Load config from file if provided
    if args.config:
        if not os.path.exists(args.config):
            print(f"Error: Config file {args.config} not found.")
            sys.exit(1)

        try:
            with open(args.config, "r", encoding="utf-8") as f:
                if args.config.endswith((".yaml", ".yml")):
                    config_dict = yaml.safe_load(f)
                elif args.config.endswith(".json"):
                    config_dict = json.load(f)
                else:
                    print(f"Error: Unsupported config file format: {args.config}")
                    sys.exit(1)
        except Exception as e:
            print(f"Error loading config file: {str(e)}")
            sys.exit(1)

    # Override with command-line arguments
    if args.content_dir:
        config_dict["content_dir"] = args.content_dir

    if args.output_dir:
        config_dict["output_dir"] = args.output_dir

    if args.template:
        config_dict["template_path"] = args.template

    if args.base_url:
        config_dict["base_url"] = args.base_url

    if args.no_minify:
        config_dict["minify"] = False

    if args.no_sitemap:
        config_dict["generate_sitemap"] = False

    if args.no_robots:
        config_dict["generate_robots"] = False

    # Build the site
    stats = build_site(config_dict=config_dict)

    # Check for errors
    if stats.get("errors", 0) > 0:
        sys.exit(1)


def run_serve(args: argparse.Namespace) -> None:
    """Starts a local development server.

    This function uses the `serve` utility to start a simple HTTP server
    for the specified directory, allowing for local previewing of the site.

    Args:
        args: The parsed command-line arguments from argparse.
    """
    try:
        serve(
            directory=args.directory,
            port=args.port,
            open_browser=not args.no_browser,
        )
    except KeyboardInterrupt:
        print("\nServer stopped.")


def run_init(args: argparse.Namespace) -> None:
    """Initializes a new Simple-SSG project structure.

    This function creates a directory structure with example content, templates,
    and a configuration file to help users get started quickly.

    Args:
        args: The parsed command-line arguments from argparse.
    """
    try:
        directory = args.directory
        template = args.template

        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create template directories
        dirs_to_create = [
            os.path.join(directory, "content"),
            os.path.join(directory, "css"),
            os.path.join(directory, "images"),
            os.path.join(directory, "js"),
        ]

        for dir_path in dirs_to_create:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"Created directory: {dir_path}")

        # Create template.html
        template_path = os.path.join(directory, "template.html")
        if not os.path.exists(template_path):
            with open(template_path, "w", encoding="utf-8") as f:
                f.write(get_template_html(template))
            print(f"Created template: {template_path}")

        # Create index.html
        index_path = os.path.join(directory, "index.html")
        if not os.path.exists(index_path):
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(get_index_html())
            print(f"Created index: {index_path}")

        # Create example content
        content_path = os.path.join(directory, "content", "index.md")
        if not os.path.exists(content_path):
            with open(content_path, "w", encoding="utf-8") as f:
                f.write(get_example_content(template))
            print(f"Created example content: {content_path}")

        # Create about.md
        about_path = os.path.join(directory, "content", "about.md")
        if not os.path.exists(about_path):
            with open(about_path, "w", encoding="utf-8") as f:
                f.write(get_about_content(template))
            print(f"Created about page: {about_path}")

        # Create 404.md
        not_found_path = os.path.join(directory, "content", "404.md")
        if not os.path.exists(not_found_path):
            with open(not_found_path, "w", encoding="utf-8") as f:
                f.write(get_404_content())
            print(f"Created 404 page: {not_found_path}")

        # Create CSS
        css_path = os.path.join(directory, "css", "styles.css")
        if not os.path.exists(css_path):
            with open(css_path, "w", encoding="utf-8") as f:
                f.write(get_css_content(template))
            print(f"Created stylesheet: {css_path}")

        # Create config.yaml
        config_path = os.path.join(directory, "config.yaml")
        if not os.path.exists(config_path):
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(get_config_yaml(template))
            print(f"Created config: {config_path}")

        print("\nSimple-SSG project initialized successfully!")
        print("\nTo build your site:")
        print(f"  cd {directory}")
        print("  simple-ssg build --config config.yaml")
        print("\nTo preview your site:")
        print("  simple-ssg serve")

    except Exception as e:
        print(f"Error initializing project: {str(e)}")
        sys.exit(1)


def get_template_html(template_type: str) -> str:
    """Generates the default HTML template content.

    Args:
        template_type: The type of project template (e.g., 'basic').
                       Currently, this is not used to vary the output.

    Returns:
        A string containing the HTML for the main site template.
    """
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Simple-SSG Site</title>
    <meta name="description" content="A site built with Simple-SSG">
    
    <!-- Open Graph / Social Media -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="My Simple-SSG Site">
    <meta property="og:description" content="A site built with Simple-SSG">
    <meta property="og:url" content="https://example.com">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="My Simple-SSG Site">
    <meta name="twitter:description" content="A site built with Simple-SSG">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://example.com">
    
    <link rel="stylesheet" href="css/styles.css">
    <link rel="icon" href="favicon.ico">
</head>
<body>
    <header>
        <div class="container">
            <nav>
                <a href="index.html" class="logo">Simple-SSG</a>
                <button class="menu-toggle" aria-label="Toggle menu">☰</button>
                <ul class="nav-links">
                    <li><a href="index.html">Home</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <div id="content-container">
                <div class="loading">Loading content...</div>
            </div>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2025 Simple-SSG. Built with <a href="https://github.com/bradyclarke/simple-ssg">Simple-SSG</a>.</p>
        </div>
    </footer>

    <!-- JavaScript for mobile menu -->
    <script>
        document.querySelector('.menu-toggle').addEventListener('click', function() {
            document.querySelector('.nav-links').classList.toggle('active');
        });
    </script>
</body>
</html>"""


def get_index_html() -> str:
    """Generates content for a root-level index.html redirect file.

    This is useful for servers that don't automatically serve `index.html`
    from a subdirectory.

    Returns:
        A string containing a simple HTML page with a meta-refresh redirect.
    """
    return """<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="0;url=index.html">
  </head>
  <body>
    Redirecting...
  </body>
</html>"""


def get_example_content(template_type: str) -> str:
    """Generates example Markdown content for the main page.

    Args:
        template_type: The type of project template ('basic', 'blog',
                       'portfolio').

    Returns:
        A string containing example Markdown content.
    """
    if template_type == "blog":
        return """# Welcome to My Blog

This is a blog built with Simple-SSG, a minimalist static site generator.

## Latest Posts

### Getting Started with Simple-SSG {.post}

Welcome to my new blog! In this post, I'll share my experience setting up Simple-SSG and why I chose it for my website.

[Read more](post1.html)

### Why Markdown is Awesome {.post}

Markdown makes writing content so much easier and more enjoyable. Here's why I love using it for my blog.

[Read more](post2.html)"""
    elif template_type == "portfolio":
        return """# My Portfolio

Welcome to my portfolio site. I'm a designer and developer creating beautiful and functional websites.

## Featured Projects

### Project One {.project}

A responsive e-commerce website built with modern technologies.

[View Project](project1.html)

### Project Two {.project}

Brand identity and website design for a local business.

[View Project](project2.html)"""
    else:  # basic
        return """# Welcome to Simple-SSG

This is a site built with Simple-SSG, a minimalist static site generator.

## Features

- **Simple** - Easy to set up and use
- **Fast** - Generates static HTML with no client-side processing
- **Flexible** - Customize to your needs
- **Markdown-Based** - Write content in Markdown

## Getting Started

Edit the files in the `content` directory to add your own content. The site will be generated in the `build` directory.

[Learn more about Simple-SSG](about.html)"""


def get_about_content(template_type: str) -> str:
    """Generates the content for the 'about' page.

    Args:
        template_type: The type of project template. This argument is not
                       currently used to vary the content.

    Returns:
        A string containing Markdown content for the about page.
    """
    return """# About

This site was built with Simple-SSG, a minimalist static site generator.

## How It Works

Simple-SSG converts Markdown content to HTML and injects it into a template. This makes it easy to maintain a consistent look and feel across your site.

## Why Simple-SSG?

- **Minimal Dependencies** - Just Python and a few libraries
- **Easy to Understand** - Simple, clean code
- **Fast Build Times** - Generates static HTML quickly
- **SEO Friendly** - Includes sitemap, meta tags, and more

## Getting Started

Check out the [Simple-SSG GitHub repository](https://github.com/bradyclarke/simple-ssg) for more information."""


def get_404_content() -> str:
    """Generates the content for the '404 not found' page.

    Returns:
        A string containing Markdown content for the 404 page.
    """
    return """# Page Not Found

Sorry, the page you were looking for couldn't be found.

## What Might Have Happened?

- The page might have been moved or renamed
- There might be a typo in the URL
- The page might no longer exist

## What to Do Next

[Return to Homepage](index.html){.button}

If you continue to experience issues, please [contact us](contact.html)."""


def get_css_content(template_type: str) -> str:
    """Generates the default CSS content for the project.

    Args:
        template_type: The type of project template. This argument is not
                       currently used to vary the content.

    Returns:
        A string containing the default CSS styles.
    """
    return """/* Base styles */
:root {
    --primary-color: #3498db;
    --secondary-color: #2c3e50;
    --text-color: #333;
    --light-color: #f5f5f5;
    --border-color: #ddd;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: #fff;
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    margin-bottom: 1rem;
    line-height: 1.3;
    color: var(--secondary-color);
}

h1 {
    font-size: 2.5rem;
}

h2 {
    font-size: 2rem;
}

h3 {
    font-size: 1.5rem;
}

p {
    margin-bottom: 1.5rem;
}

a {
    color: var(--primary-color);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

ul, ol {
    margin-bottom: 1.5rem;
    padding-left: 1.5rem;
}

blockquote {
    border-left: 4px solid var(--primary-color);
    padding-left: 1rem;
    margin-left: 0;
    margin-bottom: 1.5rem;
    font-style: italic;
}

/* Header */
header {
    background-color: var(--secondary-color);
    padding: 1rem 0;
    color: white;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
}

.nav-links {
    display: flex;
    list-style: none;
}

.nav-links li {
    margin-left: 1.5rem;
}

.nav-links a {
    color: white;
}

.menu-toggle {
    display: none;
    background: none;
    border: none;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
}

/* Main content */
main {
    padding: 2rem 0;
}

section {
    margin-bottom: 2rem;
}

.hero {
    padding: 2rem 0;
    text-align: center;
}

/* Buttons */
.button {
    display: inline-block;
    padding: 0.5rem 1rem;
    background-color: var(--primary-color);
    color: white;
    border-radius: 4px;
    text-decoration: none;
}

.button:hover {
    background-color: #2980b9;
    text-decoration: none;
}

/* Footer */
footer {
    background-color: var(--light-color);
    padding: 1rem 0;
    text-align: center;
    border-top: 1px solid var(--border-color);
}

/* Responsive */
@media (max-width: 768px) {
    .menu-toggle {
        display: block;
    }
    
    .nav-links {
        display: none;
        flex-direction: column;
        position: absolute;
        top: 60px;
        left: 0;
        right: 0;
        background-color: var(--secondary-color);
        padding: 1rem;
    }
    
    .nav-links.active {
        display: flex;
    }
    
    .nav-links li {
        margin: 0.5rem 0;
    }
}

/* Images */
img {
    max-width: 100%;
    height: auto;
}

/* Forms */
form {
    margin-bottom: 2rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
}

input,
textarea,
select {
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    background-color: var(--primary-color);
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: var(--secondary-color);
}"""


def get_config_yaml(template_type: str) -> str:
    """Generates the default YAML configuration content.

    Args:
        template_type: The type of project template. This argument is not
                       currently used to vary the content.

    Returns:
        A string containing the default `config.yaml` content.
    """
    return """# Simple-SSG Configuration

# Basic paths
content_dir: content
template_path: template.html
output_dir: build
static_dirs:
  - css
  - images
  - js
index_path: index.html

# Build options
clean_output: true
minify: true
wrap_sections: true

# Section wrapping
h1_section_class: hero
h2_section_class: section

# SEO settings
base_url: https://example.com
generate_sitemap: true
generate_robots: true
generate_htaccess: true

# Image paths
image_path_replacements:
  ../images/: images/

# Markdown extensions
markdown_extensions:
  - extra
  - tables
  - smarty
"""


if __name__ == "__main__":
    main()
