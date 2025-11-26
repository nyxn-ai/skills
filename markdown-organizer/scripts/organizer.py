# scripts/organizer.py
import os
import shutil

def organize_files(file_path: str, category: str, base_dir: str) -> str:
    """
    Organizes a Markdown file into a category-specific subdirectory.

    If a file with the same name already exists in the destination,
    it renames the file being moved to avoid overwriting (e.g., 'file.md' -> 'file (1).md').
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Source file not found: {file_path}")

    category_dir = os.path.join(base_dir, category)
    os.makedirs(category_dir, exist_ok=True)

    file_name = os.path.basename(file_path)
    new_file_path = os.path.join(category_dir, file_name)

    # Prevent overwriting
    counter = 1
    while os.path.exists(new_file_path):
        name, extension = os.path.splitext(file_name)
        new_file_name = f"{name} ({counter}){extension}"
        new_file_path = os.path.join(category_dir, new_file_name)
        counter += 1

    try:
        shutil.move(file_path, new_file_path)
        return new_file_path
    except Exception as e:
        # Re-raise with a more informative message
        raise IOError(f"Failed to move file from {file_path} to {new_file_path}: {e}")
