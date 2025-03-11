# Changelog Updater Action

This GitHub Action generates or updates a changelog markdown file based on merged pull requests and referenced issues. It automates the process of keeping your changelog up to date, ensuring that your project documentation reflects the latest changes.

## Table of Contents

- [Changelog Updater Action](#changelog-updater-action)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
    - [Job](#job)
    - [Inputs](#inputs)
    - [Example](#example)
  - [License](#license)

## Usage

### Job

uses: attieretief/changelog-updater@v1

### Inputs

- `github_token`: **Required**. A GitHub token for authentication. This token is used to access the GitHub API and fetch merged pull requests and issues.
- `changelog_file`: **Optional**. The path to the changelog file. Defaults to `CHANGELOG.md`.
- `front_matter`: **Optional**. Front matter to include in the changelog. Defaults to `---\n---\n\n`.
- `owner`: **Required**. Repository owner. Defaults to `${{ github.repository_owner }}`.
- `repository`: **Required**. Repository name. Defaults to `${{ github.repository }}`.
- `pull_request_number`: **Optional**. Pull request number. If one is provided, the changelog will be updated with just the information from this pull request. If not, the changelog will be regenerated.

### Example

Here is an example of how to configure the action in your workflow:

```yaml
name: Update Changelog

on:
  push:
    branches:
      - main

jobs:
  update-changelog:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Update Changelog
        uses: attieretief/changelog@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          changelog_file: CHANGELOG.md
          front_matter: |
            ---
            ---
          owner: ${{ github.repository_owner }}
          repository: ${{ github.repository }}
          pull_request_number: ${{ github.event.pull_request.number }}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.