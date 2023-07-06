import os

from logic.apps.admin.config.variables import Vars
from logic.apps.dockers_runned import service as dockers_runned_service
from logic.apps.tools import cmd
from logic.libs.logger.logger import get_log
from logic.libs.variables.variables import get_var

LIST_DOCKERS_RUNNED_FILE_NAME = 'dockers_runned.json'
REPO_GIT_FOLDER = 'repo'


def sync():

    original_workindir = os.getcwd()

    temp_path = get_var(Vars.WORKSPACE)
    cmd.exec(f'mkdir -p {temp_path}')
    os.chdir(temp_path)

    cmd.exec(f'rm -rf {REPO_GIT_FOLDER}')

    git_clone_command = _get_git_clone_command(
        get_var(Vars.GIT_REPO_NAME),
        get_var(Vars.GIT_REPO_USER),
        get_var(Vars.GIT_REPO_PASS),
        get_var(Vars.GIT_REPO_BRANCH)
    )
    cmd.exec(git_clone_command, echo=False)

    _run_dockers_compose('.')
    os.chdir(original_workindir)


def _get_git_clone_command(repo: str, user: str = None, password: str = None, branch: str = 'main') -> str:

    git_repo_url_full = f'github.com/{user}/{repo}.git'

    if user and password:
        git_repo_url_full = f'{user}:{password}@{git_repo_url_full}'

    git_repo_url_full = f'https://{git_repo_url_full}'

    return f'git clone -c http.sslVerify=false -b {branch} {git_repo_url_full} {REPO_GIT_FOLDER}'


def _get_list_docker_compose_paths(base_path: str) -> list[str]:

    result = []
    for (dirpath, _, files) in os.walk(base_path):

        result.extend([
            f'{dirpath}/{file}'
            for file in files
            if file.endswith('.yaml') or file.endswith('.yml')
        ])

    return result


def _get_docker_compose_name(docker_compose_path: str) -> str:

    docker_compose_file_name = docker_compose_path.split(
        '/')[-1].split('.')[0].lower()

    if docker_compose_file_name != 'docker-compose':
        return docker_compose_file_name

    return docker_compose_path.split('/')[-2]


def _run_dockers_compose(base_path: str):

    list_dockers_runned = dockers_runned_service.get_list()

    for docker_compose_path in _get_list_docker_compose_paths(base_path):

        docker_compose_name = _get_docker_compose_name(docker_compose_path)

        if docker_compose_name in list_dockers_runned:
            continue

        original_workindir = os.getcwd()

        docker_compose_folder = os.path.dirname(docker_compose_path)
        docker_compose_file = os.path.basename(docker_compose_path)

        os.chdir(docker_compose_folder)
        get_log().info(f'{docker_compose_name}')
        get_log().info(f'Path: {docker_compose_path}')
        get_log().info(f'File: {docker_compose_file}')
        get_log().info(f'Folder: {docker_compose_folder}')
        cmd.exec(f'docker compose -f {docker_compose_file} up -d')
        get_log().info('------------------------------------------------')
        os.chdir(original_workindir)

        list_dockers_runned.append(docker_compose_name)

    dockers_runned_service.update_list(list_dockers_runned)
