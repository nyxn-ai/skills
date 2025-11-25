# Spec Manager: Empowering AI Agents with API Specification Intelligence

The `spec-manager` skill equips AI Agents with advanced capabilities to interact with and leverage API specifications (like OpenAPI, Swagger, AsyncAPI). It streamlines spec-driven development workflows, enabling Agents to understand, validate, compare, and generate artifacts from API definitions.

## Key Features

*   **Universal Spec Handling**: Fetch and parse API specifications from various sources (local files, URLs) and formats.
*   **Intelligent Validation**: Automatically validate specifications against industry standards for correctness and consistency.
*   **Code Generation**: Assist Agents in generating client SDKs, server stubs, data models, and more, directly from specs.
*   **Documentation Automation**: Facilitate the creation of comprehensive API documentation.
*   **Spec Comparison**: Identify and report differences between API specification versions.
*   **Change Management**: Support structured workflows for creating and archiving API specification change proposals, inspired by best practices in spec-driven development.

## How an AI Agent Uses This Skill

This skill acts as an interface, allowing AI Agents to perform complex operations on API specifications through a set of defined actions. For actions that require creative generation (e.g., code, documentation, change proposals), the skill will often prepare a detailed `llm_prompt` for the Agent to process using its own Large Language Model (LLM) capabilities.

### Agent Actions Overview

| Action                      | Description                                                                    | Agent's Role                                                                                                                                                                                                                           |
| :-------------------------- | :----------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fetch_spec`                | Retrieve API specification content.                                            | Provides `source_path`.                                                                                                                                                                                                                |
| `parse_spec`                | Extract structured data from a given API spec.                                 | Provides `spec_content`.                                                                                                                                                                                                               |
| `validate_spec`             | Verify the compliance and correctness of an API spec.                          | Provides `spec_content`.                                                                                                                                                                                                               |
| `generate_code_from_spec`   | Generate code (SDKs, stubs, models) based on a spec.                           | Provides `spec_content`, `target_language`, and `code_type`. **Processes `llm_prompt` to generate actual code.**                                                                                                                      |
| `generate_docs_from_spec`   | Produce documentation (reference, guides) from a spec.                         | Provides `spec_content`, `doc_format`. **Processes `llm_prompt` to generate actual documentation.**                                                                                                                                    |
| `compare_specs`             | Highlight differences between two API specifications.                          | Provides `spec_content_a` and `spec_content_b`.                                                                                                                                                                                        |
| `create_change_proposal`    | Initiate a structured proposal for API spec modifications.                     | Provides `proposed_changes_description` and optionally `original_spec_content`. **Processes `llm_prompt` to draft proposal documents.**                                                                                                |
| `archive_change_proposal`   | Finalize and integrate approved spec changes into the main definition.         | Provides `change_id` and `base_dir`.                                                                                                                                                                                                   |

## Installation & Prerequisites

To enable the `spec-manager` skill in your AI Agent's environment:

1.  **Python**: Ensure Python 3.9+ is installed.
2.  **Dependencies**: Install necessary Python packages. This skill will primarily use libraries like `requests` (for `fetch_spec`), `pyyaml`, `jsonschema` (for `validate_spec`), and potentially OpenAPI/Swagger-specific parsers. A `requirements.txt` will be provided for easy installation.
3.  **Skill Integration**: Follow your AI Agent's specific instructions for integrating new skills (e.g., placing the `spec-manager` directory in a designated `skills/` folder).

## Directory Structure

```
spec-manager/
├── SKILL.md                  // Skill definition for the AI Agent
├── README.md                 // Human-readable documentation for the skill
├── resources/                // Templates, configurations, schemas
│   ├── config.json
│   ├── schemas/              // e.g., openapi_v3.json for validation
│   ├── templates/
│   │   ├── code_generation/
│   │   │   └── python/
│   │   │       └── client.j2 // Jinja2 template for Python client code
│   │   └── docs_generation/
│   │       └── markdown.j2   // Jinja2 template for Markdown docs
└── scripts/                  // Python scripts implementing skill actions
    ├── __init__.py
    ├── spec_fetcher.py       // Implements fetch_spec
    ├── spec_parser.py        // Implements parse_spec
    ├── spec_validator.py     // Implements validate_spec
    ├── code_generator.py     // Implements generate_code_from_spec
    ├── doc_generator.py      // Implements generate_docs_from_spec
    ├── spec_comparer.py      // Implements compare_specs
    └── change_manager.py     // Implements create_change_proposal, archive_change_proposal
```
