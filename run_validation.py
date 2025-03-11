
#!/usr/bin/env python3
import os
import sys
import subprocess

def main():
    # Run the package validation script
    result = subprocess.run(
        [sys.executable, 'check_package.py'], 
        capture_output=True, 
        text=True
    )
    
    # Write the output to a file
    with open('validation_results.txt', 'w') as f:
        f.write(result.stdout)
        if result.stderr:
            f.write("\n\nSTDERR:\n")
            f.write(result.stderr)
    
    # Print a message
    print(f"Validation complete. Results saved to validation_results.txt")
    
    # Return the exit code
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
