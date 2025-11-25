---
name: markdown-organizer
description: A skill to read, organize, categorize, and summarize Markdown articles using LLM for semantic understanding, facilitating knowledge management.
---

# Markdown Organizer Skill (LLM-Enhanced)

This skill helps in managing a collection of Markdown articles by leveraging Large Language Models (LLM) for semantic understanding, categorization, and summarization.

## Prerequisites

*   **Python Package**: Ensure `markdown-it-py` is installed in your environment (`pip install markdown-it-py`).

## How to Use

When invoked with a task related to organizing or summarizing Markdown content, this skill will prepare prompts for an LLM (such as myself) to process the content.

1.  **Input Source**:
    *   A `dir_path` pointing to a directory containing Markdown files (`.md`).
    *   A `file_path` pointing to a specific Markdown file.

2.  **Task Specification**: The prompt should clearly indicate the desired action:

    *   **`categorize`**:
        *   **Action**: Calls `scripts/categorizer.py` which will return a dictionary containing an `llm_prompt` for categorization.
        *   **User/Agent Role**: You (the agent) will read this `llm_prompt` and provide the categories as a comma-separated list.
        *   **(Optional) `categories_list`**: You can pass a list of suggested categories to the script, which will be included in the prompt. If not provided, a default list from `resources/category_keywords.json` will be used.

    *   **`summarize`**:
        *   **Action**: Calls `scripts/summarizer.py` which will return a dictionary containing an `llm_prompt` for summarization.
        *   **User/Agent Role**: You (the agent) will read this `llm_prompt` and provide the summary text.

    *   **`organize`**:
        *   **Action**: Requires prior categorization. Once categories are determined (e.g., by the LLM), this action calls `scripts/organizer.py` to move files into category-specific subdirectories.
        *   **Input**: Requires the `file_path` and the determined `category`.

    *   **`generate_summary_file`**:
        *   **Action**: Creates a summary Markdown file based on a list of article data (titles, paths, and their LLM-generated summaries).
        *   **Input**: Requires `articles_data` (list of dicts: `{'title': '...', 'path': '...', 'summary': '...'}`), `category_name`, and optionally `output_dir`.

    *   **`search`**:
        *   **Action**: Calls `scripts/search_engine.py` to search for content within the managed Markdown articles (currently keyword-based).

    *   **`generate_code`**:
        *   **Action**: Calls `scripts/code_generator.py` which will return a dictionary containing an `llm_prompt` for code generation.
        *   **User/Agent Role**: You (the agent) will read this `llm_prompt` and provide the generated code.
        *   **Input**: Requires `file_path` and optionally `language` (defaults to "Python").

## Resources

*   `resources/category_keywords.json`: Contains a list of `suggested_categories` for the LLM to consider during categorization. This list can be customized.
*   `resources/summary_template.md`: A Jinja2 template used by `summarizer.py` to format the final summary Markdown file.

## Scripts

*   `scripts/markdown_parser.py`: Parses Markdown files, extracting plain text content and headings for LLM processing.
*   `scripts/categorizer.py`: Prepares an LLM prompt for categorizing an article based on its content.
*   `scripts/organizer.py`: Handles file system operations to move categorized articles into designated directories.
*   `scripts/summarizer.py`: Prepares an LLM prompt for summarizing an article and formats category summary files.
*   `scripts/search_engine.py`: Provides keyword-based search functionality across Markdown articles.
*   `scripts/code_generator.py`: Sets up LLM prompts for generating code snippets from article content.

## Example Invocation (Conceptual)

Let's say you want to categorize and summarize a file `/path/to/my_article.md`:

1.  **Get Categorization Prompt**:
    ```python
    # This would be an internal call by the agent
    from scripts.categorizer import categorize_content_llm_prompt
    result = categorize_content_llm_prompt(file_path="/path/to/my_article.md")
    # result will contain {'llm_prompt': "Please categorize...", 'file_path': '...', 'title': '...'}
    print(result['llm_prompt'])
    ```
    **Agent's Response (example)**: "Machine Learning, Neural Networks"

2.  **Get Summarization Prompt**:
    ```python
    # This would be an internal call by the agent
    from scripts.summarizer import summarize_content_llm_prompt
    result = summarize_content_llm_prompt(file_path="/path/to/my_article.md")
    # result will contain {'llm_prompt': "Please provide a concise...", 'file_path': '...', 'title': '...'}
    print(result['llm_prompt'])
    ```
    **Agent's Response (example)**: "This article introduces..."

3.  **Organize File (after categorization)**:
    ```python
    # This would be an internal call by the agent based on the categorization
    from scripts.organizer import organize_files
    new_path = organize_files(file_path="/path/to/my_article.md", category="Machine Learning", base_dir="/path/to/organized_articles")
    # new_path might be "/path/to/organized_articles/Machine Learning/my_article.md"
    ```

4.  **Generate Code**:
    ```python
    # This would be an internal call by the agent based on the article content
    from scripts.code_generator import generate_code_llm_prompt
    result = generate_code_llm_prompt(file_path="/path/to/my_algorithm_article.md", language="Python")
    # result will contain {'llm_prompt': "Based on the following...", 'file_path': '...', 'title': '...', 'language': 'Python'}
    print(result['llm_prompt'])
    ```
    **Agent's Response (example)**:
    ```python
    # Generated Python code for the algorithm described in the article
    def my_algorithm(...):
        # ... implementation ...
    ```