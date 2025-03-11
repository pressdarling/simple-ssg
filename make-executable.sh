#!/bin/bash
# Set execute permissions on shell scripts and Python scripts

echo "Setting execution permissions for scripts..."

# Make Python scripts executable
PYTHON_SCRIPTS=$(find . -type f -name "*.py" | grep -v "node_modules" | grep -v ".git")

# Make each script executable
for script in $PYTHON_SCRIPTS; do
    if [ -f "$script" ]; then
        chmod +x "$script"
        echo "Made executable: $script"
    fi
done

# Make shell scripts executable
SHELL_SCRIPTS=$(find . -type f -name "*.sh" | grep -v "node_modules" | grep -v ".git")

# Make each script executable
for script in $SHELL_SCRIPTS; do
    if [ -f "$script" ]; then
        chmod +x "$script"
        echo "Made executable: $script"
    fi
done

echo "Done! All scripts now have execution permissions."
