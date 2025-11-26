# Spec Manager: Empowering AI Agents with Spec-Driven Development

The `spec-manager` skill provides a comprehensive toolkit for AI Agents to interact with and leverage API specifications (like OpenAPI, Swagger, AsyncAPI). It streamlines spec-driven development workflows, enabling Agents to understand, validate, compare, and generate artifacts from API definitions.

It now integrates the best practices and functionalities inspired by projects like `spec-kit` and `OpenSpec`, offering a unified command interface for a highly automated and persistent development experience.

## Key Features & Optimizations

*   **Unified Workflow Engine**: A single `spec_manager` command orchestrates the entire development lifecycle, from project initialization to code implementation.
*   **Multi-Project Support and Discovery**: Scans specified directories to identify multiple independent OpenSpec projects, enhancing management in complex workspaces.
*   **Spec-Driven Development**: Emphasizes defining specifications first, ensuring clarity, consistency, and traceability throughout the project.
*   **Optional & Configurable Git Integration**:
    *   Automatically creates Git branches for new change proposals.
    *   Commits initial proposal files.
    *   Deletes feature branches upon archiving.
    *   (Future: Automatic Pull Request creation, commit-per-task)
*   **Automated Testing Workflow (TDD Focused)**:
    *   Prompts AI to generate test tasks following a Test-Driven Development (TDD) approach during task breakdown.
    *   (Future: Automated test execution after tasks, specialized prompts for test execution).
*   **Interactive Requirement Clarification**: Introduces a dedicated step to analyze proposals for ambiguity and generate clarifying questions, reducing rework.
*   **Universal Spec Handling**: Fetch, parse, and validate API specifications from various sources (local files, URLs) and formats.
*   **Code & Documentation Generation**: Assist Agents in generating client SDKs, server stubs, data models, and comprehensive API documentation directly from specs.
*   **Change Management**: Supports structured workflows for creating, planning, implementing, and archiving API specification change proposals.
*   **Persistence**: All project state (specs, proposals, tasks, configurations) is managed through the file system, allowing seamless resumption of work.

## How an AI Agent Uses This Skill

This skill acts as a powerful interface, allowing AI Agents to perform complex, multi-stage operations on API specifications through a single, unified `spec_manager` command. For actions that require creative generation (e.g., code, documentation, detailed plans), the skill prepares a detailed `llm_prompt` for the Agent to process using its own Large Language Model (LLM) capabilities.

### Unified Agent Action: `spec_manager`

Instead of individual actions, the AI Agent now uses one command with a `step` parameter to control the workflow.

**Action Name**: `spec_manager`
**Purpose**: Orchestrates the entire spec-driven development workflow.
**Inputs**:
*   `step` (string, required): The specific workflow step to execute. Supported steps include:
    *   `"init"`: Initializes a new spec-driven project, optionally enabling Git integration.
    *   `"define_principles"`: Defines or updates project guiding principles (`constitution.md`).
    *   `"proposal"`: Creates a new change proposal, including initial files (`proposal.md`, `tasks.md`, `specs/spec.md`) and optionally a new Git branch.
    *   `"clarify"`: Analyzes a proposal for vague language and generates clarifying questions.
    *   `"plan"`: Generates a high-level technical implementation plan (`plan.md`).
    *   `"tasks"`: Refines the plan into a detailed, actionable task list (`tasks.md`), emphasizing TDD.
    *   `"implement"`: Orchestrates the execution of tasks from `tasks.md`, generating prompts for the AI agent and marking tasks as complete.
    *   `"archive"`: Finalizes and integrates approved spec changes, moving the proposal to the archive and optionally deleting the Git branch.
    *   `"fetch"`: Retrieves API specification content from a local path or URL.
    *   `"parse"`: Extracts structured data from an API specification.
    *   `"validate"`: Verifies the compliance and correctness of an API specification.
    *   `"generate_code"`: Prepares prompt for generating client SDKs, server stubs, or data models.
    *   `"generate_docs"`: Prepares prompt for generating API documentation.
    *   `"compare"`: Identifies differences between two API specifications.
    *   `"list_projects"`: Scans a directory for OpenSpec projects and returns a list of their names and roots.
*   `kwargs` (object, optional): A dictionary of keyword arguments specific to the chosen `step`. Refer to `SKILL.md` for detailed input/output for each step.

## Installation & Prerequisites

To enable the `spec-manager` skill in your AI Agent's environment:

1.  **Python**: Ensure Python 3.9+ is installed.
2.  **Dependencies**: Install necessary Python packages listed in `requirements.txt`.
    ```bash
    pip install -r spec-manager/requirements.txt
    ```
3.  **Git**: (Optional, for Git integration features) Ensure Git is installed and configured.
4.  **Skill Integration**: Follow your AI Agent's specific instructions for integrating new skills (e.g., placing the `spec-manager` directory in a designated `skills/` folder).

## Directory Structure

```
spec-manager/
├── SKILL.md                  // Skill definition for the AI Agent (unified spec_manager action)
├── README.md                 // Human-readable documentation for the skill
├── requirements.txt          // Python dependencies
├── resources/                // Templates, configurations, schemas
│   ├── config.json           // General skill configuration (currently not used)
│   ├── schemas/              // e.g., openapi_v3.json for validation (future)
│   └── templates/
│       ├── code_generation/  // Jinja2 templates for code generation
│       └── docs_generation/  // Jinja2 templates for documentation generation
└── scripts/                  // Python scripts implementing skill actions
    ├── main.py               // The unified dispatcher for all spec_manager steps
    ├── utils.py              // General utility functions (Git helpers, string sanitation)
    ├── clarifier.py          // Implements the 'clarify' step
    ├── implementer.py        // Implements the 'implement' step
    ├── project_initializer.py// Implements the 'init' and 'define_principles' steps
    ├── spec_comparer.py      // Implements the 'compare' step
    ├── spec_fetcher.py       // Implements the 'fetch' step
    ├── spec_parser.py        // Implements the 'parse' step
    ├── spec_planner.py       // Implements the 'plan' and 'tasks' steps
    ├── spec_proposal_manager.py // Implements the 'proposal' and 'archive' steps
    ├── spec_validator.py     // Implements the 'validate' step
    ├── code_generator.py     // Implements the 'generate_code' step
    └── doc_generator.py      // Implements the 'generate_docs' step

```

## Workflow Example (Simplified)

1.  **Initialize Project**: `spec_manager(step='init', kwargs={'project_root': 'my-api-project', 'git_enabled': True})`
2.  **Define Principles**: `spec_manager(step='define_principles', kwargs={'project_root': 'my-api-project', 'principles_content': 'Our API must be RESTful and secure.'})`
3.  **Create Proposal**: `spec_manager(step='proposal', kwargs={'project_root': 'my-api-project', 'change_id': 'add-user-auth', 'proposed_changes_description': 'Implement user authentication endpoints.'})`
4.  **Clarify Requirements**: `spec_manager(step='clarify', kwargs={'project_root': 'my-api-project', 'change_id': 'add-user-auth'})` (AI generates questions)
5.  **Generate Plan**: `spec_manager(step='plan', kwargs={'project_root': 'my-api-project', 'change_id': 'add-user-auth'})` (AI generates a plan)
6.  **Breakdown Tasks**: `spec_manager(step='tasks', kwargs={'project_root': 'my-api-project', 'change_id': 'add-user-auth'})` (AI generates TDD-focused tasks)
7.  **Implement Changes**: `spec_manager(step='implement', kwargs={'project_root': 'my-api-project', 'change_id': 'add-user-auth'})` (AI executes tasks step-by-step, receiving specialized prompts for test tasks)
8.  **Archive Proposal**: `spec_manager(step='archive', kwargs={'project_root': 'my-api-project', 'change_id': 'add-user-auth'})`

This new README provides a clear, up-to-date overview of the `spec-manager` skill's enhanced capabilities.