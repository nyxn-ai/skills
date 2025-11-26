import os
import json

def clarify_requirements(change_id, project_root):
    """
    Analyzes a change proposal for vague language or underspecified areas and
    generates clarifying questions for the user.
    """
    try:
        change_dir = os.path.join(project_root, 'openspec', 'changes', change_id)
        proposal_path = os.path.join(change_dir, 'proposal.md')

        if not os.path.exists(proposal_path):
            return {"llm_prompt": None, "error": f"Proposal file not found for change_id '{change_id}' at {proposal_path}"}

        with open(proposal_path, 'r', encoding='utf-8') as f:
            proposal_content = f.read()

        llm_prompt = f"""
        **Change Proposal for Clarification:**
        ---
        {proposal_content}
        ---

        **Your Goal:**
        Please carefully analyze the change proposal above for any vague language, ambiguities,
        unclear requirements, or underspecified areas.
        
        Generate a list of clarifying questions for the user. These questions should aim to:
        - Make requirements precise and unambiguous.
        - Uncover missing details.
        - Explore potential edge cases or user interactions not explicitly mentioned.
        - Identify any implicit assumptions.

        Present your questions in a clear, numbered list format.
        """
        
        return {"llm_prompt": llm_prompt, "error": None}
    except Exception as e:
        return {"llm_prompt": None, "error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate clarifying questions for a change proposal.")
    parser.add_argument("--change_id", required=True, help="The identifier of the change proposal.")
    parser.add_argument("--project_root", required=True, help="The root directory of the project.")

    args = parser.parse_args()

    result = clarify_requirements(args.change_id, args.project_root)
    print(json.dumps(result, indent=2))