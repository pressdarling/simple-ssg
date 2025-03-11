"""
File system utilities for Simple-SSG.
"""

import os
import shutil
import sys

def ensure_dir(directory):
    """
    Ensure a directory exists, creating it if necessary.
    
    Parameters:
    - directory: Path to the directory
    """
    if not directory:
        return
        
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            print(f"Error creating directory {directory}: {str(e)}")
            sys.exit(1)

def copy_static_assets(static_dirs, output_dir):
    """
    Copy static assets to the output directory.
    
    Parameters:
    - static_dirs: List of static directories to copy
    - output_dir: Output directory
    """
    for static_dir in static_dirs:
        if os.path.exists(static_dir):
            dir_name = os.path.basename(static_dir)
            try:
                output_path = os.path.join(output_dir, dir_name)
                if os.path.exists(output_path):
                    shutil.rmtree(output_path)
                shutil.copytree(static_dir, output_path)
                print(f"Copied {static_dir} to {output_path}")
            except Exception as e:
                print(f"Error copying {static_dir}: {str(e)}")
        else:
            print(f"Warning: Static directory {static_dir} does not exist. Skipping.")

def get_relative_path(path, base_path):
    """
    Get the path relative to the base path.
    
    Parameters:
    - path: Absolute path
    - base_path: Base path
    
    Returns:
    - Relative path
    """
    return os.path.relpath(path, base_path)

def list_files(directory, extensions=None):
    """
    List files in a directory with optional extension filtering.
    
    Parameters:
    - directory: Directory to list files from
    - extensions: List of extensions to filter by (e.g., ['.md', '.txt'])
    
    Returns:
    - List of file paths
    """
    file_list = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if extensions is None or any(file.endswith(ext) for ext in extensions):
                file_list.append(os.path.join(root, file))
    
    return file_list
