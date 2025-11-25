# spec-manager/scripts/spec_comparer.py
import json
import yaml
from deepdiff import DeepDiff # Need to add deepdiff to requirements.txt

def _load_spec_data(spec_content, spec_format=None):
    if spec_format and spec_format.lower() in ['json', 'openapi', 'swagger']:
        return json.loads(spec_content)
    elif spec_format and spec_format.lower() in ['yaml', 'asyncapi']:
        return yaml.safe_load(spec_content)
    else: # Attempt to infer
        try:
            return json.loads(spec_content)
        except json.JSONDecodeError:
            return yaml.safe_load(spec_content)

def compare_specs(spec_content_a, spec_content_b, spec_format=None):
    """
    Compares two API specifications to identify differences.
    """
    error = None
    diff_report = None

    try:
        spec_a = _load_spec_data(spec_content_a, spec_format)
        spec_b = _load_spec_data(spec_content_b, spec_format)
        
        diff = DeepDiff(spec_a, spec_b, ignore_order=True, verbose_level=2)
        
        diff_report = {
            "has_changes": bool(diff),
            "details": diff.to_json() # DeepDiff provides a comprehensive JSON output
        }

    except (json.JSONDecodeError, yaml.YAMLError) as e:
        error = f"Failed to parse spec content for comparison: Invalid JSON or YAML: {e}"
    except Exception as e:
        error = f"An unexpected error occurred during spec comparison: {e}"
    
    if error:
        return {"error": error}
    return {"diff_report": diff_report}

# Note: This script requires the 'deepdiff' library.
# It should be added to the skill's requirements.txt
