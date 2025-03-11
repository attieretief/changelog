def main():
    import os
    import sys
    from changelog_updater import ChangelogUpdater
    from github_api import GitHubAPI
    import dotenv

    dotenv.load_dotenv()

    # Get inputs from environment variables
    github_token = os.getenv("INPUT_GITHUB_TOKEN")
    changelog_file = os.getenv("INPUT_CHANGELOG_FILE", "CHANGELOG.md")
    owner = os.getenv("INPUT_OWNER")
    repository = os.getenv("INPUT_REPOSITORY")
    front_matter = os.getenv("INPUT_FRONT_MATTER")
    pull_request_number = os.getenv("INPUT_PULL_REQUEST_NUMBER")

    if not github_token:
        print("Error: GitHub token is required.")
        sys.exit(1)

    # Initialize GitHub API and Changelog Updater
    github_api = GitHubAPI(github_token, owner, repository, pull_request_number)
    generator = ChangelogUpdater(
        github_api, changelog_file, owner, repository, front_matter, pull_request_number
    )

    # Update the changelog
    generator.generate_changelog()


if __name__ == "__main__":
    main()
