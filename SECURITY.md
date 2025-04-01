# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the severity of the vulnerability.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

Please report (suspected) security vulnerabilities via the repository Issues with the "Security" label. You will receive a response from the maintainers within 48 hours. If the issue is confirmed, we will release a patch as soon as possible depending on complexity.

## Security Best Practices for Users

1. **Token Security**: Never hardcode your GitHub token in scripts or share it with others. Use environment variables or secure credential storage.

2. **Minimum Permissions**: Create GitHub tokens with the minimum required permissions for this tool (typically just the `repo` scope).

3. **Token Rotation**: Regularly rotate your GitHub personal access tokens.

4. **Secure Communication**: Always use HTTPS when communicating with GitHub's API (this tool enforces this).

5. **Code Review**: Review any changes to this tool before using a new version, especially if you're using it in automated workflows.

## Security Features

- The tool uses HTTPS for all API communications
- Tokens are never logged or displayed in plain text
- The tool supports retrieving tokens from environment variables rather than command line arguments
