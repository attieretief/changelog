import requests


class GitHubAPI:
    def __init__(self, token, owner, repo, pull_request_number):
        self.token = token
        self.base_url = "https://api.github.com"
        self.owner = owner
        self.repo = repo
        self.pull_request_number = pull_request_number

    def fetch_pull_request(self):
        print(f"Fetching pull request: {self.pull_request_number}")
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls/{self.pull_request_number}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return [response.json()]
        return {}

    def fetch_issue(self, issue_number):
        print(f"Fetching issue: {issue_number}")
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        return {}

    def fetch_pull_requests(self, page=1):
        print("Fetching pull requests")
        print(f"Page: {page}")
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls?per_page=100&page={page}"
        headers = {"Authorization": f"token {self.token}"}
        params = {
            "state": "closed",
            "sort": "updated",
            "direction": "desc",
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 200:
            result = response.json()
            if response.headers.get("link"):
                links = response.headers["link"].split(",")
                for link in links:
                    if 'rel="next"' in link:
                        result = result + self.fetch_pull_requests(page + 1)
        return result

    def fetch_issues(self, page=1):
        print("Fetching issues")
        print(f"Page: {page}")
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues?per_page=100&page={page}"
        headers = {"Authorization": f"token {self.token}"}
        params = {
            "state": "all",
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 200:
            result = response.json()
            if response.headers.get("link"):
                links = response.headers["link"].split(",")
                for link in links:
                    if 'rel="next"' in link:
                        result = result + self.fetch_issues(page + 1)
        return result

    def fetch_artifacts(self, page=1):
        print("Fetching artifacts")
        print(f"Page: {page}")
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/actions/artifacts?per_page=100&page={page}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            result = response.json()["artifacts"]
            if response.headers.get("link"):
                links = response.headers["link"].split(",")
                for link in links:
                    if 'rel="next"' in link:
                        result = result + self.fetch_artifacts(page + 1)
        return result

    def fetch_commits(self, url):
        url = f"{url}?per_page=100"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        return []
