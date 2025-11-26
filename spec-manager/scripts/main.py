import argparse
import json
import os
import sys

# Import functions from other scripts
from project_initializer import init_spec_project, define_principles
from spec_planner import generate_plan, breakdown_tasks
from implementer import implement_change
from spec_fetcher import fetch_spec
from spec_parser import parse_spec
from spec_validator import validate_spec
from code_generator import generate_code_from_spec
from doc_generator import generate_docs_from_spec
from spec_comparer import compare_specs
from spec_proposal_manager import create_change_proposal, archive_change_proposal
from clarifier import clarify_requirements
from project_finder import list_projects # New import for project discovery # New import for clarification


def handle_result(result):
    """
    Handles the result from a command function, especially for generator functions.
    """
    if isinstance(result, dict):
        return result
    elif hasattr(result, '__iter__') and not isinstance(result, str): # Check if it's a generator
        all_results = []
        for item in result:
            all_results.append(item)
        return all_results
    return {"success": True, "message": "Command executed successfully.", "output": result}


def run(step, **kwargs):
    """
    Main dispatcher for the spec-manager skill.
    Calls the appropriate function based on the workflow step.
    """
    print(f"Dispatcher running step: {step} with args: {kwargs}", file=sys.stderr) # Print to stderr for debugging

    COMMAND_MAP = {
        "init": init_spec_project,
        "define_principles": define_principles,
        "proposal": create_change_proposal,
        "plan": generate_plan,
        "tasks": breakdown_tasks,
        "implement": implement_change,
        "archive": archive_change_proposal,
        "fetch": fetch_spec,
        "parse": parse_spec,
        "validate": validate_spec,
        "generate_code": generate_code_from_spec,
        "generate_docs": generate_docs_from_spec,
        "compare": compare_specs,
        "clarify": clarify_requirements,
        "list_projects": list_projects, # New list_projects step
    }

    command_func = COMMAND_MAP.get(step)

    if not command_func:
        return {"success": False, "message": f"Unknown step: {step}"}

    # Default project_root to current working directory for 'init' step if not provided
    if step == "init" and "project_root" not in kwargs:
        kwargs["project_root"] = os.getcwd()

    try:
        result = command_func(**kwargs)
        return handle_result(result)
    except Exception as e:
        return {"success": False, "message": f"Error executing step '{step}': {str(e)}"}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Main dispatcher for spec-manager workflow.")
    parser.add_argument("step", help="The workflow step to execute (e.g., 'init', 'proposal', 'plan', 'tasks', 'implement', 'archive').")
    parser.add_argument('--kwargs', type=json.loads, default='{}', help='JSON string of keyword arguments for the step.')
    parser.add_argument("--git_enabled", action='store_true', help="Enable Git integration during project initialization.") # Added git_enabled arg

    args = parser.parse_args()

    # If git_enabled is provided as a top-level argument, add it to kwargs for init step
    if args.step == 'init' and args.git_enabled:
        args.kwargs['git_enabled'] = True
    
    final_result = run(args.step, **args.kwargs)
    
    print(json.dumps(final_result, indent=2))
