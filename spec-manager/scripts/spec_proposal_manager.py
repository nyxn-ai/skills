import os
import argparse
import json
import shutil

def create_change_proposal(proposed_changes_description, project_root, change_id):
    """
    Assists the AI Agent in creating structured API specification change proposals, including proposed changes, task lists, and spec deltas.
    """
    try:
        change_dir = os.path.join(project_root, 'openspec', 'changes', change_id)
        os.makedirs(os.path.join(change_dir, 'specs'), exist_ok=True)

        with open(os.path.join(change_dir, 'proposal.md'), 'w') as f:
            f.write(f"# Change Proposal: {change_id}\n\n{proposed_changes_description}\n\n")
            f.write("## Proposed Changes\n\n[Describe proposed changes in detail here]\n")
        
        with open(os.path.join(change_dir, 'tasks.md'), 'w') as f:
            f.write(f"# Tasks for {change_id}\n\n[Initial tasks will be broken down here]\n")

        # Placeholder for spec deltas
        # In a real scenario, this might involve copying a base spec or creating an empty one.
        with open(os.path.join(change_dir, 'specs', 'spec.md'), 'w') as f:
            f.write(f"# Spec Delta for {change_id}\n\n")
            f.write("## ADDED Requirements\n\n## MODIFIED Requirements\n\n## REMOVED Requirements\n")

        return {
            "llm_prompt": f"Change proposal '{change_id}' created at '{change_dir}'. Please refine 'proposal.md', 'tasks.md', and 'specs/spec.md' with detailed changes.",
            "proposal_path": change_dir,
            "error": None
        }
    except Exception as e:
        return {"llm_prompt": None, "proposal_path": None, "error": str(e)}

def archive_change_proposal(change_id, project_root):
    """
    Merges approved specification changes from a proposal into the main specification and archives the change files.
    """
    try:
        change_dir = os.path.join(project_root, 'openspec', 'changes', change_id)
        if not os.path.exists(change_dir):
            return {"success": False, "message": f"Change proposal '{change_id}' not found.", "updated_main_spec_path": None}

        # Placeholder for merging logic
        # In a real scenario, this would involve parsing spec deltas and applying them to the main spec.
        # For simplicity, we'll just move the spec delta to the main specs directory,
        # assuming it's a new spec or a full replacement for an existing one.
        main_specs_dir = os.path.join(project_root, 'openspec', 'specs')
        delta_spec_path = os.path.join(change_dir, 'specs', 'spec.md')
        target_main_spec_path = os.path.join(main_specs_dir, f"{change_id}_spec.md") # Or a more sophisticated naming

        if os.path.exists(delta_spec_path):
            shutil.copy(delta_spec_path, target_main_spec_path) # Copy delta as new main spec for simplicity
            updated_main_spec_path = target_main_spec_path
        else:
            updated_main_spec_path = None
        
        archive_dir = os.path.join(project_root, 'openspec', 'archive')
        os.makedirs(archive_dir, exist_ok=True)
        shutil.move(change_dir, os.path.join(archive_dir, change_id))

        return {
            "success": True,
            "message": f"Change proposal '{change_id}' archived successfully. Main spec updated.",
            "updated_main_spec_path": updated_main_spec_path
        }
    except Exception as e:
        return {"success": False, "message": str(e), "updated_main_spec_path": None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage spec-driven development change proposals.")
    parser.add_argument("action", choices=["create_change_proposal", "archive_change_proposal"], help="Action to perform.")
    parser.add_argument("--project_root", required=True, help="The root directory of the project.")
    parser.add_argument("--change_id", required=True, help="The identifier for the change proposal (e.g., 'add-profile-filters').")
    parser.add_argument("--proposed_changes_description", help="A natural language description of the proposed changes (required for create_change_proposal).")

    args = parser.parse_args()

    if args.action == "create_change_proposal":
        if not args.proposed_changes_description:
            result = {"llm_prompt": None, "proposal_path": None, "error": "--proposed_changes_description is required for create_change_proposal action."}
        else:
            result = create_change_proposal(args.proposed_changes_description, args.project_root, args.change_id)
    elif args.action == "archive_change_proposal":
        result = archive_change_proposal(args.change_id, args.project_root)
    
    print(json.dumps(result))
