import re


class ChangelogUpdater:
    def __init__(
        self, github_api, changelog_file, owner, repo, front_matter, pull_request_number
    ):
        self.github_api = github_api
        self.changelog_file = changelog_file
        self.owner = owner
        self.repo = repo
        self.front_matter = front_matter
        self.pull_request_number = pull_request_number

    def collect_issue_references(self, body, title, commits_url):
        messages = []
        numbers = re.findall(r"#(\d+)", body)
        if not numbers:
            numbers = re.findall(r"#(\d+)", title)
        if not numbers:
            commits = self.github_api.fetch_commits(commits_url)
            numbers = []
            for c in commits:
                if c["commit"]["message"]:
                    refs = re.findall(r"#(\d+)", c["commit"]["message"])
                    if refs:
                        if refs[0] not in numbers:
                            numbers.append(refs[0])
                    else:
                        if c["commit"]["message"] not in messages:
                            messages.append(c["commit"]["message"])
        list = []
        for n in numbers:
            list.append(int(n))
        return list, messages

    def generate_changelog_issues(self, issues, messages):
        issue_list = []

        for issue in issues:
            entry = f"- {issue['title']} ([#{issue['number']}]({issue["html_url"]}))"
            issue_list.append(entry)

        for message in messages:
            entry = f"- {message}"
            issue_list.append(entry)

        return "\n".join(issue_list)

    def get_build_from_artifact(self, merge_commit_sha, artifacts):
        builds = []
        for artifact in artifacts:
            if f"_{merge_commit_sha[:7]}" in artifact["name"]:
                builds.append(artifact["name"].split(" ")[1].split("_")[0])
        return builds

    def write_changelog(self, entries):
        # Write new entries at the top followed by existing content
        with open(self.changelog_file, "w") as file:
            if self.front_matter:
                file.write(f"{self.front_matter}\n\n")
            file.write("# Changelog\n\n")
            file.write("\n\n".join(entries))

    def update_changelog(self, entries):
        with open(self.changelog_file, "r") as file:
            content = file.read()
            # Replace existing frontmatter
            if self.front_matter:
                if re.search(r"---(.|\n)*---", content):
                    content = re.sub(r"---(.|\n)*---", self.front_matter, content)
                else:
                    content = f"{self.front_matter}\n\n{content}"
            # insert new entries at the top after existing Changelog title
            content = re.sub(
                r"# Changelog", f"# Changelog\n\n{'\n\n'.join(entries)}", content
            )
        with open(self.changelog_file, "w") as file:
            file.write(content)

    def generate_changelog(self):
        try:
            with open(self.changelog_file, "r") as file:
                file.read()
        except FileNotFoundError:
            self.pull_request_number = None
        if self.pull_request_number:
            issues = []
            prs = self.github_api.fetch_pull_request()
            pr = prs[0]
            pr_issue_numbers, messages = self.collect_issue_references(
                pr["body"], pr["title"], pr["commits_url"]
            )
            if pr_issue_numbers:
                for i in pr_issue_numbers:
                    issue = self.github_api.fetch_issue(i)
                    if issue:
                        issues.append(issue)
        else:
            prs = self.github_api.fetch_pull_requests()
            issues = self.github_api.fetch_issues()
        artifacts = self.github_api.fetch_artifacts()
        changelog_entries = []
        for pr in prs:
            if pr["merge_commit_sha"] is not None:
                print(f"Processing PR#{pr['number']} - {pr['title']}")
                builds = self.get_build_from_artifact(pr["merge_commit_sha"], artifacts)
                if pr["body"] is not None:
                    pr_issue_numbers, messages = self.collect_issue_references(
                        pr["body"], pr["title"], pr["commits_url"]
                    )
                    pr_issues = []
                    for pri in pr_issue_numbers:
                        issue = None
                        for i in issues:
                            if i["number"] == pri:
                                issue = i
                                break
                        if issue:
                            pr_issues.append(issue)
                    changelog_issues = self.generate_changelog_issues(
                        pr_issues, messages
                    )
                    if not pr["merged_at"]:
                        pr["merged_at"] = pr["closed_at"]
                    if builds:
                        builds = sorted(builds, reverse=True)
                        version_string = f"Builds: {', '.join(builds)}"
                    else:
                        version_string = ""
                    changelog_entry = f"### [PR#{pr["number"]}]({pr["html_url"]}) ({pr["merged_at"].replace("T"," ").replace("Z","")} - [{pr["merge_commit_sha"][:7]}](https://github.com/{self.owner}/{self.repo}/commit/{pr["merge_commit_sha"][:7]}) - {version_string})\n{changelog_issues}"
                    changelog_entries.append(changelog_entry)
        if self.pull_request_number:
            self.update_changelog(changelog_entries)
        else:
            self.write_changelog(changelog_entries)
        print("Changelog updated successfully.")
