import unittest
import os
import sys

# Add the scripts directory to the Python path to allow importing the script to be tested
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from spec_parser import parse_spec

VALID_SPEC_YAML = """
openapi: 3.0.0
info:
  title: Simple API
  version: 1.0.0
paths:
  /users:
    get:
      summary: Get all users
      responses:
        '200':
          description: A list of users.
"""

INVALID_SPEC_YAML = """
openapi: 3.0.0
info:
  title: Simple API
  version: 1.0.0
paths:
  /users
    get:
      summary: Get all users
"""

class TestSpecParser(unittest.TestCase):

    def test_parse_valid_spec(self):
        """
        Tests that a valid YAML OpenAPI spec is parsed correctly.
        """
        result = parse_spec(VALID_SPEC_YAML)
        
        self.assertIn('parsed_data', result)
        self.assertNotIn('error', result)
        
        parsed_data = result['parsed_data']
        self.assertEqual(parsed_data['info']['title'], 'Simple API')
        self.assertIn('/users', parsed_data['endpoints'])
        self.assertIn('get', parsed_data['endpoints']['/users'])
        self.assertEqual(parsed_data['endpoints']['/users']['get']['summary'], 'Get all users')

    def test_parse_invalid_spec(self):
        """
        Tests that an invalid YAML spec returns a structured error.
        """
        result = parse_spec(INVALID_SPEC_YAML)
        
        self.assertIn('error', result)
        self.assertNotIn('parsed_data', result)
        self.assertTrue('Failed to parse spec content' in result['error'])

    def test_infer_format(self):
        """
        Tests that the parser can infer the format correctly (YAML in this case).
        """
        result = parse_spec(VALID_SPEC_YAML, spec_format=None) # Explicitly test inference
        
        self.assertIn('parsed_data', result)
        self.assertEqual(result['parsed_data']['info']['title'], 'Simple API')

if __name__ == '__main__':
    unittest.main()
