
#!/usr/bin/env python3
"""
Make Python scripts in the current directory executable.
"""

import os
import stat
import sys

def main():
    """Make Python scripts executable"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all Python scripts in the current directory
    python_scripts = []
    for filename in os.listdir(script_dir):
        filepath = os.path.join(script_dir, filename)
        if (filename.endswith('.py') and 
            os.path.isfile(filepath) and 
            not os.access(filepath, os.X_OK)):
            python_scripts.append(filepath)
    
    # Make each script executable
    for script in python_scripts:
        try:
            # Get current permissions
            current_permissions = os.stat(script).st_mode
            
            # Add executable permissions (equivalent to chmod +x)
            new_permissions = current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            
            # Set new permissions
            os.chmod(script, new_permissions)
            print(f"Made executable: {os.path.basename(script)}")
        except Exception as e:
            print(f"Error making {os.path.basename(script)} executable: {e}")
    
    if not python_scripts:
        print("No non-executable Python scripts found.")
    else:
        print(f"Made {len(python_scripts)} scripts executable.")

if __name__ == "__main__":
    main()
