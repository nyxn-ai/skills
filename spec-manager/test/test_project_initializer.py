import unittest
import os
import shutil
import sys
from unittest.mock import patch

# Add the scripts directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

import project_initializer

class TestProjectInitializer(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_root = os.path.join(os.path.dirname(__file__), "test_project_root")
        os.makedirs(self.test_root, exist_ok=True)
        self.openspec_dir = os.path.join(self.test_root, 'openspec')

    def tearDown(self):
        # Clean up the temporary directory after each test
        if os.path.exists(self.test_root):
            shutil.rmtree(self.test_root)

    def test_init_spec_project_success(self):
        result = project_initializer.init_spec_project(self.test_root)
        self.assertTrue(result["success"])
        self.assertIn("initialized", result["message"])

        self.assertTrue(os.path.isdir(self.openspec_dir))
        self.assertTrue(os.path.isdir(os.path.join(self.openspec_dir, 'specs')))
        self.assertTrue(os.path.isdir(os.path.join(self.openspec_dir, 'changes')))
        self.assertTrue(os.path.exists(os.path.join(self.openspec_dir, 'project.md')))
        self.assertTrue(os.path.exists(os.path.join(self.openspec_dir, 'constitution.md')))

        with open(os.path.join(self.openspec_dir, 'project.md'), 'r') as f:
            content = f.read()
            self.assertIn("# Project Context", content)
        
        with open(os.path.join(self.openspec_dir, 'constitution.md'), 'r') as f:
            content = f.read()
            self.assertIn("# Project Principles", content)

    def test_define_principles_success(self):
        project_initializer.init_spec_project(self.test_root) # Ensure project is initialized
        principles_content = "New guiding principles for the project."
        result = project_initializer.define_principles(principles_content, self.test_root)
        self.assertTrue(result["success"])
        self.assertIn("updated", result["message"])

        constitution_path = os.path.join(self.openspec_dir, 'constitution.md')
        self.assertTrue(os.path.exists(constitution_path))
        with open(constitution_path, 'r') as f:
            content = f.read()
            self.assertEqual(content, principles_content)

    def test_define_principles_project_not_initialized(self):
        principles_content = "New guiding principles for the project."
        result = project_initializer.define_principles(principles_content, self.test_root) # Project not initialized
        self.assertFalse(result["success"])
        self.assertIn("not initialized", result["message"])

    @patch('project_initializer.os.makedirs', side_effect=OSError("Disk full"))
    def test_init_spec_project_failure(self, mock_makedirs):
        result = project_initializer.init_spec_project(self.test_root)
        self.assertFalse(result["success"])
        self.assertIn("Disk full", result["message"])

    @patch('builtins.open', side_effect=OSError("Permission denied"))
    def test_define_principles_write_failure(self, mock_open):
        project_initializer.init_spec_project(self.test_root) # Ensure project is initialized
        principles_content = "New guiding principles for the project."
        result = project_initializer.define_principles(principles_content, self.test_root)
        self.assertFalse(result["success"])
        self.assertIn("Permission denied", result["message"])

if __name__ == '__main__':
    unittest.main()
