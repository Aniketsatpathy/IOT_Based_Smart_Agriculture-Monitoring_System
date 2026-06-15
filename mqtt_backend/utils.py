import os
from datetime import datetime

def ensure_directory_exists(path: str):
    """
    Ensures that the directory for the given path exists.
    If the path is a file, it creates the parent directory.
    """
    if not path:
        return
    directory = os.path.dirname(path) if "." in os.path.basename(path) else path
    if directory:
        os.makedirs(directory, exist_ok=True)

def get_current_timestamp() -> str:
    """
    Returns the current timestamp in YYYY-MM-DD HH:MM:SS format.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_current_date() -> str:
    """
    Returns the current date in YYYY-MM-DD format.
    """
    return datetime.now().strftime("%Y-%m-%d")
