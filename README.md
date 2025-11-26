# nyxn-ai/skills

This repository serves as a central collection point for various skills designed to extend the capabilities of the nyxn-ai agent. Each skill is self-contained within its own directory and includes a `SKILL.md` file detailing its functionality and how an agent can interact with it.

## Available Skills

*   **markdown-organizer**
    *   **Description**: This skill empowers an agent to manage Markdown articles by leveraging Large Language Models (LLM) for advanced semantic understanding, categorization, summarization, and even code generation. It transforms a collection of static documents into a dynamic, LLM-powered knowledge and creation assistant.
    *   **Path**: `markdown-organizer/`

*   **mcp-tool-factory**
    *   **Description**: A skill for creating new MCP tools in Python using a standardized class-based pattern. Use this to quickly bootstrap new tools for a FastMCP server, ensuring consistency and adherence to best practices for tool registration.
    *   **Path**: `mcp-tool-factory/`

*   **prompt-optimizer**
    *   **Description**: A skill to guide users in crafting token-efficient prompts for tool-using AI agents. Use this when you want to learn how to write better prompts to get faster, more accurate results and save costs.
    *   **Path**: `prompt-optimizer/`

*   **spec-manager**
    *   **Description**: This skill equips AI Agents with a unified workflow engine for comprehensive spec-driven development, including multi-project support and project discovery. It integrates best practices from OpenSpec and Spec Kit to streamline the entire API lifecycle—from project initialization with optional Git integration, interactive requirement clarification, and TDD-focused task breakdowns, to automated code implementation and change archiving. It empowers agents to fetch, parse, validate, compare, and generate various artifacts from API definitions.
    *   **Path**: `spec-manager/`

## Contributing New Skills

To add a new skill to this repository:
1.  Create a new directory for your skill.
2.  Inside the new directory, create a `SKILL.md` file that describes the skill's purpose, usage, inputs, outputs, and any prerequisites.
3.  Include all necessary scripts, resources, and configuration files within the skill's directory.
4.  Update this `README.md` to include your new skill in the "Available Skills" section.
