from enum import Enum

from logic.libs.variables.variables import Config, get_var, setup


class Vars(Enum):
    VERSION = 'VERSION'
    PYTHON_HOST = 'PYTHON_HOST'
    PYTHON_PORT = 'PYTHON_PORT'
    LOGS_LEVEL = 'LOGS_LEVEL'
    LOGS_PATH = 'LOGS_PATH'
    LOGS_BACKUPS = 'LOGS_BACKUPS'
    GIT_REPO_NAME = 'GIT_REPO_NAME'
    GIT_REPO_USER = 'GIT_REPO_USER'
    GIT_REPO_PASS = 'GIT_REPO_PASS'
    GIT_REPO_BRANCH = 'GIT_REPO_BRANCH'
    WORKSPACE = 'WORKSPACE'
    TEMP_PATH = 'TEMP_PATH'


def setup_vars():
    setup(
        Config(
            file_path='logic/resources/variables.yaml',
            hiden_vars=[]
        )
    )
