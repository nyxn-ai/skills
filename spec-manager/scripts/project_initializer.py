import os
import argparse
import json

def init_spec_project(project_root):
    """
    Initializes a project for spec-driven development, setting up the required directory structure and foundational files.
    """
    try:
        openspec_dir = os.path.join(project_root, 'openspec')
        os.makedirs(os.path.join(openspec_dir, 'specs'), exist_ok=True)
        os.makedirs(os.path.join(openspec_dir, 'changes'), exist_ok=True)

        # Create placeholder files
        with open(os.path.join(openspec_dir, 'project.md'), 'w') as f:
            f.write("# Project Context\n\nDescribe your project, its tech stack, and conventions here.")
        
        with open(os.path.join(openspec_dir, 'constitution.md'), 'w') as f:
            f.write("# Project Principles\n\nDefine your project's guiding principles and development guidelines here.")

        return {"success": True, "message": f"OpenSpec project initialized at {project_root}"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def define_principles(principles_content, project_root):
    """
    Allows the user to define or update the project's governing principles and development guidelines.
    """
    try:
        constitution_path = os.path.join(project_root, 'openspec', 'constitution.md')
        if not os.path.exists(os.path.dirname(constitution_path)):
            return {"success": False, "message": f"OpenSpec project not initialized at {project_root}. Please run init_spec_project first."}

        with open(constitution_path, 'w') as f:
            f.write(principles_content)
        
        return {"success": True, "message": f"Project principles updated in {constitution_path}"}
    except Exception as e:
        return {"success": False, "message": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage spec-driven development project initialization and principles.")
    parser.add_argument("action", choices=["init_spec_project", "define_principles"], help="Action to perform.")
    parser.add_argument("--project_root", required=True, help="The root directory of the project.")
    parser.add_argument("--principles_content", help="The content for project principles (required for define_principles action).")

    args = parser.parse_args()

    if args.action == "init_spec_project":
        result = init_spec_project(args.project_root)
    elif args.action == "define_principles":
        if not args.principles_content:
            result = {"success": False, "message": "--principles_content is required for define_principles action."}
        else:
            result = define_principles(args.principles_content, args.project_root)
    
    print(json.dumps(result))
