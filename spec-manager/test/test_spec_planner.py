import unittest
import os
import shutil
import sys
import json
from unittest.mock import patch, mock_open

# Add the scripts directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

import spec_planner

class TestSpecPlanner(unittest.TestCase):

    def setUp(self):
        self.test_root = os.path.join(os.path.dirname(__file__), "test_project_root_planner")
        self.change_id = "test-feature"
        self.openspec_dir = os.path.join(self.test_root, 'openspec')
        self.change_dir = os.path.join(self.openspec_dir, 'changes', self.change_id)

        os.makedirs(os.path.join(self.change_dir, 'specs'), exist_ok=True)
        # Create a dummy constitution.md and project.md for realistic setup
        os.makedirs(self.openspec_dir, exist_ok=True)
        with open(os.path.join(self.openspec_dir, 'constitution.md'), 'w') as f:
            f.write("# Project Principles\n\nSome principles.")
        with open(os.path.join(self.openspec_dir, 'project.md'), 'w') as f:
            f.write("# Project Context\n\nSome context.")

    def tearDown(self):
        if os.path.exists(self.test_root):
            shutil.rmtree(self.test_root)

    def test_generate_plan_success(self):
        result = spec_planner.generate_plan(self.change_id, self.test_root)
        self.assertIsNotNone(result["llm_prompt"])
        self.assertIsNotNone(result["plan_path"])
        self.assertIsNone(result["error"])

        plan_file_path = os.path.join(self.change_dir, 'plan.md')
        self.assertTrue(os.path.exists(plan_file_path))
        with open(plan_file_path, 'r') as f:
            content = f.read()
            self.assertIn(f"# Implementation Plan for {self.change_id}", content)

    def test_breakdown_tasks_success(self):
        result = spec_planner.breakdown_tasks(self.change_id, self.test_root)
        self.assertIsNotNone(result["llm_prompt"])
        self.assertIsNotNone(result["tasks_path"])
        self.assertIsNone(result["error"])

        tasks_file_path = os.path.join(self.change_dir, 'tasks.md')
        self.assertTrue(os.path.exists(tasks_file_path))
        with open(tasks_file_path, 'r') as f:
            content = f.read()
            self.assertIn(f"# Tasks for {self.change_id}", content)

    @patch('spec_planner.os.makedirs', side_effect=OSError("Disk full"))
    def test_generate_plan_failure(self, mock_makedirs):
        result = spec_planner.generate_plan(self.change_id, self.test_root)
        self.assertIsNone(result["llm_prompt"])
        self.assertIsNone(result["plan_path"])
        self.assertIsNotNone(result["error"])
        self.assertIn("Disk full", result["error"])

    @patch('spec_planner.os.makedirs', side_effect=OSError("Disk full"))
    def test_breakdown_tasks_failure(self, mock_makedirs):
        result = spec_planner.breakdown_tasks(self.change_id, self.test_root)
        self.assertIsNone(result["llm_prompt"])
        self.assertIsNone(result["tasks_path"])
        self.assertIsNotNone(result["error"])
        self.assertIn("Disk full", result["error"])

if __name__ == '__main__':
    unittest.main()
