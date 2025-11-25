# scripts/organizer.py
import os

def organize_files(file_path, category, base_dir):
    """
    Organizes a Markdown file into a category-specific subdirectory.
    """
    category_dir = os.path.join(base_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    
    file_name = os.path.basename(file_path)
    new_file_path = os.path.join(category_dir, file_name)
    
    os.rename(file_path, new_file_path)
    return new_file_path
