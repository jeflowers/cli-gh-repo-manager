import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import github_repo_creator


class TestGitHubRepoCreator(unittest.TestCase):
    
    def setUp(self):
        self.mock_token = "mock_token"
        self.creator = github_repo_creator.GitHubRepoCreator(self.mock_token)
    
    @patch('requests.get')
    def test_validate_token_valid(self, mock_get):
        # Setup the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.creator.validate_token()
        
        # Assertions
        self.assertTrue(result)
        mock_get.assert_called_once_with("https://api.github.com/user", headers=self.creator.headers)
    
    @patch('requests.get')
    def test_validate_token_invalid(self, mock_get):
        # Setup the mock
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.creator.validate_token()
        
        # Assertions
        self.assertFalse(result)
        mock_get.assert_called_once_with("https://api.github.com/user", headers=self.creator.headers)
    
    @patch('requests.get')
    def test_get_username(self, mock_get):
        # Setup the mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"login": "testuser"}
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.creator.get_username()
        
        # Assertions
        self.assertEqual(result, "testuser")
        mock_get.assert_called_once_with("https://api.github.com/user", headers=self.creator.headers)
    
    @patch('requests.post')
    def test_create_repo(self, mock_post):
        # Setup the mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"name": "test-repo", "html_url": "https://github.com/testuser/test-repo"}
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.creator.create_repo("test-repo", "Test description", private=True)
        
        # Assertions
        self.assertEqual(result["name"], "test-repo")
        self.assertEqual(result["html_url"], "https://github.com/testuser/test-repo")
        mock_post.assert_called_once()


if __name__ == '__main__':
    unittest.main()
