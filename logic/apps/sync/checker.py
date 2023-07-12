import threading
import time

from logic.apps.admin.config.variables import Vars
from logic.apps.sync import service
from logic.libs.logger.logger import get_log


def start_thread_checker():

    get_log().info('Start thread -> Checker')

    def thread_method():
        while True:
            service.sync()
            time.sleep(15)

    thread = threading.Thread(target=thread_method)
    thread.start()
