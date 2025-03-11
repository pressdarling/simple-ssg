# Simple-SSG Integration Guide

This guide explains how to integrate Simple-SSG into your own projects.

## Using Simple-SSG as a Library

Simple-SSG can be used as a library in your Python projects, allowing you to customize the build process or integrate it into larger applications.

### Installation

```bash
# Recommended: install with uv for faster, more reliable dependency management
uv pip install simple-ssg

# Or use pip if you don't have uv
pip install simple-ssg
```

### Basic Integration

Here's a simple example of using Simple-SSG in your own code:

```python
from simple_ssg import build_site

# Configure the site
config = {
    'content_dir': 'content',
    'template_path': 'template.html',
    'output_dir': 'build',
    'static_dirs': ['css', 'images', 'js'],
    'base_url': 'https://example.com',
    'minify': True
}

# Build the site
stats = build_site(config_dict=config)

# Print build statistics
print(f"Files processed: {stats['processed']}")
print(f"Build time: {stats['build_time']} seconds")
```

### Using Individual Components

You can also use individual components of Simple-SSG:

```python
from simple_ssg.converters.markdown import convert_markdown_to_html
from simple_ssg.enhancers.minifier import minify_html
from simple_ssg.utils.fs import ensure_dir

# Convert Markdown to HTML
markdown_content = "# Hello, World!\n\nThis is a test."
html_content = convert_markdown_to_html(markdown_content)

# Minify HTML
minified_html = minify_html(html_content)

# Ensure directory exists
ensure_dir('output')

# Write to file
with open('output/hello.html', 'w', encoding='utf-8') as f:
    f.write(minified_html)
```

## Integration Patterns

### 1. As a Pre-build Step

You can use Simple-SSG as a pre-build step in larger web applications:

```python
import subprocess
from simple_ssg import build_site

# Build the static site
build_site(config_file='config.yaml')

# Run another build process
subprocess.run(['npm', 'run', 'build'])
```

### 2. As a Content Processor

You can use Simple-SSG to process content for another system:

```python
from simple_ssg.converters.markdown import convert_markdown_to_html

def process_content(markdown_content):
    # Convert Markdown to HTML
    html_content = convert_markdown_to_html(markdown_content)

    # Perform additional processing
    # ...

    return html_content
```

### 3. As a Git Submodule

For more complex projects, you can include Simple-SSG as a Git submodule:

```bash
# Add Simple-SSG as a submodule
git submodule add https://github.com/bradyclarke/simple-ssg.git tools/simple-ssg

# Initialize and update the submodule
git submodule update --init --recursive
```

Then in your Python code:

```python
import sys
import os

# Add the submodule to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools/simple-ssg'))

# Import Simple-SSG
from simple_ssg import build_site

# Use Simple-SSG
build_site(config_file='config.yaml')
```

## Using Simple-SSG with GitHub Actions

You can use Simple-SSG in a GitHub Actions workflow to build and deploy your site:

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install simple-ssg

      - name: Build site
        run: |
          simple-ssg build --config config.yaml

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

## Using Simple-SSG with Custom Template Engines

Simple-SSG uses a simple template system by default, but you can extend it to use other template engines:

```python
from simple_ssg import build_site
from jinja2 import Environment, FileSystemLoader

# Create a custom template processor
def jinja2_process_template(content, template_path, **kwargs):
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))

    # Load the template
    template = env.get_template(template_path)

    # Render the template with content
    return template.render(content=content, **kwargs)

# Configure Simple-SSG with your custom template processor
config = {
    'content_dir': 'content',
    'template_path': 'templates/base.html',
    'output_dir': 'build',
    'template_processor': jinja2_process_template
}

# Build the site
build_site(config_dict=config)
```

## Contributing to Simple-SSG

If you make improvements to Simple-SSG while using it in your project, consider contributing back to the main repository:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

We welcome contributions of all kinds, from bug fixes to new features!
