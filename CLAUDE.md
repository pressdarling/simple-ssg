# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Simple-SSG is a minimalist static site generator that converts Markdown to HTML with minimal dependencies and maximum simplicity.

## Essential Commands

```bash
# Development setup (prefers uv package manager)
uv pip install -e ".[dev]"

# Run all quality checks (linting, tests, package validation)
python run_code_quality.py

# Build and serve a site
cd examples/basic-website
simple-ssg build --config config.yaml
simple-ssg serve

# Initialize new project
simple-ssg init my-site --template basic

# Package building and PyPI validation
python -m build              # Build package
twine check dist/*           # Validate for PyPI
```

## Architecture

**Core Flow**: Configuration → Content Processing → Template Injection → Enhancement → Output

**Key Files**:
- `builder.py` - Main build orchestration via `build_site()`
- `config.py` - `SiteConfig` class handles YAML/JSON config with defaults
- `cli.py` - Command-line interface with build/serve/init commands

**Modular Systems**:
- `converters/` - Markdown to HTML conversion
- `enhancers/` - SEO, minification, dev server
- `utils/` - Filesystem and template operations

## Key Patterns

**Configuration**: File config → CLI args → defaults precedence

**Content**: Markdown files in `content/` become HTML pages with:
- Front matter for metadata
- `{.classname}` for CSS classes
- Automatic section wrapping on headings

**Templates**: `{{content}}`, `{{title}}`, `{{description}}` placeholders

**Error Handling**: Graceful degradation - build continues despite individual file errors

## Development Notes

- Uses `ruff` for linting, `pytest` for tests
- Template injection looks for `<div id="content-container">` first, falls back to other methods
- Static assets (CSS, images, JS) copied automatically
- Build statistics track processed files, errors, and timing
- Package discovery configured to exclude logs/, .claude-trace/, .claude/
- Optional dependencies: `[dev]` for full development, `[test]` for testing only
- PyPI-ready with modern metadata (SPDX license, keywords, comprehensive URLs)