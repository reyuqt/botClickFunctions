import os
import re
from typing import List


def get_folder_structure_os(path: str, ignore_patterns: List[str] = None) -> str:
    """
    Returns the folder structure of the given path as a string using the os module,
    while ignoring directories that match any of the provided regex patterns.

    Args:
        path (str): The root directory path.
        ignore_patterns (List[str], optional): A list of regex patterns to ignore directories. Defaults to None.

    Returns:
        str: A string representation of the folder structure.
    """
    tree_str = ""

    # Compile regex patterns for efficiency
    compiled_patterns = [re.compile(pattern) for pattern in ignore_patterns] if ignore_patterns else []

    for root, dirs, files in os.walk(path):
        # Modify dirs in-place to remove ignored directories
        if compiled_patterns:
            original_dirs = dirs.copy()
            dirs[:] = [d for d in dirs if not any(pattern.search(d) for pattern in compiled_patterns)]
            ignored_dirs = set(original_dirs) - set(dirs)
            if ignored_dirs:
                print(f"Ignored directories in '{root}': {', '.join(ignored_dirs)}")

        # Calculate the depth by counting separators
        relative_path = os.path.relpath(root, path)
        if relative_path == '.':
            level = 0
        else:
            level = relative_path.count(os.sep)
        indent = ' ' * 4 * level
        tree_str += f"{indent}{os.path.basename(root)}/\n"
        sub_indent = ' ' * 4 * (level + 1)

        for f in files:
            # Skip files containing '.git' or 'cache'
            if '.git' in f or 'cache' in f:
                continue
            tree_str += f"{sub_indent}{f}\n"

    return tree_str
