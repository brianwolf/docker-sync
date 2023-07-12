import json
import os

from logic.apps.admin.config.variables import Vars
from logic.apps.tools import cmd
from logic.libs.variables.variables import get_var
from logic.apps.dockers_runned.model import Compose


def get_list() -> list[str]:
    return cmd.exec('docker ps --format "{{.Names}}"', echo=False)
