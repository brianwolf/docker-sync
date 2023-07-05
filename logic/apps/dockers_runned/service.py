import json
import os

from logic.apps.admin.config.variables import Vars
from logic.apps.tools import cmd
from logic.libs.logger.logger import logger
from logic.libs.variables.variables import get_var

LIST_DOCKERS_RUNNED_FILE_NAME = 'dockers_runned.json'


def delete(name: str):

    list_dockers = get_list()
    list_dockers.remove(name)
    update_list(list_dockers)


def get_list() -> list[str]:

    file_path = _prepare_file()

    with open(file_path) as file:
        return json.load(file)


def update_list(list: list[str]):

    file_path = _prepare_file()

    with open(file_path, 'w') as file:
        file.write(json.dumps(list))


def _prepare_file() -> str:

    list_dockers_runned_file_path = os.path.join(
        get_var(Vars.WORKSPACE),
        LIST_DOCKERS_RUNNED_FILE_NAME
    )

    cmd.exec(f'mkdir -p {os.path.dirname(list_dockers_runned_file_path)}')

    if not os.path.exists(list_dockers_runned_file_path):
        with open(list_dockers_runned_file_path, 'w') as file:
            file.write('[]')

    return list_dockers_runned_file_path
