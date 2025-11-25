# scripts/search_engine.py
import os
import glob

def search_articles(query, base_dir):
    """
    Searches for the query within Markdown files in the specified base directory.
    This is a simple placeholder for a more sophisticated search.
    """
    results = []
    markdown_files = glob.glob(os.path.join(base_dir, '**', '*.md'), recursive=True)

    for file_path in markdown_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if query.lower() in content.lower():
                results.append(file_path)
    return results
