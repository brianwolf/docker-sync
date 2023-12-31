import threading
import time

import requests

from logic.apps.admin.config.variables import Vars
from logic.apps.sync import service
from logic.libs.logger.logger import get_log
from logic.libs.variables.variables import get_var

_LAST_COMMIT_SHA = ""


def start_thread_cloner():

    get_log().info('Start thread -> Cloner')

    def thread_method():
        while True:
            _cloner()
            time.sleep(20)

    thread = threading.Thread(target=thread_method)
    thread.start()


def _cloner():

    last_commit = _get_last_commit_sha()

    global _LAST_COMMIT_SHA
    if _LAST_COMMIT_SHA != last_commit:

        get_log().info(f'Checked new commit in repo -> cloning...')
        _LAST_COMMIT_SHA = last_commit
        service.clone_repository()


def _get_last_commit_sha() -> str:

    user = get_var(Vars.GIT_REPO_USER)
    token = get_var(Vars.GIT_REPO_PASS)
    repo = get_var(Vars.GIT_REPO_NAME)

    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f'https://api.github.com/repos/{user}/{repo}/commits'

    return requests.get(url, headers=headers).json()[0]['sha']
