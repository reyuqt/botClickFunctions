import os

def get_folder_structure_os(path: str) -> str:
    """
    Returns the folder structure of the given path as a string using the os module.

    Args:
        path (str): The root directory path.

    Returns:
        str: A string representation of the folder structure.
    """
    tree_str = ""
    for root, dirs, files in os.walk(path):
        # Calculate the depth by counting separators
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * level
        tree_str += f"{indent}{os.path.basename(root)}/\n"
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            if '.git' in f or 'cache' in f:
                continue
            tree_str += f"{sub_indent}{f}\n"
    return tree_str
