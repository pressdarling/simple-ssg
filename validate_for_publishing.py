#!/usr/bin/env python3
"""
This script validates the Simple-SSG package for publishing to PyPI.
"""

import os
import sys
import subprocess
import shutil
import re
import importlib
import importlib.metadata

def check_version_consistency():
    """Check if version is consistent across the package"""
    print("\n=== Checking Version Consistency ===")
    
    # Get version from __init__.py
    init_version = None
    init_path = os.path.join('simple_ssg', '__init__.py')
    if os.path.exists(init_path):
        with open(init_path, 'r', encoding='utf-8') as f:
            content = f.read()
            version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                init_version = version_match.group(1)
                print(f"✓ Version in __init__.py: {init_version}")
            else:
                print("✗ Could not find __version__ in __init__.py")
    else:
        print(f"✗ File not found: {init_path}")
    
    # Get version from pyproject.toml
    pyproject_version = None
    if os.path.exists('pyproject.toml'):
        with open('pyproject.toml', 'r', encoding='utf-8') as f:
            content = f.read()
            version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                pyproject_version = version_match.group(1)
                print(f"✓ Version in pyproject.toml: {pyproject_version}")
            else:
                print("✗ Could not find version in pyproject.toml")
    else:
        print("✗ File not found: pyproject.toml")
    
    # Compare versions
    if init_version and pyproject_version:
        if init_version == pyproject_version:
            print(f"✓ Versions match: {init_version}")
            return True, init_version
        else:
            print(f"✗ Version mismatch: __init__.py ({init_version}) vs pyproject.toml ({pyproject_version})")
            return False, None
    else:
        print("✗ Could not compare versions, some versions not found")
        return False, None

def check_package_metadata():
    """Check if package metadata is complete"""
    print("\n=== Checking Package Metadata ===")
    
    if not os.path.exists('pyproject.toml'):
        print("✗ pyproject.toml not found")
        return False
    
    with open('pyproject.toml', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check required metadata
    required_fields = [
        ('name', r'name\s*=\s*["\']([^"\']+)["\']'),
        ('version', r'version\s*=\s*["\']([^"\']+)["\']'),
        ('description', r'description\s*=\s*["\']([^"\']+)["\']'),
        ('authors', r'authors\s*='),
        ('readme', r'readme\s*='),
        ('requires-python', r'requires-python\s*='),
        ('dependencies', r'dependencies\s*='),
        ('license', r'license\s*=') # Optional but recommended
    ]
    
    all_required = True
    for field_name, pattern in required_fields:
        match = re.search(pattern, content)
        if match:
            value = match.group(1) if len(match.groups()) > 0 else "[defined]"
            print(f"✓ {field_name}: {value}")
        else:
            # License is optional
            if field_name == 'license':
                print(f"ℹ {field_name}: not specified (optional)")
            else:
                print(f"✗ {field_name}: not found")
                all_required = False
    
    return all_required

def check_pypi_existence(package_name, version):
    """Check if the package version already exists on PyPI"""
    print(f"\n=== Checking PyPI for {package_name} {version} ===")
    
    try:
        # Try to fetch the package from PyPI
        result = subprocess.run(
            ['pip', 'index', 'versions', package_name], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0 and package_name in result.stdout:
            print(f"✓ Package {package_name} exists on PyPI")
            
            # Check if the version exists
            if version in result.stdout:
                print(f"✗ Version {version} already exists on PyPI")
                return False
            else:
                print(f"✓ Version {version} does not exist on PyPI yet")
                return True
        else:
            print(f"✓ Package {package_name} does not exist on PyPI yet")
            return True
    except Exception as e:
        print(f"! Error checking PyPI: {e}")
        print("✓ Continuing validation")
        return True

def check_build_dist():
    """Check if the package can be built"""
    print("\n=== Testing Package Build ===")
    
    # Remove existing dist directory
    if os.path.exists('dist'):
        try:
            shutil.rmtree('dist')
            print("✓ Removed existing dist directory")
        except Exception as e:
            print(f"✗ Failed to remove dist directory: {e}")
            return False
    
    # Build the package
    try:
        subprocess.run([sys.executable, '-m', 'build'], check=True, capture_output=True)
        print("✓ Package built successfully")
        
        # Check if dist files were created
        wheel_files = [f for f in os.listdir('dist') if f.endswith('.whl')]
        tar_files = [f for f in os.listdir('dist') if f.endswith('.tar.gz')]
        
        if wheel_files:
            print(f"✓ Wheel file created: {wheel_files[0]}")
        else:
            print("✗ No wheel file created")
            return False
        
        if tar_files:
            print(f"✓ Source distribution created: {tar_files[0]}")
        else:
            print("✗ No source distribution created")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Failed to build package: {e}")
        return False

def check_github_actions():
    """Check if GitHub Actions are set up correctly"""
    print("\n=== Checking GitHub Actions ===")
    
    # Check tests workflow
    tests_workflow = os.path.join('.github', 'workflows', 'tests.yml')
    if os.path.exists(tests_workflow):
        print(f"✓ Tests workflow found: {tests_workflow}")
    else:
        print(f"✗ Tests workflow not found: {tests_workflow}")
    
    # Check release workflow
    release_workflow = os.path.join('.github', 'workflows', 'release.yml')
    if os.path.exists(release_workflow):
        # Check if it contains PyPI secrets reference
        with open(release_workflow, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}' in content and 'TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}' in content:
                print(f"✓ Release workflow found with PyPI secrets: {release_workflow}")
            else:
                print(f"✗ Release workflow found but PyPI secrets are not configured: {release_workflow}")
    else:
        print(f"✗ Release workflow not found: {release_workflow}")

def check_readme_documentation():
    """Check if the README contains necessary documentation"""
    print("\n=== Checking README Documentation ===")
    
    if not os.path.exists('README.md'):
        print("✗ README.md not found")
        return False
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key sections
    sections_to_check = [
        ('Installation instructions', r'##\s*Install|pip install|uv pip install'),
        ('Usage examples', r'##\s*(Usage|Quick Start)'),
        ('Features', r'##\s*Features'),
        ('API documentation', r'##\s*(API|API Usage)'),
        ('License', r'##\s*License'),
    ]
    
    all_sections = True
    for section_name, pattern in sections_to_check:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"✓ README contains {section_name}")
        else:
            print(f"✗ README is missing {section_name}")
            all_sections = False
    
    # Check for uv recommendations
    if 'uv pip install' in content or 'uv pip install simple-ssg' in content:
        print("✓ README recommends uv for installation")
    else:
        print("✗ README does not mention uv for installation")
        all_sections = False
    
    return all_sections

def main():
    """Main function"""
    print("Simple-SSG PyPI Publication Validation")
    print("=" * 40)
    
    # Change to the package directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working in directory: {script_dir}")
    
    # Track validation results
    is_valid = True
    
    # Check version consistency
    version_valid, version = check_version_consistency()
    is_valid = is_valid and version_valid
    
    # Check package metadata
    metadata_valid = check_package_metadata()
    is_valid = is_valid and metadata_valid
    
    # Check if package is on PyPI
    if version_valid:
        pypi_valid = check_pypi_existence('simple-ssg', version)
        is_valid = is_valid and pypi_valid
    
    # Check if package can be built
    build_valid = check_build_dist()
    is_valid = is_valid and build_valid
    
    # Check GitHub Actions
    check_github_actions()
    
    # Check README documentation
    readme_valid = check_readme_documentation()
    is_valid = is_valid and readme_valid
    
    # Print summary
    print("\n=== Publication Validation Summary ===")
    if is_valid:
        print("✅ SUCCESS: The package is ready to be published to PyPI!")
        print("\nTo publish to PyPI, you can:")
        print("1. Create a GitHub release (recommended) - This will trigger the GitHub Actions workflow")
        print("   - Go to https://github.com/bradyclarke/simple-ssg/releases/new")
        print("   - Create a new release with tag v" + (version if version else "0.1.0"))
        print("\nOr manually:")
        print("2. Use twine to upload to PyPI:")
        print("   python -m twine upload dist/*")
    else:
        print("❌ FAIL: The package is not ready to be published to PyPI.")
        print("Please fix the issues above before publishing.")
    
    return 0 if is_valid else 1

if __name__ == "__main__":
    sys.exit(main())
