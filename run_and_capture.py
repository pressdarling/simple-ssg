
#!/usr/bin/env python3
import os
import sys
import subprocess

# Change to the package directory to make sure imports work
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Required files check
print("=== Checking Package Structure ===")
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

# Required directories check
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

# Install package
print("\n=== Installing Package in Development Mode ===")
try:
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '-e', '.'],
        capture_output=True,
        text=True,
        check=True
    )
    print("✓ Installation succeeded")
except subprocess.CalledProcessError as e:
    print(f"✗ Installation failed: {e}")
    print(f"Error output: {e.stderr}")
    sys.exit(1)

# Try importing the package
print("\n=== Basic Import Test ===")
try:
    import simple_ssg
    print(f"✓ Successfully imported simple_ssg version {simple_ssg.__version__}")
except ImportError as e:
    print(f"✗ Failed to import simple_ssg: {e}")
    sys.exit(1)

# Save results to file
print("\n=== Tests Complete ===")
print("Saving full test results to validation_results.txt")
with open('validation_results.txt', 'w') as f:
    f.write("Simple-SSG Package Validation Results\n")
    f.write("====================================\n\n")
    
    # Try to import key modules and report results
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
    
    f.write("=== Module Import Tests ===\n")
    import importlib
    for module_name in modules_to_check:
        try:
            module = importlib.import_module(module_name)
            f.write(f"✓ Successfully imported {module_name}\n")
        except ImportError as e:
            f.write(f"✗ Failed to import {module_name}: {str(e)}\n")
    
    # Check dependencies
    f.write("\n=== External Dependencies ===\n")
    dependencies = ['markdown', 'yaml']
    
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            f.write(f"✓ {dep} is installed\n")
        except ImportError:
            f.write(f"✗ {dep} is not installed\n")
    
    # Check CLI
    f.write("\n=== CLI Test ===\n")
    try:
        cli_result = subprocess.run(
            [sys.executable, '-m', 'simple_ssg', '--version'],
            capture_output=True,
            text=True
        )
        if cli_result.returncode == 0:
            f.write(f"✓ CLI test successful: {cli_result.stdout.strip()}\n")
        else:
            f.write(f"✗ CLI test failed with code {cli_result.returncode}\n")
            f.write(f"Error: {cli_result.stderr}\n")
    except Exception as e:
        f.write(f"✗ CLI test failed with exception: {str(e)}\n")

print("Tests complete. Check validation_results.txt for detailed results.")
