# spec-manager/scripts/doc_generator.py
import os
from jinja2 import Environment, FileSystemLoader
import json # For parsing spec content if it's JSON

def generate_docs_from_spec(spec_content, doc_format="Markdown", output_dir=None):
    """
    Prepares a prompt for the AI Agent to generate documentation based on the API specification.
    """
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "generated_docs") # Default output to current working directory/generated_docs
    os.makedirs(output_dir, exist_ok=True)

    # In a real scenario, this would involve a proper spec parser to extract details
    # For now, we'll assume a basic structure from the spec_parser.py
    parsed_spec = {}
    try:
        parsed_spec = json.loads(spec_content) # Assuming JSON for simplicity in example
    except json.JSONDecodeError:
        # Fallback if not JSON, but proper parsing would be needed
        pass

    api_name = parsed_spec.get('info', {}).get('title', 'API Documentation')
    description = parsed_spec.get('info', {}).get('description', '')

    # Load template from skill's resources
    templates_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'templates', 'docs_generation')
    template_file = f"{doc_format.lower()}.j2"

    try:
        env = Environment(loader=FileSystemLoader(templates_path))
        template = env.get_template(template_file)
    except Exception as e:
        return {"error": f"Failed to load template {template_file}: {e}"}

    # Render the template with spec data
    rendered_docs = template.render(
        api_name=api_name,
        description=description,
        endpoints=parsed_spec.get('paths', {}),
        # You would pass more parsed data here as needed by the template
    )

    output_file_path = os.path.join(output_dir, f"{api_name.lower().replace(' ', '_')}_docs.{doc_format.lower()}")
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(rendered_docs)
    except Exception as e:
        return {"error": f"Failed to write generated docs to {output_file_path}: {e}"}

    prompt = f"""
I have generated {doc_format} documentation for the '{api_name}' API based on the provided specification.
The generated documentation is located at: {output_file_path}

Please review the generated documentation, ensure its accuracy and completeness, and integrate it into the project's documentation system as needed.
You may need to add further explanations, examples, or formatting.
"""
    return {"llm_prompt": prompt, "output_path": output_file_path}
