# spec-manager/scripts/code_generator.py
import os
from jinja2 import Environment, FileSystemLoader
import json # For parsing spec content if it's JSON

def generate_code_from_spec(spec_content, target_language, code_type="client", output_dir=None):
    """
    Prepares a prompt for the AI Agent to generate code based on the API specification.
    """
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "generated_code") # Default output to current working directory/generated_code
    os.makedirs(output_dir, exist_ok=True)

    # In a real scenario, this would involve a proper spec parser to extract details
    # For now, we'll assume a basic structure from the spec_parser.py
    parsed_spec = {}
    try:
        parsed_spec = json.loads(spec_content) # Assuming JSON for simplicity in example
    except json.JSONDecodeError:
        # Fallback if not JSON, but proper parsing would be needed
        pass

    api_name = parsed_spec.get('info', {}).get('title', 'Your API')
    
    # Load template from skill's resources
    # Dynamic template loading based on target_language and code_type
    templates_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'templates', 'code_generation')
    
    template_file = f"{target_language}/{code_type}.j2"
    
    try:
        env = Environment(loader=FileSystemLoader(templates_path))
        # Add a custom filter to trim leading/trailing slashes and make valid Python identifiers
        env.filters['trim_leading_slash'] = lambda s: s.lstrip('/')
        template = env.get_template(template_file)
    except Exception as e:
        return {"error": f"Failed to load template {template_file}: {e}"}

    # Render the template with spec data
    rendered_code = template.render(
        api_name=api_name,
        endpoints=parsed_spec.get('paths', {}), # Pass the paths object directly
        # You would pass more parsed data here as needed by the template
    )

    output_file_path = os.path.join(output_dir, f"{api_name.lower().replace(' ', '_')}_{code_type}.py")
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(rendered_code)
    except Exception as e:
        return {"error": f"Failed to write generated code to {output_file_path}: {e}"}

    prompt = f"""
I have generated a {target_language} {code_type} skeleton for the '{api_name}' API based on the provided specification.
The generated code is located at: {output_file_path}

Please review the generated code, ensure its correctness and completeness based on the specification, and integrate it into the project as needed.
You may need to fill in implementation details or add error handling.
"""
    return {"llm_prompt": prompt, "output_path": output_file_path}
