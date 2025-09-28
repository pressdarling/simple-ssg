"""File system utilities for Simple-SSG.

This module provides a collection of helper functions for performing common
filesystem operations required by the static site generator. These operations
include creating directories, copying static assets, and listing files.
"""

import os
import shutil
import sys
from typing import List, Optional


def ensure_dir(directory: str) -> None:
    """Ensures that a directory exists, creating it if necessary.

    If the specified directory path does not exist, this function will attempt
    to create it, including any necessary parent directories.

    Args:
        directory: The path to the directory to check and create.

    Raises:
        SystemExit: If the directory cannot be created due to an OS-level error.
    """
    if not directory:
        return

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            print(f"Error creating directory {directory}: {str(e)}")
            sys.exit(1)


def copy_static_assets(static_dirs: List[str], output_dir: str) -> None:
    """Copies static asset directories to the output directory.

    This function iterates through a list of source directories (e.g., 'css',
    'images') and copies them into the specified output directory. If a
    destination directory already exists, it is removed before copying to
    ensure a clean state.

    Args:
        static_dirs: A list of paths to the static directories to be copied.
        output_dir: The path to the destination directory where the static
                    assets will be placed.
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


def get_relative_path(path: str, base_path: str) -> str:
    """Calculates the relative path of a file or directory from a base path.

    Args:
        path: The absolute path of the file or directory.
        base_path: The base path from which the relative path should be
                   calculated.

    Returns:
        A string representing the relative path.
    """
    return os.path.relpath(path, base_path)


def list_files(directory: str, extensions: Optional[List[str]] = None) -> List[str]:
    """Lists all files in a directory, with optional extension filtering.

    This function recursively walks through a directory and returns a list of
    paths to all files it contains. If the `extensions` argument is provided,
    only files with matching extensions will be included in the result.

    Args:
        directory: The path to the directory to search.
        extensions: An optional list of file extensions to filter by
                    (e.g., ['.md', '.html']).

    Returns:
        A list of full paths to the files.
    """
    file_list = []

    for root, _, files in os.walk(directory):
        for file in files:
            if extensions is None or any(file.endswith(ext) for ext in extensions):
                file_list.append(os.path.join(root, file))

    return file_list
