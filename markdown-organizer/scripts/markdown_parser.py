# scripts/markdown_parser.py
from markdown_it import MarkdownIt
import os

def parse_markdown(file_path):
    """
    Parses a Markdown file and extracts its content, headings, and plain text.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        return {"error": f"Failed to read file {file_path}: {e}"}

    md = MarkdownIt()
    tokens = md.parse(md_content)

    plain_text_parts = []
    headings = []
    current_heading_level = 0
    current_heading_text = ""

    for token in tokens:
        if token.type == 'heading_open':
            current_heading_level = token.markup.count('#')
        elif token.type == 'inline' and token.children and tokens[tokens.index(token)-1].type == 'heading_open':
            current_heading_text = token.content
            headings.append({'level': current_heading_level, 'text': current_heading_text})
        elif token.type == 'text':
            plain_text_parts.append(token.content)
        elif token.type == 'paragraph_open':
            # Collect text within paragraphs
            pass
        elif token.type == 'fence': # Code blocks
            # Optionally include code blocks in plain text, or exclude
            plain_text_parts.append(f"\n```\n{token.content}\n```\n")
        # Add more token types if needed to extract specific content

    plain_text_content = " ".join(plain_text_parts).strip()
    
    return {
        "full_content": md_content,
        "plain_text": plain_text_content,
        "headings": headings,
        "title": headings[0]['text'] if headings else os.path.basename(file_path).replace('.md', '')
    }
