import os

from logic.apps.admin.config.variables import Vars
from logic.apps.dockers_runned import service as dockers_runned_service
from logic.apps.tools import cmd
from logic.libs.logger.logger import get_log
from logic.libs.variables.variables import get_var
from logic.apps.dockers_runned.model import Compose

REPO_GIT_FOLDER = 'repo'


def sync():

    cloned_repo_path = _clone_repository()

    original_workindir = os.getcwd()
    os.chdir(cloned_repo_path)

    list_dockers_runned = dockers_runned_service.get_list()

    for docker_compose_path in _get_list_docker_compose_paths('.'):

        new_compose = Compose(docker_compose_path)

        if not new_compose.name in list_dockers_runned:
            _run_new_compose(new_compose)
            continue
        new_compose

    os.chdir(original_workindir)


def _clone_repository() -> str:

    workspace_path = os.path.join(get_var(Vars.WORKSPACE), REPO_GIT_FOLDER)

    cmd.exec(f'mkdir -p {workspace_path}', echo=False)
    cmd.exec(f'rm -rf {workspace_path}', echo=False)

    git_clone_command = _get_git_clone_command(
        get_var(Vars.GIT_REPO_NAME),
        get_var(Vars.GIT_REPO_USER),
        get_var(Vars.GIT_REPO_PASS),
        get_var(Vars.GIT_REPO_BRANCH),
        workspace_path
    )
    cmd.exec(git_clone_command, echo=False)

    return workspace_path


def _get_git_clone_command(repo: str, user: str, password: str, branch: str, path: str) -> str:

    git_repo_url_full = f'https://{user}:{password}@github.com/{user}/{repo}.git'

    return f'git clone -c http.sslVerify=false -b {branch} {git_repo_url_full} {path}'


def _get_list_docker_compose_paths(base_path: str) -> list[str]:

    result = []
    for (dirpath, _, files) in os.walk(base_path):

        result.extend([
            f'{dirpath}/{file}'
            for file in files
            if file.endswith('.yaml') or file.endswith('.yml')
        ])

    return result


def _run_new_compose(compose: Compose):

    original_workindir = os.getcwd()

    get_log().info('------------------------------------------------')
    get_log().info(f'>> {compose.name} <<')
    get_log().info(f'File: {compose.file}')
    get_log().info(f'Folder: {compose.folder}')
    get_log().info('------------------------------------------------')

    os.chdir(compose.folder)
    cmd.exec(f'docker compose -f {compose.file} up -d')
    os.chdir(original_workindir)
