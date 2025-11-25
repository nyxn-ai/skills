# spec-manager/scripts/change_manager.py
import os
import json
import yaml

def create_change_proposal(proposed_changes_description, original_spec_content=None, output_dir=None):
    """
    Assists the AI Agent in creating structured API specification change proposals.
    """
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "spec-changes") # Default output to current working directory/spec-changes
    
    # Generate a simple unique ID for the change proposal
    change_id = f"change_{len(os.listdir(output_dir)) + 1:03d}" if os.path.exists(output_dir) else "change_001"
    proposal_path = os.path.join(output_dir, change_id)
    os.makedirs(proposal_path, exist_ok=True)
    
    # Create proposal.md
    proposal_md_content = f"""# Change Proposal: {change_id}

## Proposed Changes
{proposed_changes_description}

## Rationale
[Explain why these changes are necessary]

## Tasks
[Generated tasks for implementation, to be filled by LLM]

## Spec Deltas
[Details of changes to the API specification, to be filled by LLM]
"""
    with open(os.path.join(proposal_path, "proposal.md"), 'w', encoding='utf-8') as f:
        f.write(proposal_md_content)

    # Optionally save original spec for diffing later if provided
    if original_spec_content:
        with open(os.path.join(proposal_path, "original_spec.yaml"), 'w', encoding='utf-8') as f:
            f.write(original_spec_content)

    prompt = f"""
Based on the description of proposed changes, please generate the following files within the change proposal directory '{proposal_path}':

1.  **tasks.md**: A detailed markdown file outlining the implementation tasks required for these changes. Use checkboxes for each task item.
2.  **specs/delta.yaml**: A YAML file representing the changes to the API specification. This should only include the ADDED, MODIFIED, or REMOVED sections for endpoints, models, etc. (similar to OpenSpec's delta format).

Proposed Changes Description:
{proposed_changes_description}
"""
    return {"llm_prompt": prompt, "proposal_path": proposal_path, "change_id": change_id}

def archive_change_proposal(change_id, base_dir):
    """
    Merges approved specification changes from a proposal into the main specification and archives the change files.
    This is a simplified implementation. A real-world scenario would involve complex merging logic.
    """
    error = None
    success = False
    updated_main_spec_path = None

    proposal_path = os.path.join(base_dir, change_id)
    if not os.path.exists(proposal_path):
        return {"success": False, "message": f"Change proposal '{change_id}' not found at {proposal_path}"}

    # Assume main spec is at base_dir/main_spec.yaml for simplicity
    main_spec_path = os.path.join(base_dir, "main_spec.yaml")
    delta_spec_path = os.path.join(proposal_path, "specs", "delta.yaml") # Assuming delta spec is here

    try:
        # Load main spec
        main_spec_data = {}
        if os.path.exists(main_spec_path):
            with open(main_spec_path, 'r', encoding='utf-8') as f:
                main_spec_data = yaml.safe_load(f)

        # Load delta spec (simplified: just replace/add based on delta)
        delta_spec_data = {}
        if os.path.exists(delta_spec_path):
            with open(delta_spec_path, 'r', encoding='utf-8') as f:
                delta_spec_data = yaml.safe_load(f)
            
            # Simple merge logic: for full implementation, use proper spec merging library
            # This example just shows a conceptual merge
            # Here, a more sophisticated merge of delta_spec_data into main_spec_data would occur
            # For instance, if delta has 'paths', merge them into main_spec_data['paths']
            if 'paths' in delta_spec_data:
                main_spec_data['paths'] = {**main_spec_data.get('paths', {}), **delta_spec_data['paths']}
            if 'components' in delta_spec_data:
                main_spec_data['components'] = {**main_spec_data.get('components', {}), **delta_spec_data['components']}
            # ... and so on for other top-level fields
            
            # Write updated main spec
            with open(main_spec_path, 'w', encoding='utf-8') as f:
                yaml.dump(main_spec_data, f, sort_keys=False)
            updated_main_spec_path = main_spec_path
        else:
            error = f"Delta spec file not found at {delta_spec_path} for archiving."
            
        # Move proposal directory to an 'archived' folder
        archive_dir = os.path.join(base_dir, "archived_changes")
        os.makedirs(archive_dir, exist_ok=True)
        os.rename(proposal_path, os.path.join(archive_dir, change_id))
        
        success = True
        message = f"Change proposal '{change_id}' archived successfully. Main spec updated at {updated_main_spec_path}."

    except Exception as e:
        error = f"An unexpected error occurred during archiving: {e}"
        success = False

    return {"success": success, "message": message, "updated_main_spec_path": updated_main_spec_path, "error": error}
