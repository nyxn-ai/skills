#!/usr/bin/env python3

import os
import sys
import jinja2

def create_mcp_tool(tool_name: str, output_dir: str = None):
    """
    Generates boilerplate Python code for a new MCP tool using a Jinja2 template.

    Args:
        tool_name: The desired name for the tool (e.g., 'get_user_data').
        output_dir: The directory where the tool file should be created.
                    Defaults to the current directory if None.
    """
    if not tool_name:
        print("Error: tool_name cannot be empty.", file=sys.stderr)
        sys.exit(1)

    # Convert tool_name to PascalCase for the class name
    class_name = ''.join(word.capitalize() for word in tool_name.split('_')) + "Tool"
    
    # Define the output file name
    file_name = f"{tool_name}_tool.py"
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, file_name)
    else:
        output_path = file_name

    # Setup Jinja2 environment
    # The script is in 'scripts/', so the templates are in '../assets/templates'
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates')
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    
    try:
        template = env.get_template('tool_template.py.j2')
    except jinja2.TemplateNotFound:
        print(f"Error: Template 'tool_template.py.j2' not found in '{template_dir}'", file=sys.stderr)
        sys.exit(1)

    # Data to render the template with
    context = {
        "tool_name": tool_name,
        "class_name": class_name,
        "file_name": file_name
    }

    # Render the template
    template_content = template.render(context)

    try:
        with open(output_path, "w") as f:
            f.write(template_content)
        print(f"Successfully created boilerplate for tool '{tool_name}' at '{output_path}'")
        # Make the script executable
        os.chmod(output_path, 0o755)
        print(f"Made '{output_path}' executable.")
    except Exception as e:
        print(f"Error writing tool file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} <tool_name> [output_directory]", file=sys.stderr)
        sys.exit(1)

    tool_name = sys.argv[1]
    output_directory = sys.argv[2] if len(sys.argv) == 3 else None
    
    create_mcp_tool(tool_name, output_directory)
