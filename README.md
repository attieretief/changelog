# Changelog Updater Action

This GitHub Action updates the changelog based on merged pull requests and referenced issues. It automates the process of keeping your changelog up to date, ensuring that your project documentation reflects the latest changes.

## Table of Contents

- [Changelog Updater Action](#changelog-updater-action)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
  - [Inputs](#inputs)
  - [Example](#example)
  - [License](#license)

## Usage

To use this action in your GitHub workflow, include the following in your workflow YAML file:

```yaml
uses: your-username/changelog-updater@v1
with:
  github_token: ${{ secrets.GITHUB_TOKEN }}
  changelog_file: CHANGELOG.md
  pull_request_body: ${{ github.event.pr.body }}
  build_number: ${{ env.build_number }}
  merged_at: ${{ github.event.pr.merged_at }}
```

## Inputs

- `github_token`: **Required**. A GitHub token for authentication. This token is used to access the GitHub API and fetch merged pull requests and issues.
- `changelog_file`: **Optional**. The path to the changelog file. Defaults to `CHANGELOG.md`.
- `pull_request_body`: **Required**. The body of the pull request that triggered the action. Used to extract issue references from.
- `build_number`: **Required**. The build number to create the changelog entry for.
- `merged_at`; **Required**. The date for the changelog entry.

## Example

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
        uses: attieretief/changelog-updater@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          changelog_file: CHANGELOG.md
          pull_request_body: ${{ github.event.pr.body }}
          build_number: ${{ env.build_number }}
          merged_at: ${{ github.event.pr.merged_at }}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.