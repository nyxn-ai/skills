# scripts/summarizer.py
from jinja2 import Template
import os
from .markdown_parser import parse_markdown # Relative import

def summarize_content_llm_prompt(file_path):
    """
    Prepares a prompt for an LLM to summarize the given Markdown file.
    """
    parsed_data = parse_markdown(file_path)
    if "error" in parsed_data:
        return parsed_data

    plain_text = parsed_data.get("plain_text", "")
    title = parsed_data.get("title", os.path.basename(file_path))

    prompt = f"""
Please provide a concise and informative summary of the following Markdown article.
The summary should be about 3-5 sentences long and capture the main points of the article.

Article Title: {title}
---
Article Content:
{plain_text[:4000]} # Limit content for prompt length, adjust as needed.
---
Provide only the summary text as your response.
"""
    return {"llm_prompt": prompt, "file_path": file_path, "title": title}

def generate_summary_file(articles_data, category_name, template_path=None, output_dir="."):
    """
    Generates a summary Markdown file for a given category using a template.
    `articles_data` should be a list of dicts, each with 'title', 'path', and 'summary'.
    """
    if template_path is None:
        template_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'summary_template.md')

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except Exception as e:
        return {"error": f"Failed to read template file {template_path}: {e}"}

    template = Template(template_content)
    summary_content = template.render(category_name=category_name, articles=articles_data)
    
    summary_file_path = os.path.join(output_dir, f"{category_name}_summary.md")
    try:
        with open(summary_file_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        return {"summary_file_path": summary_file_path}
    except Exception as e:
        return {"error": f"Failed to write summary file {summary_file_path}: {e}"}
