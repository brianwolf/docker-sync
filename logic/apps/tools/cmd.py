import subprocess
from logic.libs.logger.logger import logger


def exec(cmd: str, echo: bool = True) -> str:

    if echo:
        logger.info(cmd)

    if 'docker compose' in cmd:
        return ''
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.wait()
    return p.stdout
