
#!/usr/bin/env python3
"""
Run code quality checks on the Simple-SSG codebase.
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n=== {description} ===")
    try:
        # If command is a string, convert to list
        if isinstance(command, str):
            command = command.split()
        
        # Ensure we're running Python scripts with python
        if command[0].endswith('.py'):
            command = [sys.executable] + command
            
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✓ {description} successful")
        if result.stdout:
            print("\nOutput:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with code {e.returncode}")
        if e.stdout:
            print("\nOutput:")
            print(e.stdout)
        if e.stderr:
            print("\nErrors:")
            print(e.stderr)
        return False

def main():
    """Run all code quality checks"""
    all_passed = True
    
    # Change to the project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run package checks first
    pkg_check_result = run_command('check_package.py', "Package Structure Check")
    all_passed = all_passed and pkg_check_result
    
    # Check if Python packages are installed properly
    pkg_import_result = run_command('check_imports.py', "Package Import Check")
    all_passed = all_passed and pkg_import_result
    
    # Run ruff check
    if shutil.which('ruff'):
        ruff_result = run_command(['ruff', 'check', 'simple_ssg'], "Ruff Check")
        all_passed = all_passed and ruff_result
    else:
        print("✗ ruff not found. Please install it with: uv pip install ruff")
        run_command(f"{sys.executable} -m pip install ruff", "Installing ruff")
        ruff_result = run_command(['ruff', 'check', 'simple_ssg'], "Ruff Check (retry)")
        all_passed = all_passed and ruff_result
    
    # Run pytest
    if shutil.which('pytest'):
        pytest_result = run_command(['pytest'], "PyTest")
        all_passed = all_passed and pytest_result
    else:
        print("✗ pytest not found. Please install it with: uv pip install pytest")
        run_command(f"{sys.executable} -m pip install pytest", "Installing pytest")
        pytest_result = run_command(['pytest'], "PyTest (retry)")
        all_passed = all_passed and pytest_result
    
    # Print summary
    print("\n=== Code Quality Check Summary ===")
    if all_passed:
        print("✓ All checks passed! The code is ready for publication.")
    else:
        print("✗ Some checks failed. Please fix the issues before publishing.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
