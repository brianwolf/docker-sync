import os

from logic.apps.admin.config.variables import Vars
from logic.apps.sync.model import Compose
from logic.apps.tools import cmd
from logic.libs.logger.logger import get_log
from logic.libs.variables.variables import get_var

REPO_GIT_FOLDER = 'repo'


def sync():

    repo_path = get_clone_repository_path()

    original_workindir = os.getcwd()
    os.chdir(repo_path)

    dockers_running_list = get_dockers_running_list()

    for docker_compose_path in _get_docker_compose_paths_list('./'):

        new_compose = Compose(docker_compose_path)

        if new_compose.name in dockers_running_list:
            continue

        _run_new_compose(new_compose)

    os.chdir(original_workindir)


def get_clone_repository_path() -> str:

    workspace_path = os.path.join(get_var(Vars.WORKSPACE), REPO_GIT_FOLDER)

    if not os.path.exists(workspace_path):
        cmd.exec(f'mkdir -p {workspace_path}', echo=False)

    return workspace_path


def clone_repository() -> str:

    workspace_path = get_clone_repository_path()

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


def get_dockers_running_list() -> list[str]:
    return cmd.exec('docker ps --format "{{.Names}}"', echo=False).split('\n')


def _get_git_clone_command(repo: str, user: str, password: str, branch: str, path: str) -> str:

    git_repo_url_full = f'https://{user}:{password}@github.com/{user}/{repo}.git'

    return f'git clone -c http.sslVerify=false -b {branch} {git_repo_url_full} {path}'


def _get_docker_compose_paths_list(base_path: str) -> list[str]:

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
