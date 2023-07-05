import subprocess
from logic.libs.logger.logger import logger


def exec(cmd: str, echo: bool = True) -> str:

    if echo:
        logger.info(cmd)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.wait()
    return p.stdout
