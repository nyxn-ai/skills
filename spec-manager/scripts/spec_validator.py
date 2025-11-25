# spec-manager/scripts/spec_validator.py
import json
import yaml
import os

# Placeholder for a proper schema loader
# In a real implementation, you'd load the OpenAPI schema from resources
def load_openapi_schema():
    # For now, a very basic placeholder
    # Later: load from spec-manager/resources/schemas/openapi_v3.json
    return {
        "type": "object",
        "properties": {
            "openapi": {"type": "string", "pattern": "^3\\.0\\.[0-9]+$"},
            "info": {"type": "object", "required": ["title", "version"]},
            "paths": {"type": "object"}
        },
        "required": ["openapi", "info", "paths"]
    }

def validate_spec(spec_content, spec_format=None):
    """
    Validates the API specification against its standard.
    Currently a very basic validation for OpenAPI/Swagger.
    """
    is_valid = True
    validation_messages = []
    error = None

    try:
        if spec_format and spec_format.lower() in ['json', 'openapi', 'swagger']:
            spec_data = json.loads(spec_content)
        elif spec_format and spec_format.lower() in ['yaml', 'asyncapi']:
            spec_data = yaml.safe_load(spec_content)
        else: # Attempt to infer
            try:
                spec_data = json.loads(spec_content)
            except json.JSONDecodeError:
                spec_data = yaml.safe_load(spec_content)
        
        # Basic OpenAPI/Swagger validation
        if not isinstance(spec_data, dict):
            is_valid = False
            validation_messages.append("Spec content is not a valid object.")
            return {"is_valid": is_valid, "validation_messages": validation_messages}

        if "openapi" not in spec_data and "swagger" not in spec_data:
            is_valid = False
            validation_messages.append("Spec does not specify 'openapi' or 'swagger' version.")
        
        if "info" not in spec_data or not isinstance(spec_data["info"], dict):
            is_valid = False
            validation_messages.append("'info' object is missing or invalid.")
        else:
            if "title" not in spec_data["info"] or not spec_data["info"]["title"]:
                is_valid = False
                validation_messages.append("'info.title' is missing or empty.")
            if "version" not in spec_data["info"] or not spec_data["info"]["version"]:
                is_valid = False
                validation_messages.append("'info.version' is missing or empty.")

        if "paths" not in spec_data or not isinstance(spec_data["paths"], dict):
            is_valid = False
            validation_messages.append("'paths' object is missing or invalid.")
        elif not spec_data["paths"]:
            validation_messages.append("'paths' object is empty.")

        # More comprehensive validation would involve a proper JSON Schema validation
        # For now, this placeholder provides basic structural checks.

    except (json.JSONDecodeError, yaml.YAMLError) as e:
        is_valid = False
        validation_messages.append(f"Invalid JSON or YAML content: {e}")
    except Exception as e:
        is_valid = False
        validation_messages.append(f"An unexpected error occurred during validation: {e}")
    
    return {"is_valid": is_valid, "validation_messages": validation_messages}
