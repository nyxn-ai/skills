import os
import json
import argparse # Added import for argparse

def list_projects(base_directory=None):
    """
    Scans a base directory for subdirectories containing an 'openspec/' folder,
    identifying them as distinct projects.
    """
    if base_directory is None:
        base_directory = os.getcwd()

    identified_projects = []
    
    # Walk through the directories, but only one level deep initially
    # This prevents scanning into project subdirectories unnecessarily
    for entry in os.listdir(base_directory):
        potential_project_path = os.path.join(base_directory, entry)
        
        if os.path.isdir(potential_project_path):
            openspec_path = os.path.join(potential_project_path, 'openspec')
            if os.path.isdir(openspec_path):
                # Found an OpenSpec project
                project_name = entry
                project_root = potential_project_path
                identified_projects.append({
                    "project_name": project_name,
                    "project_root": project_root
                })
    
    # Also check the base directory itself if it's an openspec project
    if os.path.isdir(os.path.join(base_directory, 'openspec')):
        project_name = os.path.basename(base_directory)
        project_root = base_directory
        # Avoid duplicates if the base directory was also found as a subdirectory
        if not any(p['project_root'] == project_root for p in identified_projects):
            identified_projects.append({
                "project_name": project_name,
                "project_root": project_root
            })

    return {"success": True, "projects": identified_projects, "base_directory": base_directory}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan for OpenSpec projects.")
    parser.add_argument("--base_directory", help="The directory to scan for projects. Defaults to current working directory.")

    args = parser.parse_args()

    result = list_projects(args.base_directory)
    print(json.dumps(result, indent=2))
