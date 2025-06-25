# PyPI Publishing Guide

This guide covers the complete process for publishing Simple-SSG to PyPI, including validation, testing, and release procedures.

## Prerequisites

1. **PyPI Account**: Create accounts on both [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)
2. **API Tokens**: Generate API tokens for both repositories
3. **Development Environment**: Ensure you have the development dependencies installed:
   ```bash
   uv pip install -e ".[dev]"
   ```

## Pre-Publication Checklist

### 1. Code Quality Validation

Run the complete quality assurance pipeline:

```bash
# This runs package structure checks, import validation, linting, and tests
python run_code_quality.py
```

All checks must pass before proceeding.

### 2. Version Management

Update the version in `pyproject.toml`:

```toml
[project]
version = "x.y.z"  # Follow semantic versioning
```

Ensure the version in `simple_ssg/__init__.py` matches:

```python
__version__ = "x.y.z"
```

### 3. Documentation Updates

- Update CHANGELOG.md with release notes
- Verify README.md reflects current functionality
- Check that all documentation links work

### 4. Git Preparation

```bash
# Create release commit
git add .
git commit -m "Release version x.y.z"

# Create and push tag
git tag -a vx.y.z -m "Release version x.y.z"
git push origin main --tags
```

## Building the Package

### 1. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf dist/ build/ simple_ssg.egg-info/
```

### 2. Build Distribution Files

```bash
# Build both wheel and source distribution
python -m build
```

This creates:
- `dist/simple_ssg-x.y.z-py3-none-any.whl` (wheel)
- `dist/simple_ssg-x.y.z.tar.gz` (source)

### 3. Validate Build

```bash
# Check package metadata and structure
twine check dist/*
```

Must show "PASSED" for all files.

## Testing with TestPyPI

Always test with TestPyPI before publishing to production PyPI:

### 1. Upload to TestPyPI

```bash
# Configure TestPyPI if not already done
# Create ~/.pypirc with TestPyPI configuration

twine upload --repository testpypi dist/*
```

### 2. Test Installation

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ simple-ssg

# Test basic functionality
simple-ssg --help
simple-ssg init test-site
cd test-site
simple-ssg build
```

### 3. Verify Package

- Check that all dependencies install correctly
- Verify CLI commands work
- Test that example sites build successfully
- Confirm package metadata displays correctly on TestPyPI

## Publishing to PyPI

Once TestPyPI testing is successful:

### 1. Upload to PyPI

```bash
twine upload dist/*
```

### 2. Verify Publication

- Check package appears at https://pypi.org/project/simple-ssg/
- Verify metadata, description, and links display correctly
- Test installation: `pip install simple-ssg`

## Post-Publication Tasks

### 1. GitHub Release

Create a GitHub release:
- Go to https://github.com/bradyclarke/simple-ssg/releases
- Create new release with tag `vx.y.z`
- Upload the wheel and source distribution files
- Write release notes describing changes

### 2. Update Documentation

- Update any version-specific documentation
- Verify installation instructions still work
- Check that example projects work with new version

### 3. Communication

- Announce release in relevant channels
- Update any dependent projects
- Monitor for issues or feedback

## Security Considerations

### API Token Management

- Use scoped tokens (not global PyPI tokens)
- Store tokens securely (use environment variables)
- Never commit tokens to version control
- Rotate tokens regularly

### Trusted Publishing (Recommended)

Consider setting up OpenID Connect (OIDC) trusted publishing:
- No need for long-lived API tokens
- More secure authentication
- Automatic from GitHub Actions

## Troubleshooting

### Common Issues

1. **Upload Rejected**: Version already exists
   - Solution: Increment version number, rebuild, and retry

2. **Metadata Validation Fails**: 
   - Run `twine check dist/*` to see specific errors
   - Common issues: invalid README format, missing required fields

3. **Import Errors After Installation**:
   - Check package discovery configuration in pyproject.toml
   - Verify all modules are included in the build

4. **Dependency Conflicts**:
   - Review version constraints in dependencies
   - Test in clean environment

### Getting Help

- PyPI Help: https://pypi.org/help/
- Packaging Python Projects: https://packaging.python.org/
- Simple-SSG Issues: https://github.com/bradyclarke/simple-ssg/issues

## Automation

Consider setting up GitHub Actions for automated publishing:

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI
on:
  release:
    types: [published]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

This enables automatic publishing when you create a GitHub release.