import subprocess

from logic.libs.logger.logger import get_log


def exec(cmd: str, echo: bool = True) -> str:

    if echo:
        get_log().info(cmd)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.wait()
    return p.stdout
