import os
import re
import sys # Keep sys for now, useful for debug prints to stderr later
import unicodedata # Added for sanitize_task_name
from utils import sanitize_task_name # Import the sanitation function

def _mark_task_complete(tasks_path, task_description):
    """
    Marks a specific task as complete in the tasks.md file.
    """
    with open(tasks_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # Match the line for the specific task, ignoring leading/trailing whitespace
        if f"- [ ] {task_description.strip()}" in line.strip():
            new_lines.append(line.replace("- [ ]", "- [x]", 1))
        else:
            new_lines.append(line)

    with open(tasks_path, 'w') as f:
        f.write("".join(new_lines))

def implement_change(change_id, project_root):
    """
    Orchestrates the implementation of a change proposal by parsing the tasks.md file
    and generating prompts for the AI agent to execute each task.
    
    This function is a generator that yields prompts for the agent.
    """
    change_dir = os.path.join(project_root, 'openspec', 'changes', change_id)
    tasks_path = os.path.join(change_dir, 'tasks.md')
    constitution_path = os.path.join(project_root, 'openspec', 'constitution.md')

    if not os.path.exists(tasks_path):
        yield {"success": False, "message": f"tasks.md not found for change_id '{change_id}'"}
        return

    with open(tasks_path, 'r') as f:
        tasks_content = f.read()
    
    # Fix: Add re.MULTILINE flag and use a more robust regex pattern
    raw_pending_tasks = re.findall(r'^\s*-\s*\[\s*\]\s*(.+)', tasks_content, re.MULTILINE)
    
    if not raw_pending_tasks:
        yield {"success": True, "message": "All tasks are already completed."}
        return

    # Sanitize tasks immediately after parsing
    pending_tasks = [] # Initialize here
    for raw_task in raw_pending_tasks:
        cleaned_task = sanitize_task_name(raw_task)
        # We can add a print here if raw_task != cleaned_task for future debugging, but keep it clean for now
        pending_tasks.append(cleaned_task)


    # Read context files
    constitution = ""
    if os.path.exists(constitution_path):
        with open(constitution_path, 'r') as f:
            constitution = f.read()

    # In a real scenario, we would also read the spec delta files.
    # For this example, we'll just use the constitution.

    yield {
        "success": True, 
        "message": f"Starting implementation of {len(pending_tasks)} pending tasks for change_id '{change_id}'."
    }

    for task in pending_tasks:
        task_lower = task.lower() # 'task' is already sanitized, just lowercasing
        
        is_test_task = any(indicator in task_lower for indicator in [
            "test", "tests", "testing", "run test", "execute test",
            "unit test", "unit tests"
        ])
        
        if is_test_task:
            prompt = f"""
            **Project Constitution & Principles:**
            ---\n
            {constitution}
            ---

            **Current Task:**
            {task}

            **Your Goal:**
            Execute the test task described above. 
            - Identify the appropriate test command and framework for this project (e.g., `pytest`, `npm test`, `flutter test`).
            - Run the tests and report the outcome (success/failure).
            - If tests fail, report the errors.
            - Adhere strictly to the project constitution.
            """
        else:
            prompt = f"""
            **Project Constitution & Principles:**
            ---\n
            {constitution}
            ---

            **Current Task:**
            {task}

            **Your Goal:**
            Execute the task described above. 
            - If the task involves creating or modifying a file, please output the full content of the file.
            - If the task involves running a command, please output the command to run.
            - Adhere strictly to the project constitution.
            """
        
        yield {
            "prompt": prompt.strip(),
            "task": task
        }
        
        # --- Task completion and yield for next iteration ---
        _mark_task_complete(tasks_path, task)
        yield {
            "message": f"Task '{task}' marked as complete."
        }
        # --- End of task completion ---

    yield {"success": True, "message": f"All tasks for change_id '{change_id}' have been completed."}

if __name__ == '__main__':
    # Example usage for testing
    project_dir = 'test_project'
    change_name = 'example_change'
    tasks_file_path = os.path.join(project_dir, 'openspec', 'changes', change_name, 'tasks.md')
    constitution_file_path = os.path.join(project_dir, 'openspec', 'constitution.md')

    # Re-create dummy files for a clean test run
    os.makedirs(os.path.dirname(tasks_file_path), exist_ok=True)
    with open(tasks_file_path, 'w') as f:
        f.write("- [ ] Task 1: Write code for login feature.\n")
        f.write("- [ ] Task 2: Run unit tests for login feature.\n")
        f.write("- [ ] Task 3: Refactor login code.\n")
    
    os.makedirs(os.path.dirname(constitution_file_path), exist_ok=True)
    with open(constitution_file_path, 'w') as f:
        f.write("All code should be written in JavaScript ES6. All functions must have JSDoc comments.")

    print(f"--- Running implementation for '{change_name}' ---")
    
    implementation_generator = implement_change(change_name, project_dir)
    
    for result in implementation_generator:
        print("\n--- Yielded Result ---")
        if result.get("prompt"):
            print(f"Agent Prompt:\n{result['prompt']}")
            print(f"\n(Simulating agent action for task: '{result['task']}')")
        else:
            print(f"Status Update: {result['message']}")

    print("\n--- Final tasks.md content ---")
    with open(tasks_file_path, 'r') as f:
        print(f.read())