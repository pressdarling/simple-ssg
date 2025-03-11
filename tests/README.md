# Simple-SSG Test Suite

This directory contains the test suite for the Simple-SSG package. The tests ensure that the package functions correctly and maintains its quality as it evolves.

## Test Files

- [**test_builder.py**](test_builder.py) - Tests for the core build functionality
- [**test_config.py**](test_config.py) - Tests for configuration loading and processing
- [**test_converters.py**](test_converters.py) - Tests for content converters

## Test Fixtures

The `fixtures` directory contains test data used by the tests:

- [**fixtures/test_content.md**](fixtures/test_content.md) - Sample Markdown content
- [**fixtures/test_template.html**](fixtures/test_template.html) - Sample HTML template

## Running Tests

You can run the tests using pytest:

```bash
# From the simple_ssg directory
pytest

# Run with coverage
pytest --cov=simple_ssg

# Run specific test file
pytest tests/test_builder.py

# Run with verbose output
pytest -v
```

## Test Structure

The tests follow a consistent structure:

1. **Test Functions**: Named with `test_` prefix to be discovered by pytest
2. **Fixtures**: Reusable test data and setup functions
3. **Assertions**: Verify expected behavior
4. **Coverage**: Aim for comprehensive coverage of the codebase

## Test Categories

### Builder Tests

Tests for the core build functionality:

- Building sites from Markdown content
- Applying templates
- Processing static assets
- Handling errors

### Config Tests

Tests for configuration handling:

- Loading configuration from files
- Processing configuration options
- Handling invalid configurations
- Default configuration behavior

### Converter Tests

Tests for content converters:

- Converting Markdown to HTML
- Processing frontmatter
- Handling custom class annotations
- Error handling

## Adding Tests

When adding new features, also add tests that verify the feature works correctly:

1. **Create Test Cases**: Think about what scenarios need to be tested
2. **Write Test Functions**: Create test functions that check these scenarios
3. **Use Fixtures**: Reuse existing fixtures or create new ones as needed
4. **Run Tests**: Make sure all tests pass
5. **Check Coverage**: Ensure good test coverage for the new feature

## Continuous Integration

These tests are automatically run on GitHub using GitHub Actions when changes are pushed to the repository. The workflow configuration is in `.github/workflows/tests.yml`.

## Test Philosophy

The test suite follows these principles:

1. **Comprehensive**: Test all important functionality
2. **Fast**: Tests should run quickly to enable rapid development
3. **Independent**: Tests should not depend on each other
4. **Readable**: Tests should be easy to understand
5. **Maintainable**: Tests should be easy to update as the code evolves

For more information about Simple-SSG, see the [Simple-SSG Documentation](../docs/README.md).
