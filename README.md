# Workflow Migrator

## Overview
**Workflow Migrator** is a GitHub App designed to automate the migration of CI/CD pipelines from GitLab to GitHub Actions. This tool reads `.gitlab-ci.yml` files and converts them into GitHub Actions workflow syntax, facilitating a seamless transition for projects moving from GitLab to GitHub.

## Features
- **Automatic Conversion**: Converts `.gitlab-ci.yml` to `.github/workflows/main.yml`.
- **Pull Request Creation**: Automatically creates pull requests with the new GitHub Actions workflows into the target repositories.
- **Multi-Repository Support**: Supports the migration of multiple repositories listed in an issue body.

## How to Use
1. Install the GitHub App to your desired repository.
2. Open an issue using the provided template.
3. Comment `/migrate-workflows` on the issue to trigger the migration.
4. The app will convert all listed GitLab CI configurations to GitHub Actions workflows and create pull requests.

## Installation
To install the app, navigate to the [GitHub App installation page](https://github.com/mshubham2007/workflow-migrator/settings/installations).

## Contributing
Contributions are welcome! Please read the `CONTRIBUTING.md` for instructions on how to submit pull requests.

## License
Distributed under the MIT License. See `LICENSE` for more information.
