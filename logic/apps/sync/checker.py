import threading
import time

import requests

from logic.apps.admin.config.variables import Vars
from logic.apps.sync import service
from logic.libs.logger.logger import get_log
from logic.libs.variables.variables import get_var

_THREAD_CHECKER_ACTIVE = True
_LAST_COMMIT_SHA = ""


def checker():

    user = get_var(Vars.GIT_REPO_USER)
    token = get_var(Vars.GIT_REPO_PASS)
    repo = get_var(Vars.GIT_REPO_NAME)

    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f'https://api.github.com/repos/{user}/{repo}/commits'

    first_commit = requests.get(url, headers=headers).json()[0]

    global _LAST_COMMIT_SHA
    if _LAST_COMMIT_SHA != first_commit['sha']:
        get_log().info(f'Checked commit in {repo}')
        _LAST_COMMIT_SHA = first_commit['sha']
        service.sync()


def start_thread_checker():

    get_log().info('Start thread -> Checker')

    global _THREAD_CHECKER_ACTIVE
    _THREAD_CHECKER_ACTIVE = True

    def thread_method():
        global _THREAD_CHECKER_ACTIVE
        while _THREAD_CHECKER_ACTIVE:
            checker()
            time.sleep(15)

    thread = threading.Thread(target=thread_method)
    thread.start()


def stop_runner_thread():
    global _THREAD_CHECKER_ACTIVE
    _THREAD_CHECKER_ACTIVE = False
