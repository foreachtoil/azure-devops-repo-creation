import requests
from requests.auth import HTTPBasicAuth
from modules.shared import get_environment_value

class DevOpsInterface:
    def __init__(self):
        self.user = get_environment_value("AZURE_REPO_USER")
        self.token = get_environment_value("AZURE_REPO_TOKEN")
        self.api_version = "6.0"
        self.devops_url = "https://dev.azure.com/azuresynegen"
        self.projects = self.get_projects()

    def get_projects(self):
        response = requests.get(
            f"{self.devops_url}/_apis/projects?api-version={self.api_version}",
            auth=HTTPBasicAuth(
                self.user,
                self.token
            )
        )
        response = response.json()["value"]
        projects = {}
        for project in response:
            projects[project["name"]] = project["id"]
        return projects

    def get_repos_per_project(self, project_name):
        response = requests.get(
            f"{self.devops_url}/{project_name}/_apis/git/repositories?api-version={self.api_version}",
            auth=HTTPBasicAuth(
                self.user,
                self.token
            )
        ).json()["value"]
        names = []
        for repo in response:
            names.append(repo["name"])
        return names

    def get_all_repos(self):
        repos = {}
        for project in self.get_projects().keys():
            repos[project] = self.get_repos_per_project(project)
        return repos

    def create_project(self, project_name):
        payload = {
            "name": project_name,
            "description": f"Project name: {project_name}",
            "visibility": 0,
            "capabilities": {
                "processTemplate": {
                    "templateTypeId": "b8a3a935-7e91-48b8-a94c-606d37c3e9f2"
                },
                "versioncontrol": {
                    "sourceControlType": "git"
                }
            }
        }
        response = requests.post(
            f"{self.devops_url}/_apis/projects?api-version={self.api_version}",
            auth=HTTPBasicAuth(
                self.user,
                self.token
            ),
            json=payload
        )
        if response.status_code != 202 and response.status_code != 200:
            raise Exception(response.text)


    def create_repo(self, project_name, project_id, repo_name):
        payload = {
            "name": repo_name,
            "project": {
                "name": project_name,
                "id": project_id
            }
        }
        response = requests.post(
            f"{self.devops_url}/{project_name}/_apis/git/repositories?api-version={self.api_version}",
            auth=HTTPBasicAuth(
                self.user,
                self.token
            ),
            json=payload
        )
        if response.status_code != 202 and response.status_code != 200 and response.status_code != 201:
            raise Exception(response.text)