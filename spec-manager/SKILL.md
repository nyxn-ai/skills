---
name: spec-manager
description: A skill to manage, analyze, validate, and generate content related to API specifications. It supports spec-driven development workflows, enabling AI Agents to better understand and operate with API interfaces, and assist in generating code, documentation, or tests.
---

# Spec Manager Skill (API Specification Management)

This skill provides a comprehensive toolkit for AI Agents to interact with API specifications, fostering spec-driven development practices. It enables the agent to fetch, parse, validate, compare, and generate various artifacts from API specifications, as well as manage change proposals.

## Actions

### `init_spec_project`
*   **Purpose**: Initializes a project for spec-driven development, setting up the required directory structure and foundational files.
*   **Inputs**:
    *   `project_root` (string, required): The root directory of the project to initialize.
*   **Outputs**:
    *   `success` (boolean): `true` if initialization was successful, `false` otherwise.
    *   `message` (string, optional): A success or error message.

### `define_principles`
*   **Purpose**: Allows the user to define or update the project's governing principles and development guidelines.
*   **Inputs**:
    *   `principles_content` (string, required): The content of the principles (Markdown format).
    *   `project_root` (string, required): The root directory of the project where `openspec/` is located.
*   **Outputs**:
    *   `success` (boolean): `true` if principles were successfully defined/updated, `false` otherwise.
    *   `message` (string, optional): A success or error message.

### `fetch_spec`
*   **Purpose**: Fetches API specification content from a local file path or a remote URL.
*   **Inputs**:
    *   `source_path` (string, required): The file path or URL to the API specification.
    *   `spec_format` (string, optional): The format of the specification (e.g., "OpenAPI", "Swagger", "AsyncAPI"). If not provided, the skill will attempt to infer it.
*   **Outputs**:
    *   `spec_content` (string): The content of the specification as a string.
    *   `error` (string, optional): An error message if fetching fails.

### `parse_spec`
*   **Purpose**: Parses the given API specification content and extracts key information such as endpoints, methods, request/response models, and security definitions.
*   **Inputs**:
    *   `spec_content` (string, required): The content of the API specification.
    *   `spec_format` (string, optional): The format of the specification.
*   **Outputs**:
    *   `parsed_data` (object): A structured representation (e.g., Python dictionary) of the specification's key elements.
    *   `error` (string, optional): An error message if parsing fails.

### `validate_spec`
*   **Purpose**: Validates the API specification against its standard (e.g., OpenAPI Specification) for correctness and consistency.
*   **Inputs**:
    *   `spec_content` (string, required): The content of the API specification.
    *   `spec_format` (string, optional): The format of the specification.
*   **Outputs**:
    *   `is_valid` (boolean): `true` if the specification is valid, `false` otherwise.
    *   `validation_messages` (list of strings, optional): Detailed error or warning messages.

### `generate_code_from_spec`
*   **Purpose**: Generates client SDKs, server stubs, data models, or controller code based on the API specification.
*   **Inputs**:
    *   `spec_content` (string, required): The content of the API specification.
    *   `target_language` (string, required): The programming language for code generation (e.g., "Python", "TypeScript", "Java").
    *   `code_type` (string, optional): The type of code to generate (e.g., "client", "server-stub", "models"). Defaults to "client".
    *   `output_dir` (string, optional): The directory where the generated code should be saved. Defaults to a temporary directory.
*   **Outputs**:
    *   `llm_prompt` (string): A prompt for the AI Agent to perform the actual code generation, detailing the context and requirements.
    *   `output_path` (string, optional): The path to the generated code files (if skill generates directly).
    *   `error` (string, optional): An error message if generation setup fails.

### `generate_docs_from_spec`
*   **Purpose**: Generates developer documentation or API reference pages from the API specification.
*   **Inputs**:
    *   `spec_content` (string, required): The content of the API specification.
    *   `doc_format` (string, optional): The format of the documentation (e.g., "Markdown", "HTML"). Defaults to "Markdown".
    *   `output_dir` (string, optional): The directory where the generated documentation should be saved. Defaults to a temporary directory.
*   **Outputs**:
    *   `llm_prompt` (string): A prompt for the AI Agent to perform the actual documentation generation.
    *   `output_path` (string, optional): The path to the generated documentation files.
    *   `error` (string, optional): An error message if generation setup fails.

### `compare_specs`
*   **Purpose**: Compares two API specifications (or different versions of the same spec) to identify differences (added, modified, or removed endpoints/models).
*   **Inputs**:
    *   `spec_content_a` (string, required): The content of the first API specification.
    *   `spec_content_b` (string, required): The content of the second API specification.
    *   `spec_format` (string, optional): The format of the specifications.
*   **Outputs**:
    *   `diff_report` (object): A structured report detailing the differences.
    *   `error` (string, optional): An error message if comparison fails.

### `create_change_proposal`
*   **Purpose**: Assists the AI Agent in creating structured API specification change proposals, including proposed changes, task lists, and spec deltas.
*   **Inputs**:
    *   `proposed_changes_description` (string, required): A natural language description of the proposed changes.
    *   `original_spec_content` (string, optional): The content of the original API specification, if available for diffing.
    *   `output_dir` (string, optional): The directory to create the proposal files.
*   **Outputs**:
    *   `llm_prompt` (string): A prompt for the AI Agent to generate the actual proposal files (e.g., `proposal.md`, `tasks.md`, `spec_deltas`).
    *   `proposal_path` (string, optional): The path to the created proposal directory.
    *   `error` (string, optional): An error message if proposal setup fails.

### `generate_plan`
*   **Purpose**: Generates a high-level technical implementation plan based on a given spec delta and project principles.
*   **Inputs**:
    *   `change_id` (string, required): The identifier of the change proposal.
    *   `project_root` (string, required): The root directory of the project where `openspec/` is located.
*   **Outputs**:
    *   `llm_prompt` (string): A prompt for the AI Agent to perform the actual plan generation.
    *   `plan_path` (string, optional): The path to the generated plan file.
    *   `error` (string, optional): An error message if generation setup fails.

### `breakdown_tasks`
*   **Purpose**: Refines the implementation plan into a detailed, actionable task list.
*   **Inputs**:
    *   `change_id` (string, required): The identifier of the change proposal.
    *   `project_root` (string, required): The root directory of the project where `openspec/` is located.
*   **Outputs**:
    *   `llm_prompt` (string): A prompt for the AI Agent to perform the actual task breakdown.
    *   `tasks_path` (string, optional): The path to the generated tasks file.
    *   `error` (string, optional): An error message if breakdown setup fails.

### `archive_change_proposal`
*   **Purpose**: Merges approved specification changes from a proposal into the main specification and archives the change files.
*   **Inputs**:
    *   `change_id` (string, required): The identifier of the change proposal to archive.
    *   `base_dir` (string, required): The base directory where the change proposal is located.
*   **Outputs**:
    *   `success` (boolean): `true` if archiving was successful, `false` otherwise.
    *   `message` (string, optional): A success or error message.
    *   `updated_main_spec_path` (string, optional): The path to the updated main specification.

## Implementation Details

This skill utilizes Python scripts in the `scripts/` directory for its functionalities.

*   `project_initializer.py`: Implements `init_spec_project` and `define_principles`.
*   `spec_proposal_manager.py`: Implements `create_change_proposal` and `archive_change_proposal`.
*   `spec_planner.py`: Implements `generate_plan` and `breakdown_tasks`.
*   Other scripts (e.g., `spec_parser.py`, `spec_validator.py`, `code_generator.py`, `doc_generator.py`, `spec_comparer.py`, `spec_fetcher.py`, `change_manager.py`): Implement the remaining tasks (`fetch_spec`, `parse_spec`, `validate_spec`, `generate_code_from_spec`, `generate_docs_from_spec`, `compare_specs`).

Templates for code and documentation generation are located in the `resources/templates/` directory.

## Prerequisites

Python 3.9+ and pip are required. Specific Python package dependencies will be managed within the skill's Python environment.

## Resources

*   `resources/config.json`: General skill configuration.
*   `resources/templates/code_generation/`: Templates for code generation.
*   `resources/templates/docs_generation/`: Templates for documentation generation.

