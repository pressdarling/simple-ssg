
#!/usr/bin/env python3

import subprocess
import sys
import os
import shutil

# Try to install the package in development mode
try:
    print("Installing package in development mode...")
    if shutil.which('uv'):
        print("Using uv (recommended)...")
        subprocess.run(['uv', 'pip', 'install', '-e', '.'], check=True)
    else:
        print("uv not found, falling back to pip...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', '.'], check=True)
    print("Installation successful")
except subprocess.CalledProcessError as e:
    print(f"Installation failed: {e}")
    sys.exit(1)

# Try to import the package
try:
    print("Importing package...")
    import simple_ssg
    print(f"Import successful. Version: {simple_ssg.__version__}")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

# Check for any obvious import issues with main modules
modules_to_check = [
    'simple_ssg.builder',
    'simple_ssg.cli',
    'simple_ssg.config',
    'simple_ssg.converters.markdown',
    'simple_ssg.enhancers.server',
    'simple_ssg.utils.templates'
]

print("Checking main module imports...")
for module in modules_to_check:
    try:
        exec(f"import {module}")
        print(f"  ✓ {module}")
    except ImportError as e:
        print(f"  ✗ {module}: {e}")
