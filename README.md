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

Simple-SSG is configured using a `config.yaml` or `config.json` file. The following options are available:

```yaml
# Paths
# Directory containing your Markdown content files.
content_dir: content
# Path to your main HTML template file.
template_path: template.html
# Directory where the final static site will be generated.
output_dir: build
# List of directories containing static assets (CSS, images, etc.) to be copied.
static_dirs:
  - css
  - images
  - js
# Path to a root-level index.html file, if you have one.
index_path: index.html

# Build Options
# If true, the output directory will be deleted before each build.
clean_output: true
# If true, the generated HTML will be minified to reduce file size.
minify: true
# If true, content will be automatically wrapped in <section> tags based on headings.
wrap_sections: true

# Section Wrapping
# The CSS class to apply to <section> tags generated from <h1> headings.
h1_section_class: hero
# The CSS class to apply to <section> tags generated from <h2> headings.
h2_section_class: section

# SEO Settings
# The base URL of your final website (e.g., "https://example.com").
base_url: https://example.com
# If true, a sitemap.xml will be generated.
generate_sitemap: true
# If true, a robots.txt will be generated.
generate_robots: true
# If true, a .htaccess file with common web server settings will be generated.
generate_htaccess: true

# Content Handling
# A dictionary of path replacements to fix image links in your content.
image_path_replacements:
  ../images/: images/
# A list of extensions to use for the Python-Markdown library.
markdown_extensions:
  - extra
  - tables
  - smarty
```

## Template System

Simple-SSG uses a straightforward template system. Your `template.html` file serves as the master layout for all pages.

### Content Injection

The generator injects your converted Markdown content into the template by replacing the contents of a specific `div`. Your template should contain a `div` element with `id="content-container"`.

Example `div` in `template.html`:
```html
<main>
    <div class="container">
        <div id="content-container">
            <!-- Your Markdown content will be injected here -->
            <div class="loading">Loading content...</div>
        </div>
    </div>
</main>
```

### Automatic Metadata

Simple-SSG automatically extracts metadata from your content to populate tags in the `<head>` of your template:

-   **`<title>`**: The content of the first `<h1>` tag in your Markdown file is used as the page title.
-   **`<meta name="description">`**: The content of the first `<p>` tag that follows the `<h1>` is used as the meta description.

These values are also used to populate other SEO-related tags, such as Open Graph and Twitter Cards, if they exist in your template.

## Writing Content

### Class Annotations

You can add CSS classes to HTML elements directly from your Markdown files using the `{.classname}` syntax immediately after a block-level element.

```markdown
# Page Title {.custom-title}

This is the first paragraph.

## Section Title {.important}

> A blockquote with a class. {.note}
```

This will produce:
```html
<h1 class="custom-title">Page Title</h1>
<p>This is the first paragraph.</p>
<h2 class="important">Section Title</h2>
<blockquote class="note">
<p>A blockquote with a class.</p>
</blockquote>
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

`inline code`

```python
# A code block
def hello():
    print("Hello, World!")
```

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

## License

Simple-SSG is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Origins

Simple-SSG was developed by Brady Clarke as a lightweight alternative to complex static site generators, focusing on simplicity, performance, and maintainability. It was originally part of the Knowledge Architecture Framework project and has been extracted as a standalone package to benefit a wider audience.