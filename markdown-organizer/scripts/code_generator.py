# scripts/code_generator.py
import os
from .markdown_parser import parse_markdown # Relative import

def generate_code_llm_prompt(file_path, language="Python"):
    """
    Prepares a prompt for an LLM to generate code based on the given Markdown article.
    """
    parsed_data = parse_markdown(file_path)
    if "error" in parsed_data:
        return parsed_data

    plain_text = parsed_data.get("plain_text", "")
    title = parsed_data.get("title", os.path.basename(file_path))

    prompt = f"""
Based on the following Markdown article, please generate a complete and professional code implementation of the described algorithm or concept.
The code should be in {language} and include necessary imports, clear function definitions, comments where appropriate, and a simple example usage if applicable.
Focus on correctness and readability.

Article Title: {title}
---
Article Content:
{plain_text[:8000]} # Limit content for prompt length, adjust as needed.
---
Please provide only the code block.
"""
    return {"llm_prompt": prompt, "file_path": file_path, "title": title, "language": language}
