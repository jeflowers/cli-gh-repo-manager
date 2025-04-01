# GitHub Repository Creator CLI

![GitHub License](https://img.shields.io/github/license/jeflowers/cli-gh-repo-manager)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jeflowers/cli-gh-repo-manager/python-tests.yml?branch=main&label=tests)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A powerful command-line tool that simplifies creating and managing GitHub repositories from local Git repositories. Say goodbye to the tedious process of manually creating repositories and configuring remotes!

## 🚀 Features

- **One-Command Repository Creation**: Create a GitHub repository and link it to your local Git repository with a single command
- **Smart Detection**: Automatically determines repository name from local directory
- **Remote Configuration**: Automatically configures Git remotes for your local repository
- **Initial Push Support**: Pushes your code to the new repository right away
- **Private Repository Support**: Create private repositories with a simple flag
- **Flexible Configuration**: Customize repository settings, remote names, and branches
- **Secure Token Handling**: Multiple secure options for providing GitHub authentication

## 📋 Prerequisites

- Python 3.6 or higher
- Git installed and configured
- A GitHub account
- A GitHub Personal Access Token with `repo` scope (see [Creating a PAT](#creating-a-github-personal-access-token))

## 🔧 Installation

### Using pip (Recommended)

```bash
pip install github-repo-creator
```

### Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/jeflowers/cli-gh-repo-manager.git
   cd cli-gh-repo-manager
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make the script executable (Unix/Linux/macOS):
   ```bash
   chmod +x github_repo_creator.py
   ```

## 📖 Usage

### Basic Usage

```bash
# Create a GitHub repo from the current directory
github-repo-creator

# Create a GitHub repo from a specific directory
github-repo-creator /path/to/your/repo
```

### Advanced Options

```bash
# Create a private repository with a custom name and description
github-repo-creator --name my-awesome-project \
                   --description "This is my awesome project" \
                   --private

# Use a specific GitHub token
github-repo-creator --token YOUR_GITHUB_TOKEN

# Use a different remote name and branch
github-repo-creator --remote upstream --branch dev

# Configure the remote but don't push
github-repo-creator --no-push
```

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--name`, | `-n` | Name for the GitHub repository | Directory name |
| `--description` | `-d` | Repository description | "" |
| `--private` | `-p` | Create a private repository | False |
| `--token` | `-t` | GitHub personal access token | GITHUB_TOKEN env var |
| `--remote` | `-r` | Name of the remote | "origin" |
| `--branch` | `-b` | Branch to push | Current branch |
| `--no-push` | | Don't push to the new repository | False |

### Environment Variables

You can set your GitHub token as an environment variable for convenience and security:

```bash
export GITHUB_TOKEN=your_github_token
github-repo-creator
```

## 🔐 Creating a GitHub Personal Access Token

1. Log in to your GitHub account
2. Go to **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**
3. Click **Generate new token** and select **Generate new token (classic)**
4. Give your token a descriptive name (e.g., "GitHub Repo Creator CLI")
5. Select the `repo` scope (for repository operations)
6. Click **Generate token**
7. **IMPORTANT**: Copy the generated token immediately. GitHub will only show it once!

## 🛡️ Security Best Practices

- Never hardcode your GitHub token in scripts
- Use environment variables or the `--token` option to provide your token
- Store your token securely and rotate it regularly
- Use a token with the minimum required permissions
- Consider using a credential manager for your tokens

## 🧪 Development

### Running Tests

```bash
pytest
```

### Code Style

This project follows the Black code style. To format your code:

```bash
pip install black
black .
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the contribution process.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [GitHub REST API](https://docs.github.com/en/rest) for providing the endpoints used by this tool
- Python's `argparse` for making command-line argument parsing a breeze
- All our contributors and supporters
