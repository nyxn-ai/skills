# scripts/categorizer.py
import json
import os
from .markdown_parser import parse_markdown # Relative import

def categorize_content_llm_prompt(file_path, categories_list=None):
    """
    Prepares a prompt for an LLM to categorize the given Markdown file.
    """
    parsed_data = parse_markdown(file_path)
    if "error" in parsed_data:
        return parsed_data

    plain_text = parsed_data.get("plain_text", "")
    title = parsed_data.get("title", os.path.basename(file_path))

    if not categories_list:
        # Load default suggested categories (assuming it's in the same skill's resources)
        # In a real scenario, this would use a more robust path
        try:
            with open(os.path.join(os.path.dirname(__file__), '..', 'resources', 'category_keywords.json'), 'r', encoding='utf-8') as f:
                config = json.load(f)
                categories_list = config.get("suggested_categories", [])
        except Exception as e:
            categories_list = [] # Fallback

    categories_str = ", ".join(categories_list) if categories_list else "General, Uncategorized"

    prompt = f"""
Please categorize the following Markdown article based on its content.
Provide up to 3 most relevant categories from the following list, or suggest new ones if none are suitable.
The categories should be concise (1-3 words) and descriptive.

Suggested Categories: {categories_str}

Article Title: {title}
---
Article Content:
{plain_text[:2000]} # Limit content for prompt length, adjust as needed.
---
Provide your response as a comma-separated list of categories, for example: "Machine Learning, Deep Learning".
"""
    return {"llm_prompt": prompt, "file_path": file_path, "title": title}

# The actual categorization logic will be handled by the agent (LLM) after receiving this prompt.
# This script prepares the input for the LLM.
