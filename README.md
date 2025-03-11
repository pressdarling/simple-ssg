# Simple-SSG - A Minimalist Static Site Generator

Simple-SSG is a lightweight, dependency-minimal static site generator that converts Markdown content to HTML. It's designed to be simple, understandable, and customizable while providing all the essential features needed for modern static websites.

## Overview

Simple-SSG is a lightweight static site generator focusing on simplicity and efficiency. It provides a clean, organized approach to building static websites with minimal dependencies.

## Features

- **Markdown-based content** with custom class annotations
- **Template system** for consistent site design
- **Automatic section wrapping** based on heading structure
- **SEO enhancements** including sitemap and meta tag generation
- **Development server** for local preview
- **HTML minification** for optimized output
- **Zero JavaScript required** in the generated site (unless you add it)
- **Modern Python tooling** including type hints, ruff, and pytest
- **Customizable through configuration files** (YAML or JSON)
- **Simple CLI** for easy usage

## Package Structure

```
simple-ssg/
├── pyproject.toml           # Package metadata and config
├── setup.py                 # Installation script
├── LICENSE                  # MIT license
├── .github/                 # GitHub configuration
│   └── workflows/           # GitHub Actions workflows
│       ├── tests.yml        # Automated testing
│       └── release.yml      # Publishing workflow
├── docs/                    # Package documentation
│   ├── getting-started.md   # Getting started guide
│   ├── integration-guide.md # Integration documentation
│   └── structure.md         # Package structure explanation
├── examples/                # Example projects
│   └── basic-website/       # Minimal example site
│       ├── config.yaml      # Configuration file
│       ├── content/         # Content directory
│       ├── css/             # Stylesheets
│       ├── images/          # Images directory
│       ├── template.html    # HTML template
│       └── index.html       # Entry point
├── simple_ssg/               # Package source code
│   ├── __init__.py          # Package initialization
│   ├── builder.py           # Core build functionality
│   ├── cli.py               # Command-line interface
│   ├── config.py            # Configuration handling
│   ├── converters/          # Content converters
│   │   ├── __init__.py
│   │   ├── markdown.py      # Markdown converter
│   │   └── html.py          # HTML processor
│   ├── enhancers/           # Optional enhancements
│   │   ├── __init__.py
│   │   ├── minifier.py      # HTML minification
│   │   ├── seo.py           # SEO enhancements
│   │   └── server.py        # Development server
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── fs.py            # Filesystem operations
│       └── templates.py     # Template handling
└── tests/                   # Test suite
    ├── fixtures/            # Test data
    ├── test_builder.py      # Builder tests
    ├── test_config.py       # Configuration tests
    └── test_converters.py   # Converter tests
```

## Installation

### With pip

```bash
pip install simple-ssg
```

### With uv (Recommended)

```bash
uv pip install simple-ssg
```

### From source

```bash
git clone https://github.com/bradyclarke/simple-ssg.git
cd simple-ssg
uv pip install -e .
```

### Dev Environment

```bash
# Install development dependencies
uv pip install -e ".[dev]"
# or with pip
pip install -e ".[dev]"
```

## Quick Start

### Create a new project

```bash
# Initialize a new project
mkdir my-website
cd my-website

# Create a basic structure
simple-ssg init
```

### Add content

Create a Markdown file in the `content` directory:

```markdown
# My First Page

This is a paragraph with **bold** and *italic* text.

## Section Title

- List item 1
- List item 2

[Link text](another-page.html)
```

### Build the site

```bash
simple-ssg build
```

### Preview the site

```bash
simple-ssg serve
```

## Project Structure

A basic Simple-SSG project looks like this:

```
my-website/
├── config.yaml           # Configuration file
├── content/              # Markdown content files
│   ├── index.md          # Homepage content
│   ├── about.md          # About page content
│   └── 404.md            # 404 page content
├── css/                  # CSS stylesheets
│   └── styles.css        # Main stylesheet
├── images/               # Image files
├── js/                   # JavaScript files (optional)
└── template.html         # HTML template
```

## Configuration

Simple-SSG can be configured through a YAML file (default: `config.yaml`):

```yaml
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
site_name: "My Website"
site_description: "A website built with Simple-SSG"
base_url: https://example.com
generate_sitemap: true
generate_robots: true

# Image paths
image_path_replacements:
  ../images/: images/

# Markdown extensions
markdown_extensions:
  - extra
  - tables
  - smarty
```

## Template System

Simple-SSG uses a simple template system with placeholders:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{title}} - {{site_name}}</title>
    <meta name="description" content="{{description}}" />
    <link rel="stylesheet" href="/css/styles.css" />
  </head>
  <body>
    <header>
      <nav>
        <a href="/">Home</a>
        <a href="/about.html">About</a>
        <a href="/contact.html">Contact</a>
      </nav>
    </header>

    <main>{{content}}</main>

    <footer>
      <p>&copy; 2025 - {{site_name}}</p>
    </footer>
  </body>
</html>
```

### Available Placeholders

- `{{content}}` - The converted content from Markdown
- `{{title}}` - The page title (from first h1 heading or front matter)
- `{{description}}` - The page description (from front matter)
- `{{site_name}}` - The site name from config
- `{{site_description}}` - The site description from config
- `{{base_url}}` - The base URL from config
- Any custom variable defined in front matter

## Writing Content

### Front Matter

You can add YAML front matter to the beginning of your Markdown files:

```markdown
---
title: My Custom Title
description: This is a custom page description for SEO
custom_variable: This can be used in the template
---

# Page Content

Regular markdown content goes here.
```

### Class Annotations

Add CSS classes to elements using the `{.classname}` syntax:

```markdown
# Page Title {.custom-title}

This is a paragraph with a [special link](page.html){.special-link}.

## Section Title {.important}

> A blockquote with a class {.note}
```

### Basic Markdown

All standard Markdown syntax is supported:

```markdown
# Heading 1
## Heading 2
### Heading 3

This is a **bold** and *italic* text.

- List item 1
- List item 2
  - Nested item
  
1. Numbered item 1
2. Numbered item 2

[Link text](url)

![Image alt text](image.jpg)

```code block```

| Table | Header |
|-------|--------|
| Cell  | Cell   |
```

## Command Line Interface

### Initialize a new project

```bash
simple-ssg init [directory] [--template basic|blog|portfolio]
```

### Build the site

```bash
simple-ssg build [--config config.yaml] [--content-dir content] [--output-dir build]
```

### Start a development server

```bash
simple-ssg serve [--port 8000] [--no-browser]
```

### Get help

```bash
simple-ssg --help
simple-ssg build --help
```

## API Usage

You can use Simple-SSG programmatically in your Python code:

```python
from simple_ssg import build_site

# Using a config file
build_site(config_file="config.yaml")

# Or using a config dictionary
config = {
    "content_dir": "content",
    "template_path": "template.html",
    "output_dir": "build",
    "static_dirs": ["css", "images", "js"],
    "minify": True
}
build_site(config_dict=config)

# With custom enhancers
from simple_ssg.enhancers import Minifier, SeoEnhancer
build_site(
    config_file="config.yaml",
    enhancers=[Minifier(), SeoEnhancer()]
)
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/bradyclarke/simple-ssg.git
cd simple-ssg

# Install development dependencies
uv pip install -e ".[dev]"
```

### Code Quality Tools

Simple-SSG uses modern Python tools for code quality:

```bash
# Run linter
ruff check simple_ssg

# Run type checking
mypy simple_ssg

# Run tests
pytest
```

### GitHub Actions

The repository includes GitHub Actions workflows for:

- Running tests on every push
- Code quality checks
- Automated publishing to PyPI on new releases

## Extending Simple-SSG

### Custom Converters

You can create custom content converters by extending the base Converter class:

```python
from simple_ssg.converters import Converter

class MyCustomConverter(Converter):
    def convert(self, content, **kwargs):
        # Process content
        return processed_content
```

### Custom Enhancers

Create custom enhancers to add functionality to the build process:

```python
from simple_ssg.enhancers import Enhancer

class MyCustomEnhancer(Enhancer):
    def enhance(self, site, **kwargs):
        # Enhance the site object
        return enhanced_site
```

## Integration with Other Projects

Simple-SSG can be used as a component in larger projects:

- As a dependency in a web application
- Integrated into a content management system
- Part of a continuous integration pipeline
- Embedded in a developer tool

See the [Integration Guide](https://github.com/bradyclarke/simple-ssg/blob/main/docs/integration-guide.md) for more details.

## License

Simple-SSG is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Origins

Simple-SSG was developed by Brady Clarke as a lightweight alternative to complex static site generators, focusing on simplicity, performance, and maintainability. It was originally part of the Knowledge Architecture Framework project and has been extracted as a standalone package to benefit a wider audience.
