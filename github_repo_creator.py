#!/usr/bin/env python3
"""
GitHub Repository Creator CLI

A command-line tool to create a GitHub repository from a local Git repository.
"""

import argparse
import os
import subprocess
import sys
import requests
import json
import getpass
from typing import Dict, Any, Optional, List, Tuple


class GitHubRepoCreator:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.api_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def validate_token(self) -> bool:
        """Validate the GitHub token by making a test API call."""
        if not self.token:
            return False

        response = requests.get(f"{self.api_url}/user", headers=self.headers)
        return response.status_code == 200

    def get_username(self) -> str:
        """Get the authenticated user's GitHub username."""
        response = requests.get(f"{self.api_url}/user", headers=self.headers)
        response.raise_for_status()
        return response.json()["login"]

    def create_repo(self, name: str, description: str = "", private: bool = False,
                    auto_init: bool = False, gitignore_template: str = None,
                    license_template: str = None) -> Dict[Any, Any]:
        """Create a new GitHub repository."""
        data = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": auto_init,
        }

        if gitignore_template:
            data["gitignore_template"] = gitignore_template

        if license_template:
            data["license_template"] = license_template

        response = requests.post(f"{self.api_url}/user/repos", 
                                headers=self.headers, 
                                data=json.dumps(data))
        
        response.raise_for_status()
        return response.json()

    def check_git_repo(self, repo_path: str) -> bool:
        """Check if the given path is a Git repository."""
        return os.path.isdir(os.path.join(repo_path, ".git"))

    def configure_remote(self, repo_path: str, remote_url: str, remote_name: str = "origin") -> bool:
        """Configure the remote for the local repository."""
        try:
            # Check if remote already exists
            result = subprocess.run(
                ["git", "remote", "get-url", remote_name],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                # Remote exists, update it
                subprocess.run(
                    ["git", "remote", "set-url", remote_name, remote_url],
                    cwd=repo_path,
                    check=True
                )
            else:
                # Remote doesn't exist, add it
                subprocess.run(
                    ["git", "remote", "add", remote_name, remote_url],
                    cwd=repo_path,
                    check=True
                )
            return True
        except subprocess.CalledProcessError:
            return False

    def push_to_remote(self, repo_path: str, remote_name: str = "origin", branch: str = "main") -> bool:
        """Push the local repository to the remote."""
        try:
            # Get the current branch if none specified
            if not branch:
                result = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=repo_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                branch = result.stdout.strip()

            # Push to remote
            subprocess.run(
                ["git", "push", "-u", remote_name, branch],
                cwd=repo_path,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Create a GitHub repository from a local Git repository")
    
    parser.add_argument("path", help="Path to the local Git repository", nargs="?", default=".")
    parser.add_argument("--name", "-n", help="Name for the GitHub repository (defaults to folder name)")
    parser.add_argument("--description", "-d", help="Repository description", default="")
    parser.add_argument("--private", "-p", action="store_true", help="Create a private repository")
    parser.add_argument("--token", "-t", help="GitHub personal access token (can also use GITHUB_TOKEN env var)")
    parser.add_argument("--remote", "-r", default="origin", help="Name of the remote (default: origin)")
    parser.add_argument("--branch", "-b", help="Branch to push (default: current branch)")
    parser.add_argument("--no-push", action="store_true", help="Don't push to the new repository")
    
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()
    
    # Get absolute path
    repo_path = os.path.abspath(args.path)
    
    # Create GitHub client
    github = GitHubRepoCreator(args.token)
    
    # Validate token
    if not github.validate_token():
        token = getpass.getpass("GitHub Personal Access Token: ")
        github.token = token
        github.headers["Authorization"] = f"Bearer {token}"
        
        if not github.validate_token():
            print("Error: Invalid GitHub token. Please provide a valid token.")
            sys.exit(1)
    
    # Check if path is a Git repository
    if not github.check_git_repo(repo_path):
        print(f"Error: {repo_path} is not a Git repository.")
        sys.exit(1)
    
    # Determine repository name
    repo_name = args.name
    if not repo_name:
        repo_name = os.path.basename(repo_path)
        print(f"Using directory name as repository name: {repo_name}")
    
    try:
        # Create repository
        print(f"Creating GitHub repository: {repo_name}")
        repo_info = github.create_repo(
            name=repo_name,
            description=args.description,
            private=args.private
        )
        
        print(f"Repository created successfully: {repo_info['html_url']}")
        
        # Configure remote
        remote_url = repo_info["clone_url"]
        if github.configure_remote(repo_path, remote_url, args.remote):
            print(f"Remote '{args.remote}' configured to: {remote_url}")
        else:
            print(f"Error: Failed to configure remote '{args.remote}'.")
            sys.exit(1)
        
        # Push to remote
        if not args.no_push:
            print(f"Pushing to remote '{args.remote}'...")
            if github.push_to_remote(repo_path, args.remote, args.branch):
                print("Push successful!")
            else:
                print("Error: Failed to push to remote.")
                sys.exit(1)
    
    except requests.exceptions.HTTPError as e:
        print(f"GitHub API Error: {e.response.json().get('message', str(e))}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()