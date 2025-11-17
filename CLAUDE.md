# CLAUDE.md - AI Assistant Guide for Simple-SSG

This document provides comprehensive guidance for AI assistants working on the Simple-SSG codebase. It explains the project structure, development workflows, conventions, and key architectural patterns.

## Project Overview

**Simple-SSG** is a minimalist static site generator written in Python that converts Markdown content to HTML. It focuses on simplicity, performance, and maintainability with minimal dependencies.

### Core Philosophy
- **Simplicity First**: Minimal dependencies (only `markdown` and `pyyaml`)
- **Zero Client-Side JavaScript**: Generated sites are pure HTML/CSS
- **Developer-Friendly**: Clean, understandable code with type hints
- **Modern Python**: Uses Python 3.8+ features and modern tooling

### Key Features
- Markdown-to-HTML conversion with custom class annotations `{.classname}`
- Template-based site generation with placeholder injection
- Automatic section wrapping based on heading structure
- SEO enhancements (sitemap, robots.txt, meta tags)
- HTML minification
- Development server with live preview
- CLI interface with `init`, `build`, and `serve` commands

---

## Project Structure

```
simple-ssg/
├── pyproject.toml           # Package metadata, dependencies, tool config
├── setup.py                 # Installation script
├── uv.lock                  # UV dependency lock file
├── LICENSE                  # MIT license
├── README.md                # User-facing documentation
├── CLAUDE.md                # This file - AI assistant guide
│
├── .github/
│   └── workflows/
│       ├── tests.yml        # CI: Run tests on push/PR (Python 3.8-3.11)
│       └── release.yml      # CD: Publish to PyPI on releases
│
├── docs/                    # Package documentation
│   ├── getting-started.md
│   ├── integration-guide.md
│   └── structure.md
│
├── examples/
│   └── basic-website/       # Example project showing usage
│       ├── config.yaml
│       ├── content/
│       ├── css/
│       ├── images/
│       └── template.html
│
├── simple_ssg/              # Main package source
│   ├── __init__.py          # Package exports: build_site, __version__
│   ├── __main__.py          # Enables `python -m simple_ssg`
│   ├── builder.py           # Core build logic
│   ├── cli.py               # Command-line interface
│   ├── config.py            # Configuration management
│   │
│   ├── converters/          # Content converters
│   │   ├── __init__.py
│   │   ├── markdown.py      # Markdown → HTML conversion
│   │   └── html.py          # HTML post-processing
│   │
│   ├── enhancers/           # Optional enhancements
│   │   ├── __init__.py
│   │   ├── minifier.py      # HTML minification
│   │   ├── seo.py           # SEO enhancements (sitemap, meta tags)
│   │   └── server.py        # Development server
│   │
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── fs.py            # Filesystem operations
│       └── templates.py     # Template handling
│
└── tests/                   # Test suite
    ├── fixtures/            # Test data
    ├── test_builder.py
    ├── test_config.py
    └── test_converters.py
```

---

## Architecture & Key Components

### 1. Build Pipeline (`builder.py`)

The build process follows this flow:

1. **Configuration Loading** (`config.py`)
   - Load from YAML/JSON file or dictionary
   - Apply defaults for unspecified values
   - Validate required files/directories exist

2. **Setup Build Directory**
   - Clean output directory if `clean_output: true`
   - Create output directory structure
   - Copy static assets (CSS, images, JS)
   - Copy `index.html` if specified

3. **Process Content Files**
   - Walk `content_dir` to find `.md` and `.markdown` files
   - Skip `README.md` files
   - For each file:
     - Read content
     - Fix image paths using `image_path_replacements`
     - Convert Markdown to HTML
     - Wrap sections if `wrap_sections: true`
     - Inject into template
     - Minify if `minify: true`
     - Write to output directory

4. **Generate SEO Files** (if enabled)
   - `sitemap.xml` - XML sitemap with priorities
   - `robots.txt` - Crawler directives
   - `.htaccess` - Apache server config

5. **Return Statistics**
   - Files processed
   - Errors encountered
   - Build time

### 2. Markdown Conversion (`converters/markdown.py`)

Key function: `convert_markdown_to_html(md_content, config)`

- Uses Python `markdown` library with configurable extensions
- Default extensions: `['extra', 'tables', 'smarty']`
- Post-processing: `process_class_annotations(html)`

**Class Annotation Syntax**:
```markdown
# Heading {.hero}
[Link text](url){.special-link}
> Blockquote {.note}
```

Pattern: `(<tag>content</tag>){.classname}`
- Supports multiple classes: `{.class1.class2}`
- Merges with existing class attributes
- Uses regex (not a full HTML parser)

### 3. Template System (`utils/templates.py`)

Key function: `inject_content(content, content_path, config)`

**Template Placeholders**:
- `<div id="content-container">` - Content injection point
- `<title>` - Page title (from first H1 or front matter)
- `<meta name="description" content="">` - Meta description
- Open Graph and Twitter Card tags

**Metadata Extraction**:
- Title: First `<h1>` tag from content
- Description: First `<p>` after `<h1>`, truncated to 160 chars
- Updates all meta tags for SEO

### 4. Configuration System (`config.py`)

`SiteConfig` class manages configuration with:
- **Default values** for all settings
- **File loading** from YAML/JSON
- **Dictionary override** for programmatic use
- **Validation** of required files/directories
- **Test mode** to skip validation for tests

**Key Configuration Options**:
```yaml
# Paths
content_dir: content
template_path: template.html
output_dir: build
static_dirs: [css, images, js]
index_path: index.html

# Build options
clean_output: true
minify: true
wrap_sections: true
h1_section_class: hero
h2_section_class: section

# SEO
base_url: https://example.com
generate_sitemap: true
generate_robots: true
generate_htaccess: true

# Image paths
image_path_replacements:
  ../images/: images/

# Markdown
markdown_extensions: [extra, tables, smarty]
```

### 5. CLI Interface (`cli.py`)

Three main commands:

**`simple-ssg init [directory]`**
- Creates project structure
- Generates template files
- Creates example content
- Writes default config

**`simple-ssg build [--config config.yaml]`**
- Builds static site
- Accepts CLI overrides for config values
- Returns exit code 1 on errors

**`simple-ssg serve [directory] [--port 8000]`**
- Starts local HTTP server
- Opens browser automatically (unless `--no-browser`)
- Serves from `build/` by default

---

## Development Workflows

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/bradyclarke/simple-ssg.git
cd simple-ssg

# Install with uv (recommended)
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_builder.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=simple_ssg
```

**Test Structure**:
- Uses Python's `unittest` framework
- Creates temporary directories in `setUp()`
- Cleans up in `tearDown()`
- Each test is isolated with its own temp directory

**Example Test Pattern**:
```python
def test_basic_page_build(self):
    # Create test markdown file
    md_path = os.path.join(self.content_dir, 'test.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('# Test Page\n\nThis is a test page.')

    # Create config
    config_dict = {
        'content_dir': self.content_dir,
        'template_path': self.template_path,
        'output_dir': self.output_dir,
        'static_dirs': [],
        'base_url': 'http://example.com',
        'minify': False
    }

    # Build the site
    stats = build_site(config_dict=config_dict)

    # Assertions
    self.assertEqual(stats['processed'], 1)
    self.assertEqual(stats['errors'], 0)
```

### Code Quality Tools

**Ruff** (linting):
```bash
ruff check simple_ssg
ruff check simple_ssg --fix  # Auto-fix issues
```

**Configuration** (in `pyproject.toml`):
- Line length: 100
- Target: Python 3.8+
- Selected rules: E, F, B, I, W, C4, UP, N, ANN, DTZ, COM
- Ignored: ANN101 (self type), ANN401 (Any type)

**Type Checking** (mypy):
```bash
mypy simple_ssg
```

### Making Changes

When implementing features or fixing bugs:

1. **Read relevant code first**
   - Understand existing patterns
   - Check similar implementations
   - Review configuration options

2. **Write tests first (TDD recommended)**
   - Create test case in appropriate `tests/test_*.py`
   - Ensure test fails initially
   - Implement feature
   - Verify test passes

3. **Follow existing patterns**
   - Use type hints on all functions
   - Add docstrings with Parameters/Returns sections
   - Handle exceptions gracefully with try/except
   - Print informative error messages

4. **Update documentation**
   - Update README.md if user-facing changes
   - Update docstrings if API changes
   - Add comments for complex logic

5. **Run quality checks**
   - Run tests: `pytest`
   - Check linting: `ruff check simple_ssg`
   - Verify types: `mypy simple_ssg` (if configured)

---

## Code Conventions

### Python Style

**Type Hints**:
```python
def convert_markdown_to_html(md_content: str, config: SiteConfig = None) -> str:
    """Convert Markdown content to HTML."""
    pass
```

**Docstrings**:
```python
def inject_content(content, content_path, config):
    """
    Inject content into the template.

    Parameters:
    - content: The HTML content to inject
    - content_path: Path to the original content file
    - config: Configuration object

    Returns:
    - Complete HTML page with content injected
    """
```

**Error Handling**:
```python
try:
    # Operation that might fail
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    print(f"Error: File {file_path} has encoding issues.")
    return False
except Exception as e:
    print(f"Error processing {file_path}: {str(e)}")
    return False
```

**Imports**:
- Standard library first
- Third-party packages second
- Local imports third
- Sorted alphabetically within each group

### File Organization

**Module Structure**:
- `__init__.py` - Package exports and metadata
- One main class or set of related functions per file
- Helper functions at module level (not nested)

**Naming**:
- `snake_case` for functions, variables, module names
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Private functions start with `_`

### Common Patterns

**Configuration Access**:
```python
# Always check config exists and has attribute
extensions = config.markdown_extensions if config else ['extra', 'tables', 'smarty']
```

**File I/O**:
```python
# Always use encoding='utf-8'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
```

**Path Handling**:
```python
# Use os.path for cross-platform compatibility
rel_path = os.path.relpath(content_path, config.content_dir)
output_path = os.path.join(config.output_dir, f"{base_name}.html")
```

**Directory Creation**:
```python
# Use ensure_dir utility
from simple_ssg.utils.fs import ensure_dir
ensure_dir(output_directory)
```

---

## Testing Guidelines

### Test File Organization

- One test file per module: `test_builder.py`, `test_config.py`, etc.
- Test fixtures in `tests/fixtures/`
- Use `unittest.TestCase` as base class

### Test Naming

- Test methods start with `test_`
- Descriptive names: `test_basic_page_build`, `test_empty_site_build`

### Test Data

- Create temporary directories with `tempfile.mkdtemp()`
- Always clean up in `tearDown()`
- Don't rely on files in the repository (except fixtures)

### Assertions

Use specific assertions:
- `assertEqual(a, b)` not `assertTrue(a == b)`
- `assertIn(x, y)` not `assertTrue(x in y)`
- `assertTrue(os.path.exists(path))` for file existence

### Test Coverage Priorities

1. **Core functionality** (builder, converters) - HIGH
2. **Configuration loading** - HIGH
3. **CLI commands** - MEDIUM
4. **SEO enhancements** - MEDIUM
5. **Edge cases** (empty files, missing directories) - MEDIUM
6. **Development server** - LOW (interactive component)

---

## CI/CD Pipeline

### GitHub Actions Workflows

**Tests Workflow** (`.github/workflows/tests.yml`):
- Triggers: Push/PR to `main` or `master`
- Matrix testing: Python 3.8, 3.9, 3.10, 3.11
- Steps:
  1. Checkout code
  2. Set up Python
  3. Install uv
  4. Install dependencies with uv
  5. Run pytest

**Release Workflow** (`.github/workflows/release.yml`):
- Triggers: New GitHub release created
- Publishes package to PyPI
- Uses trusted publishing (no API token needed)

### Local Validation Scripts

Several validation scripts are available:

- `check_imports.py` - Verify package imports
- `check_package.py` - Validate package structure
- `run_code_quality.py` - Run linting checks
- `run_validation.py` - Run all validations
- `validate_for_publishing.py` - Pre-publish checks

---

## Common Tasks for AI Assistants

### Adding a New Configuration Option

1. **Add default in `config.py`**:
   ```python
   def set_defaults(self):
       # ... existing defaults ...
       self.new_option = 'default_value'
   ```

2. **Update README.md** with configuration example

3. **Add test in `test_config.py`**:
   ```python
   def test_new_option_config(self):
       config = SiteConfig(config_dict={'new_option': 'test_value'})
       self.assertEqual(config.new_option, 'test_value')
   ```

### Adding a New CLI Command

1. **Add subparser in `cli.py`**:
   ```python
   new_parser = subparsers.add_parser('newcommand', help='Description')
   new_parser.add_argument('--option', help='Option help')
   ```

2. **Add handler function**:
   ```python
   def run_newcommand(args):
       """Run the newcommand."""
       # Implementation
   ```

3. **Wire up in `main()`**:
   ```python
   elif args.command == 'newcommand':
       run_newcommand(args)
   ```

4. **Update README.md** with command documentation

### Adding a New Markdown Extension

1. **Update default in `config.py`**:
   ```python
   self.markdown_extensions = ['extra', 'tables', 'smarty', 'new_extension']
   ```

2. **Ensure extension is available** (add to dependencies if needed)

3. **Test with sample content** in `test_converters.py`

### Adding a New Enhancer

1. **Create file in `simple_ssg/enhancers/`**:
   ```python
   """Description of enhancer."""

   def enhance_feature(config):
       """Enhance the feature."""
       try:
           # Implementation
           print("Enhancer applied successfully")
       except Exception as e:
           print(f"Error in enhancer: {str(e)}")
   ```

2. **Import in `builder.py`**

3. **Call from build pipeline**:
   ```python
   if config.enable_feature:
       enhance_feature(config)
   ```

4. **Add configuration option** (see above)

### Debugging Build Issues

**Enable verbose output**:
- Check print statements in `builder.py`
- Each processed file prints: `Processed filename.md → filename.html`

**Common issues**:
- **No output files**: Check `content_dir` has `.md` files
- **Template not found**: Verify `template_path` exists
- **Static files missing**: Check `static_dirs` exist
- **Encoding errors**: Ensure files are UTF-8
- **Regex issues in class annotations**: Check for nested tags

**Debugging pattern**:
```python
# Add temporary debug prints
print(f"DEBUG: Processing {content_path}")
print(f"DEBUG: Output path {output_path}")
print(f"DEBUG: Content length {len(content)}")
```

---

## Important Dependencies

### Runtime Dependencies

**markdown** (>=3.3.0):
- Converts Markdown to HTML
- Extensible with plugins
- Documentation: https://python-markdown.github.io/

**pyyaml** (>=6.0):
- Parses YAML configuration files
- Safe loading with `yaml.safe_load()`
- Documentation: https://pyyaml.org/

### Development Dependencies

**pytest**:
- Test framework
- Run with `pytest` command

**ruff**:
- Fast Python linter
- Replaces flake8, isort, black
- Configured in `pyproject.toml`

**uv**:
- Fast Python package installer
- Used in CI/CD
- Drop-in replacement for pip

---

## API Usage Examples

### Programmatic Usage

```python
from simple_ssg import build_site

# Using config file
build_site(config_file="config.yaml")

# Using config dictionary
config = {
    "content_dir": "content",
    "template_path": "template.html",
    "output_dir": "build",
    "static_dirs": ["css", "images"],
    "minify": True,
    "base_url": "https://mysite.com"
}
stats = build_site(config_dict=config)

print(f"Processed {stats['processed']} files in {stats['build_time']:.2f}s")
```

### Custom Build Pipeline

```python
from simple_ssg.builder import build_site
from simple_ssg.config import SiteConfig
from simple_ssg.enhancers.seo import generate_sitemap
from simple_ssg.enhancers.minifier import minify_html

# Load config
config = SiteConfig(config_file="config.yaml")

# Build site
stats = build_site(config_dict={"minify": False})  # Build without minification

# Custom post-processing
for html_file in glob.glob(os.path.join(config.output_dir, "**/*.html")):
    with open(html_file, 'r') as f:
        content = f.read()

    # Custom processing
    processed = custom_process(content)

    with open(html_file, 'w') as f:
        f.write(processed)

# Generate sitemap after custom processing
generate_sitemap(config)
```

---

## Troubleshooting Guide

### Installation Issues

**Problem**: `ModuleNotFoundError: No module named 'simple_ssg'`
- **Solution**: Install in development mode: `pip install -e .`

**Problem**: `command not found: simple-ssg`
- **Solution**: Ensure installation completed and scripts are in PATH
- Try: `python -m simple_ssg` instead

### Build Issues

**Problem**: No HTML files generated
- Check `content_dir` exists and contains `.md` files
- Verify files don't have encoding issues (must be UTF-8)
- Check for errors in console output

**Problem**: Template not applied
- Verify `template.html` exists at `template_path`
- Check template has `<div id="content-container">` placeholder
- Ensure placeholder has closing `</div>`

**Problem**: Static assets not copied
- Verify directories in `static_dirs` exist
- Check directory names don't have typos
- Ensure `clean_output: true` isn't removing them

### Content Issues

**Problem**: Class annotations not working `{.classname}`
- Ensure syntax is correct: `{.classname}` immediately after tag
- Check for spaces: `</h1> {.class}` won't work, use `</h1>{.class}`
- Verify element isn't nested in complex HTML

**Problem**: Images not showing
- Check `image_path_replacements` in config
- Verify images are in `static_dirs`
- Ensure image paths in Markdown match replacement rules

### Testing Issues

**Problem**: Tests fail with file not found
- Check test creates temp directory in `setUp()`
- Verify test creates all required files (template, content)
- Ensure `tearDown()` uses correct temp directory

**Problem**: Tests pass locally but fail in CI
- Check Python version compatibility (supports 3.8+)
- Verify no absolute paths in tests
- Ensure no OS-specific path separators (use `os.path.join()`)

---

## Security Considerations

### Input Validation

- **Markdown content**: Sanitized by markdown library
- **Configuration files**: Use `yaml.safe_load()` (not `load()`)
- **File paths**: Validate paths stay within project directory
- **Template injection**: No eval/exec used, only string replacement

### File Operations

- **Encoding**: Always specify `encoding='utf-8'`
- **Path traversal**: Use `os.path` functions, not string concatenation
- **Permissions**: Don't modify file permissions unnecessarily

### Third-Party Dependencies

- Minimal dependencies reduce attack surface
- Dependencies pinned with version constraints
- Regular updates via Dependabot (if configured)

---

## Performance Considerations

### Build Performance

- **No caching**: Each build is from scratch (when `clean_output: true`)
- **File I/O**: Most time spent in file reads/writes
- **Markdown conversion**: Fast, but scales with content size
- **Regex processing**: Class annotations use regex, fast for typical content

### Optimization Opportunities

1. **Incremental builds**: Only rebuild changed files (not implemented)
2. **Parallel processing**: Process multiple files concurrently (not implemented)
3. **Template caching**: Load template once, reuse for all pages (not implemented)
4. **Minification**: Disable for faster dev builds, enable for production

### Scalability

- **Small sites (<100 pages)**: Instant builds (<1 second)
- **Medium sites (100-1000 pages)**: Fast builds (1-10 seconds)
- **Large sites (>1000 pages)**: Consider incremental builds

---

## Future Development Ideas

### Potential Enhancements

1. **Front matter support**: Parse YAML front matter from Markdown files
2. **Pagination**: Auto-generate paginated lists
3. **RSS/Atom feeds**: Generate feeds from content
4. **Image optimization**: Auto-resize and optimize images
5. **Syntax highlighting**: Add code block highlighting
6. **Live reload**: Auto-refresh browser on file changes
7. **Themes**: Pre-built templates and styles
8. **Plugins**: Plugin system for custom enhancers
9. **Watch mode**: Auto-rebuild on file changes
10. **Template inheritance**: Support for template extends/includes

### Extension Points

The architecture supports extensions via:
- **Converters**: Add new content format converters
- **Enhancers**: Add new build enhancements
- **Template functions**: Add custom template placeholders
- **CLI commands**: Add new commands to CLI

---

## Related Documentation

- **README.md**: User-facing documentation and quick start
- **docs/getting-started.md**: Detailed getting started guide
- **docs/integration-guide.md**: Using Simple-SSG in other projects
- **docs/structure.md**: Package structure explanation
- **pyproject.toml**: Package metadata and tool configuration
- **examples/basic-website/**: Complete working example

---

## Questions & Support

When working on this codebase:

1. **Read the code**: Start with the module you're working on
2. **Check existing patterns**: Look for similar implementations
3. **Run tests**: Verify your changes don't break existing functionality
4. **Test manually**: Use the example site to test changes
5. **Follow conventions**: Match existing code style and patterns

For specific questions about implementation details, refer to:
- Function docstrings for API details
- Test files for usage examples
- README.md for user-facing features
- This file (CLAUDE.md) for architecture and patterns

---

**Last Updated**: 2025-11-17
**Version**: 0.1.0
**Maintainer**: Brady Clarke
**Repository**: https://github.com/bradyclarke/simple-ssg
