# Instalar con pip
import time

import requests
from requests.auth import HTTPBasicAuth
import json
from modules.devops_requests import DevOpsInterface

SLEEP_TIME=10

azure_devops = DevOpsInterface()


with open("./repos.json") as file:
    try:
        details = json.load(file)
    except json.decoder.JSONDecodeError:
        raise Exception("El archivo no tiene formato JSON. Verificar.")
projects = azure_devops.get_projects()
for project in details["projects"]:
    if project["name"] not in projects:
        print(f"Creando el proyecto con nombre: {project['name']}")
        azure_devops.create_project(project["name"])

    repos = azure_devops.get_all_repos()
    for repo in project["repos"]:
        while project["name"] not in repos.keys():
            print(f"Actualizando lista de repos en {SLEEP_TIME} segundos")
            time.sleep(SLEEP_TIME)
            repos = azure_devops.get_all_repos()

        refreshed_projects = azure_devops.get_projects()
        if repo not in repos[project["name"]]:
            print(f"Creamos el repo {repo}")
            azure_devops.create_repo(
                project_name=project["name"],
                project_id=refreshed_projects[project["name"]],
                repo_name=repo
            )
