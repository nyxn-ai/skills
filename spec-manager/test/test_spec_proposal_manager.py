import unittest
import os
import shutil
import sys
import json
from unittest.mock import patch

# Add the scripts directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

import spec_proposal_manager

class TestSpecProposalManager(unittest.TestCase):

    def setUp(self):
        self.test_root = os.path.join(os.path.dirname(__file__), "test_project_root_proposal")
        self.change_id = "test-new-feature"
        self.proposed_changes_description = "Add a new user authentication flow."
        self.openspec_dir = os.path.join(self.test_root, 'openspec')
        self.changes_dir = os.path.join(self.openspec_dir, 'changes')
        self.change_dir = os.path.join(self.changes_dir, self.change_id)
        self.main_specs_dir = os.path.join(self.openspec_dir, 'specs')
        self.archive_dir = os.path.join(self.openspec_dir, 'archive')

        # Ensure openspec structure exists for tests
        os.makedirs(self.main_specs_dir, exist_ok=True)
        os.makedirs(self.changes_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_root):
            shutil.rmtree(self.test_root)

    def test_create_change_proposal_success(self):
        result = spec_proposal_manager.create_change_proposal(self.proposed_changes_description, self.test_root, self.change_id)
        self.assertIsNotNone(result["llm_prompt"])
        self.assertEqual(result["proposal_path"], self.change_dir)
        self.assertIsNone(result["error"])

        self.assertTrue(os.path.isdir(self.change_dir))
        self.assertTrue(os.path.isdir(os.path.join(self.change_dir, 'specs')))
        self.assertTrue(os.path.exists(os.path.join(self.change_dir, 'proposal.md')))
        self.assertTrue(os.path.exists(os.path.join(self.change_dir, 'tasks.md')))
        self.assertTrue(os.path.exists(os.path.join(self.change_dir, 'specs', 'spec.md')))

        with open(os.path.join(self.change_dir, 'proposal.md'), 'r') as f:
            content = f.read()
            self.assertIn(f"# Change Proposal: {self.change_id}", content)
            self.assertIn(self.proposed_changes_description, content)

    def test_archive_change_proposal_success(self):
        # First, create a proposal
        self.test_create_change_proposal_success()

        # Simulate some content in the spec delta
        with open(os.path.join(self.change_dir, 'specs', 'spec.md'), 'w') as f:
            f.write("Updated spec content for new feature.")

        result = spec_proposal_manager.archive_change_proposal(self.change_id, self.test_root)
        self.assertTrue(result["success"])
        self.assertIn("archived successfully", result["message"])
        self.assertIsNotNone(result["updated_main_spec_path"])

        # Check if change directory is moved to archive
        self.assertFalse(os.path.exists(self.change_dir))
        self.assertTrue(os.path.isdir(os.path.join(self.archive_dir, self.change_id)))

        # Check if spec is copied to main specs directory
        expected_main_spec_path = os.path.join(self.main_specs_dir, f"{self.change_id}_spec.md")
        self.assertTrue(os.path.exists(expected_main_spec_path))
        with open(expected_main_spec_path, 'r') as f:
            content = f.read()
            self.assertEqual(content, "Updated spec content for new feature.")

    def test_archive_change_proposal_not_found(self):
        result = spec_proposal_manager.archive_change_proposal(self.change_id, self.test_root)
        self.assertFalse(result["success"])
        self.assertIn("not found", result["message"])

    @patch('spec_proposal_manager.os.makedirs', side_effect=OSError("Disk full"))
    def test_create_change_proposal_failure(self, mock_makedirs):
        result = spec_proposal_manager.create_change_proposal(self.proposed_changes_description, self.test_root, self.change_id)
        self.assertIsNone(result["llm_prompt"])
        self.assertIsNone(result["proposal_path"])
        self.assertIsNotNone(result["error"])
        self.assertIn("Disk full", result["error"])

    @patch('spec_proposal_manager.shutil.move', side_effect=OSError("Permission denied"))
    def test_archive_change_proposal_failure(self, mock_move):
        self.test_create_change_proposal_success() # Create some files to archive
        result = spec_proposal_manager.archive_change_proposal(self.change_id, self.test_root)
        self.assertFalse(result["success"])
        self.assertIn("Permission denied", result["message"])

if __name__ == '__main__':
    unittest.main()
