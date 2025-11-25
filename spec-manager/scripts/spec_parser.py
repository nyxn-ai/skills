# spec-manager/scripts/spec_parser.py
import json
import yaml

def parse_spec(spec_content, spec_format=None):
    """
    Parses the given API specification content and extracts key information.
    Currently, this is a basic parser for OpenAPI/Swagger-like structures.
    """
    parsed_data = {}
    error = None

    try:
        if spec_format and spec_format.lower() in ['json', 'openapi', 'swagger']:
            data = json.loads(spec_content)
        elif spec_format and spec_format.lower() in ['yaml', 'asyncapi']:
            data = yaml.safe_load(spec_content)
        else: # Attempt to infer
            try:
                data = json.loads(spec_content)
            except json.JSONDecodeError:
                data = yaml.safe_load(spec_content)
        
        # Basic extraction for OpenAPI/Swagger
        parsed_data['info'] = data.get('info', {})
        parsed_data['servers'] = data.get('servers', [])
        
        endpoints = {}
        paths = data.get('paths', {})
        for path, path_item in paths.items():
            methods = {}
            for method, operation in path_item.items():
                if method.lower() in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                    methods[method.lower()] = {
                        'summary': operation.get('summary'),
                        'description': operation.get('description'),
                        'operation_id': operation.get('operationId'),
                        'parameters': operation.get('parameters', []),
                        'request_body': operation.get('requestBody'),
                        'responses': operation.get('responses', {})
                    }
            if methods:
                endpoints[path] = methods
        parsed_data['endpoints'] = endpoints
        
        parsed_data['components'] = data.get('components', {})

    except (json.JSONDecodeError, yaml.YAMLError) as e:
        error = f"Failed to parse spec content: Invalid JSON or YAML: {e}"
    except Exception as e:
        error = f"An unexpected error occurred during spec parsing: {e}"
    
    if error:
        return {"error": error}
    return {"parsed_data": parsed_data}
