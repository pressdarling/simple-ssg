# Contributing to Simple-SSG

Thank you for your interest in contributing to Simple-SSG! This guide will help you get started with the development environment and understand our contribution process.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Git

### Getting Started

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/simple-ssg.git
   cd simple-ssg
   ```

2. **Set up Development Environment**
   ```bash
   # Using uv (recommended)
   uv pip install -e ".[dev]"
   
   # Or using pip
   pip install -e ".[dev]"
   ```

3. **Verify Installation**
   ```bash
   # Test the CLI
   simple-ssg --help
   
   # Run tests
   pytest
   
   # Run quality checks
   python run_code_quality.py
   ```

## Development Dependencies

The `[dev]` dependency group includes:

- **pytest** & **pytest-cov**: Testing framework and coverage
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checking
- **twine**: PyPI package uploading
- **build**: Package building tools

## Code Quality Standards

Simple-SSG maintains high code quality through automated tools:

### Linting and Formatting

```bash
# Check code style and potential issues
ruff check simple_ssg

# Automatically fix issues where possible
ruff check --fix simple_ssg

# Format code
ruff format simple_ssg
```

### Type Checking

```bash
# Run type checker
mypy simple_ssg
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=simple_ssg

# Run specific test file
pytest tests/test_builder.py

# Run specific test
pytest tests/test_builder.py::TestBuilder::test_basic_build
```

### Complete Quality Check

```bash
# Run all quality checks (this is what CI runs)
python run_code_quality.py
```

## Project Structure

```
simple-ssg/
├── simple_ssg/          # Main package
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # Command-line interface
│   ├── builder.py       # Core build logic
│   ├── config.py        # Configuration handling
│   ├── converters/      # Content conversion
│   ├── enhancers/       # Post-processing
│   └── utils/           # Utility functions
├── tests/               # Test suite
│   ├── test_*.py        # Test modules
│   └── fixtures/        # Test data
├── examples/            # Example projects
├── docs/                # Documentation
└── pyproject.toml       # Package configuration
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style and patterns
- Add type hints for new functions
- Update docstrings for public APIs

### 3. Add Tests

All new functionality should include tests:

```bash
# Add tests in the appropriate test_*.py file
# Run tests to ensure they pass
pytest tests/test_your_module.py
```

### 4. Update Documentation

- Update docstrings for any API changes
- Update README.md if adding new features
- Add entries to appropriate documentation files

### 5. Commit Changes

```bash
git add .
git commit -m "Add feature: brief description"
```

Follow these commit message guidelines:
- Use imperative mood ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Reference issues when applicable ("Fixes #123")

## Testing Guidelines

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names that explain what is being tested
- Include both positive and negative test cases
- Test edge cases and error conditions

### Test Structure

```python
def test_function_name_scenario(self):
    """Test description explaining what this test validates."""
    # Arrange - set up test data
    input_data = "test input"
    expected = "expected output"
    
    # Act - call the function being tested
    result = function_under_test(input_data)
    
    # Assert - verify the result
    self.assertEqual(result, expected)
```

### Test Coverage

Aim for high test coverage, especially for:
- Core functionality (builder, converters)
- Error handling paths
- Edge cases and boundary conditions
- CLI interface

## Pull Request Process

1. **Ensure Quality**: All tests pass and code meets quality standards
   ```bash
   python run_code_quality.py
   ```

2. **Update Documentation**: Include any necessary documentation updates

3. **Create Pull Request**: 
   - Use a descriptive title
   - Reference any related issues
   - Describe what changes were made and why
   - Include testing instructions for reviewers

4. **Address Feedback**: Respond to review comments and make requested changes

5. **Merge**: Once approved, your PR will be merged by a maintainer

## Code Style Guidelines

### Python Style

- Follow PEP 8 (enforced by ruff)
- Use type hints for function parameters and return values
- Write clear, descriptive variable and function names
- Keep functions focused and single-purpose
- Use docstrings for public APIs

### Documentation Style

- Use clear, concise language
- Include examples for complex functionality
- Keep documentation up-to-date with code changes
- Follow existing documentation patterns

### Example Code Style

```python
def convert_markdown_to_html(content: str, config: SiteConfig | None = None) -> str:
    """
    Convert Markdown content to HTML.
    
    Args:
        content: The Markdown content to convert
        config: Optional configuration object
        
    Returns:
        Converted HTML content
        
    Raises:
        ValueError: If content is invalid
        
    Example:
        >>> convert_markdown_to_html("# Hello")
        '<h1>Hello</h1>'
    """
    if not content:
        raise ValueError("Content cannot be empty")
        
    # Implementation here
    return html_content
```

## Issue Guidelines

### Reporting Bugs

Include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and operating system
- Minimal code example if applicable

### Requesting Features

Include:
- Clear description of the desired functionality
- Use cases and motivation
- Proposed API or interface (if applicable)
- Willingness to implement the feature

## Release Process

Releases are managed by maintainers following semantic versioning:

- **Patch** (x.y.Z): Bug fixes, small improvements
- **Minor** (x.Y.z): New features, non-breaking changes  
- **Major** (X.y.z): Breaking changes

## Getting Help

- **Documentation**: Check README.md and docs/
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Code**: Look at existing code and tests for examples

## License

By contributing to Simple-SSG, you agree that your contributions will be licensed under the MIT License.

## Recognition

All contributors are valued and will be recognized in:
- Git commit history
- Release notes for significant contributions
- Contributors list (if we add one)

Thank you for contributing to Simple-SSG!