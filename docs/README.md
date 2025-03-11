# Simple-SSG Documentation

This directory contains the documentation for the Simple-SSG package, a lightweight static site generator that converts Markdown content to HTML.

## Documentation Files

- [**getting-started.md**](getting-started.md) - Guide for getting started with Simple-SSG
- [**integration-guide.md**](integration-guide.md) - Guide for integrating Simple-SSG into other projects
- [**structure.md**](structure.md) - Explanation of the Simple-SSG package structure

## Simple-SSG Overview

Simple-SSG is a minimalist static site generator with the following features:

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

## Key Concepts

### Content Management

Simple-SSG uses Markdown files for content, which are converted to HTML during the build process. Key features:

- **Front Matter**: YAML metadata at the top of Markdown files
- **Class Annotations**: Add CSS classes using the `{.classname}` syntax
- **Section Wrapping**: Automatically wraps headings in section elements

### Build Process

The build process involves several steps:

1. **Configuration**: Load settings from config file
2. **Content Processing**: Convert Markdown to HTML
3. **Template Application**: Apply templates to content
4. **Enhancement**: Apply optional enhancements (minification, SEO)
5. **Output Generation**: Write files to output directory

### Extension Points

Simple-SSG can be extended in several ways:

- **Custom Converters**: Create new content converters
- **Custom Enhancers**: Add new enhancement functionality
- **Template Customization**: Create custom templates
- **Configuration**: Customize build behavior through config

## Using the Documentation

- Start with [getting-started.md](getting-started.md) for a basic introduction
- Read [integration-guide.md](integration-guide.md) to learn how to integrate Simple-SSG into other projects
- Review [structure.md](structure.md) to understand the package architecture

For code examples, see the [examples directory](../examples/).

## Related Resources

- [Simple-SSG README](../README.md) - Overview of Simple-SSG
- [Simple-SSG Code](../simple_ssg/) - Source code for the package
- [Simple-SSG Tests](../tests/) - Test suite
- [Example Projects](../examples/) - Example websites built with Simple-SSG

## Package Status

Simple-SSG is a standalone package that could be extracted into its own repository if needed. It is currently part of the Knowledge Architecture Framework project but is designed to be fully independent.

For information about how Simple-SSG is used in the Knowledge Architecture Framework website, see the [Build Documentation](../../docs/build/README.md).
