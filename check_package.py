#!/usr/bin/env python3
"""
This script validates the Simple-SSG package structure and imports.
"""

import os
import sys
import subprocess
import importlib
import importlib.util
import argparse
import shutil

def check_package_structure():
    """Check the package directory structure"""
    print("\n=== Checking Package Structure ===")
    
    required_files = [
        'pyproject.toml',
        'setup.py',
        'LICENSE',
        'README.md',
        'simple_ssg/__init__.py',
        'simple_ssg/builder.py',
        'simple_ssg/cli.py',
        'simple_ssg/config.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ Found {file_path}")
        else:
            print(f"✗ Missing {file_path}")
    
    # Check for required directories
    required_dirs = [
        'simple_ssg/converters',
        'simple_ssg/enhancers',
        'simple_ssg/utils',
        'docs',
        'examples',
        'tests'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"✓ Found directory {dir_path}")
        else:
            print(f"✗ Missing directory {dir_path}")

def check_imports():
    """Check if all necessary imports work correctly"""
    print("\n=== Checking Imports ===")
    
    # Core modules to check
    modules_to_check = [
        'simple_ssg',
        'simple_ssg.builder',
        'simple_ssg.cli',
        'simple_ssg.config',
        'simple_ssg.converters.markdown',
        'simple_ssg.converters.html',
        'simple_ssg.enhancers.minifier',
        'simple_ssg.enhancers.seo',
        'simple_ssg.enhancers.server',
        'simple_ssg.utils.fs',
        'simple_ssg.utils.templates'
    ]
    
    for module_name in modules_to_check:
        try:
            module = importlib.import_module(module_name)
            print(f"✓ Successfully imported {module_name}")
        except ImportError as e:
            print(f"✗ Failed to import {module_name}: {str(e)}")

def check_external_dependencies():
    """Check if all required external dependencies are available"""
    print("\n=== Checking External Dependencies ===")
    
    # List of external dependencies
    dependencies = [
        'markdown',
        'yaml',  # Part of PyYAML
    ]
    
    for dependency in dependencies:
        # Handle the yaml special case
        if dependency == 'yaml':
            dep_name = 'PyYAML'
            import_name = 'yaml'
        else:
            dep_name = dependency
            import_name = dependency
        
        try:
            # Try to import the module
            importlib.import_module(import_name)
            print(f"✓ {dep_name} is installed")
        except ImportError:
            print(f"✗ {dep_name} is not installed")

def check_entry_point():
    """Check if the CLI entry point works"""
    print("\n=== Checking CLI Entry Point ===")
    
    try:
        # Try to run the CLI with --help
        result = subprocess.run([sys.executable, '-m', 'simple_ssg', '--version'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ CLI entry point works: {result.stdout.strip()}")
        else:
            print(f"✗ CLI entry point failed with code {result.returncode}")
            if result.stderr:
                print(f"  Error: {result.stderr.strip()}")
        
    except Exception as e:
        print(f"✗ Failed to run CLI entry point: {str(e)}")

def check_functionality():
    """Check if the core functionality works by building a simple site"""
    print("\n=== Checking Core Functionality ===")
    
    # Create a temporary test directory
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    try:
        # Create a minimal site structure
        content_dir = os.path.join(temp_dir, 'content')
        output_dir = os.path.join(temp_dir, 'build')
        os.makedirs(content_dir)
        
        # Create a test markdown file
        with open(os.path.join(content_dir, 'test.md'), 'w') as f:
            f.write("# Test Page\n\nThis is a test page.")
        
        # Create a simple template
        template_path = os.path.join(temp_dir, 'template.html')
        with open(template_path, 'w') as f:
            f.write('<!DOCTYPE html><html><head><title>Test</title></head><body><div id="content-container">Loading...</div></body></html>')
        
        # Try to build the site
        print("Attempting to build a simple test site...")
        from simple_ssg import build_site
        
        config = {
            'content_dir': content_dir,
            'template_path': template_path,
            'output_dir': output_dir,
            'static_dirs': []
        }
        
        result = build_site(config_dict=config)
        
        # Check if the build was successful
        if os.path.exists(os.path.join(output_dir, 'test.html')):
            print("✓ Successfully built a test site")
            print(f"  Processed {result.get('processed', 0)} files in {result.get('build_time', 0):.2f} seconds")
        else:
            print("✗ Failed to build the test site")
        
    except Exception as e:
        print(f"✗ Error during functionality test: {str(e)}")
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

def install_package():
    """Install the package in development mode"""
    print("\n=== Installing Package in Development Mode ===")
    
    try:
        # Check if uv is available
        if shutil.which('uv'):
            print("Using uv package manager (recommended)...")
            # Run uv pip install in development mode
            subprocess.run(['uv', 'pip', 'install', '-e', '.'], check=True)
        else:
            print("uv not found, falling back to pip...")
            # Run pip install in development mode
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', '.'], check=True)
        print("✓ Successfully installed package in development mode")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install package: {e}")
        sys.exit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Validate Simple-SSG package')
    parser.add_argument('--no-install', action='store_true', help='Skip installing the package')
    
    args = parser.parse_args()
    
    print("Simple-SSG Package Validation")
    print("=" * 30)
    
    # Change to the package directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working in directory: {script_dir}")
    
    # Check the package structure
    check_package_structure()
    
    # Install the package if not skipped
    if not args.no_install:
        install_package()
    
    # Check imports
    check_imports()
    
    # Check external dependencies
    check_external_dependencies()
    
    # Check entry point
    check_entry_point()
    
    # Check functionality
    check_functionality()
    
    print("\n=== Validation Complete ===")

if __name__ == "__main__":
    main()
