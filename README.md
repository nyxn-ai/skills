# Markdown Organizer Skill (LLM-Enhanced)

This skill empowers an agent to manage Markdown articles by leveraging Large Language Models (LLM) for advanced semantic understanding, categorization, summarization, and even code generation. It transforms a collection of static documents into a dynamic, LLM-powered knowledge and creation assistant.

## Agent Environment Setup

To enable this skill, ensure the following Python packages are installed in the agent's execution environment:
```bash
python3 -m pip install markdown-it-py jinja2
```

## How the Agent Uses This Skill

This skill provides a set of actions that an agent can invoke to process Markdown content. For actions that generate an LLM prompt, the agent is expected to process that prompt using its own LLM capabilities and return the relevant output.

### Available Actions and Their Invocation Patterns

The agent will invoke specific internal scripts based on the task.

*   **`categorize`**:
    *   **Purpose**: Prepares an LLM prompt for categorizing a given Markdown article.
    *   **Agent's Role**: The agent receives an `llm_prompt`, processes it, and returns a comma-separated list of categories.
    *   **Inputs (to the skill)**:
        *   `file_path` (string, required): Path to the Markdown file.
        *   `categories_list` (list of strings, optional): Suggested categories to include in the prompt.
    *   **Internal Script**: `scripts/categorizer.py`

*   **`summarize`**:
    *   **Purpose**: Prepares an LLM prompt for summarizing a given Markdown article.
    *   **Agent's Role**: The agent receives an `llm_prompt`, processes it, and returns the summary text.
    *   **Inputs (to the skill)**:
        *   `file_path` (string, required): Path to the Markdown file.
    *   **Internal Script**: `scripts/summarizer.py`

*   **`generate_code`**:
    *   **Purpose**: Prepares an LLM prompt for generating code based on an article's description of an algorithm or concept.
    *   **Agent's Role**: The agent receives an `llm_prompt`, processes it, and returns the generated code.
    *   **Inputs (to the skill)**:
        *   `file_path` (string, required): Path to the Markdown file.
        *   `language` (string, optional): Target programming language (defaults to "Python").
    *   **Internal Script**: `scripts/code_generator.py`

*   **`organize`**:
    *   **Purpose**: Moves a specified article into a category-specific subdirectory.
    *   **Agent's Role**: The agent provides the necessary parameters to trigger file organization.
    *   **Inputs (to the skill)**:
        *   `file_path` (string, required): Current path to the Markdown file.
        *   `category` (string, required): The category determined for the file.
        *   `base_dir` (string, required): The root directory where categorized articles should be stored.
    *   **Internal Script**: `scripts/organizer.py`

*   **`generate_summary_file`**:
    *   **Purpose**: Creates a summary Markdown file for a given category, compiling titles, paths, and LLM-generated summaries of related articles.
    *   **Agent's Role**: The agent provides the collected article data and category information.
    *   **Inputs (to the skill)**:
        *   `articles_data` (list of dicts, required): Each dict: `{'title': '...', 'path': '...', 'summary': '...'}`.
        *   `category_name` (string, required): The name of the category for which to generate the summary file.
        *   `output_dir` (string, optional): Directory to save the summary file.
    *   **Internal Script**: `scripts/summarizer.py` (specifically, likely a function within it for file generation)

*   **`search`**:
    *   **Purpose**: Searches for content within the managed Markdown articles.
    *   **Agent's Role**: The agent provides a query to find relevant articles.
    *   **Inputs (to the skill)**:
        *   `query` (string, required): The search query.
        *   `dir_path` (string, optional): Directory to search within (defaults to all managed articles).
    *   **Internal Script**: `scripts/search_engine.py`

## Internal Scripts Overview

The skill utilizes the following Python scripts:
*   `scripts/markdown_parser.py`: Handles parsing Markdown content to extract plain text and headings.
*   `scripts/categorizer.py`: Orchestrates the creation of LLM prompts for article categorization.
*   `scripts/organizer.py`: Manages file system operations for moving and structuring categorized articles.
*   `scripts/summarizer.py`: Prepares LLM prompts for article summarization and generates formatted summary files using templates.
*   `scripts/search_engine.py`: Provides content search capabilities across Markdown articles.
*   `scripts/code_generator.py`: Sets up LLM prompts for generating code snippets from article content.

## Configuration & Resources

*   **`resources/category_keywords.json`**: Defines a list of `suggested_categories` that can be included in categorization prompts. This file is customizable for tailoring category suggestions.
*   **`resources/summary_template.md`**: A Jinja2 template used by the `summarizer.py` for structuring output summary Markdown files.

This README focuses on how an agent would interface with and utilize the `markdown-organizer` skill to effectively manage and process Markdown-based knowledge.

# Spec Manager Skill (API Specification Management)

This skill provides a comprehensive toolkit for AI Agents to interact with API specifications, fostering spec-driven development practices. It enables the agent to fetch, parse, validate, compare, and generate various artifacts from API specifications, as well as manage change proposals, implementation plans, and task breakdowns. It integrates concepts from OpenSpec and Spec Kit to offer a robust workflow for managing API specifications throughout their lifecycle.