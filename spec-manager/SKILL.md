---
name: spec-manager
description: A skill to manage, analyze, validate, and generate content related to API specifications. It supports spec-driven development workflows, enabling AI Agents to better understand and operate with API interfaces, and assist in generating code, documentation, or tests.
---

# Spec Manager Skill (API Specification Management)

This skill provides a comprehensive toolkit for AI Agents to interact with API specifications, fostering spec-driven development practices. It enables the agent to fetch, parse, validate, compare, and generate various artifacts from API specifications, as well as manage change proposals.

## Actions

### `spec_manager`
*   **Purpose**: Orchestrates the entire spec-driven development workflow, providing a unified interface for all stages from project initialization to code implementation.
*   **Inputs**:
    *   `step` (string, required): The specific workflow step to execute. Supported steps include:
        *   `"init"`: Initializes a new spec-driven project.
        *   `"define_principles"`: Defines or updates project guiding principles.
        *   `"proposal"`: Creates a new change proposal.
        *   `"plan"`: Generates a high-level implementation plan.
        *   `"tasks"`: Refines the plan into a detailed task list.
        *   `"implement"`: Orchestrates the execution of tasks for a change proposal.
        *   `"archive"`: Archives a completed change proposal.
        *   `"fetch"`: Fetches API specification content.
        *   `"parse"`: Parses API specification content.
        *   `"validate"`: Validates API specifications.
        *   `"generate_code"`: Generates code from API specifications.
        *   `"generate_docs"`: Generates documentation from API specifications.
        *   `"compare"`: Compares two API specifications.
        *   `"clarify"`: Analyzes a change proposal for vague language and generates clarifying questions.
        *   `"list_projects"`: Scans a directory for OpenSpec projects and returns a list of their names and roots.
    *   `kwargs` (object, optional): A dictionary of keyword arguments specific to the chosen `step`. Refer to the individual script documentation for required arguments for each step.
*   **Outputs**:
    *   The output varies depending on the `step` executed. It will typically include a `success` status, a `message`, and any step-specific data (e.g., `llm_prompt`, `output_path`, `parsed_data`, `diff_report`).

## Implementation Details

This skill utilizes a main dispatcher script (`main.py`) in the `scripts/` directory to orchestrate all its functionalities. All individual workflow steps are handled internally by this dispatcher.

## Prerequisites

Python 3.9+ and pip are required. Specific Python package dependencies will be managed within the skill's Python environment.

## Resources

*   `resources/config.json`: General skill configuration.
*   `resources/templates/code_generation/`: Templates for code generation.
*   `resources/templates/docs_generation/`: Templates for documentation generation.

