from logic.apps.sync.checker import start_thread_checker
from logic.apps.sync.cloner import start_thread_cloner


def prepare_threads():
    start_thread_checker()
    start_thread_cloner()
