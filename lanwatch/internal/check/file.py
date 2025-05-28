import os
import logging

def path(file_path):
    """Create the path if it doesn't exist"""
    if file_path and not os.path.exists(file_path):
        dir_path = os.path.dirname(file_path)

        try:
            os.makedirs(dir_path, exist_ok=True)
            with open(file_path, 'w'):
                pass  # Create an empty file
            return False
        except OSError as e:
            logging.error(f"Error creating path: {e}")
            return False

    return True

def exists(file_path):
    """Check if a file exists"""
    return bool(file_path and os.path.exists(file_path))

def is_yaml(file_path):
    """Check if a file has a .yaml or .yml extension"""
    return exists(file_path) and os.path.splitext(file_path)[1] in {".yaml", ".yml"}

def is_empty(file_path):
    """Check if a file is empty"""
    return exists(file_path) and os.path.getsize(file_path) == 0
