# spec-manager/scripts/spec_fetcher.py
import requests
import os
import yaml
import json

def fetch_spec(source_path, spec_format=None):
    """
    Fetches API specification content from a local file path or a remote URL.
    """
    spec_content = None
    error = None

    try:
        if source_path.startswith('http://') or source_path.startswith('https://'):
            response = requests.get(source_path)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            spec_content = response.text
        else:
            with open(source_path, 'r', encoding='utf-8') as f:
                spec_content = f.read()
    except requests.exceptions.RequestException as e:
        error = f"Failed to fetch remote spec from {source_path}: {e}"
    except FileNotFoundError:
        error = f"Local spec file not found at {source_path}"
    except Exception as e:
        error = f"An unexpected error occurred while fetching spec: {e}"

    if error:
        return {"error": error}

    # Attempt to infer format if not provided
    if spec_format is None and spec_content:
        try:
            json.loads(spec_content)
            spec_format = "OpenAPI" # Assuming JSON is often OpenAPI
        except json.JSONDecodeError:
            try:
                yaml.safe_load(spec_content)
                spec_format = "OpenAPI" # Assuming YAML is often OpenAPI
            except yaml.YAMLError:
                # Could be other formats, or invalid
                pass

    return {"spec_content": spec_content, "spec_format": spec_format}
