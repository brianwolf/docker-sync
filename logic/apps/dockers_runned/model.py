import os
from dataclasses import dataclass


@dataclass
class Compose:
    name: str
    file: str
    folder: str

    def __init__(self, dockerfile_path: str):
        self.name = dockerfile_path.split('/')[-2]
        self.file = os.path.basename(dockerfile_path)
        self.folder = os.path.dirname(dockerfile_path)

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

    def get_path(self) -> str:
        return f'{self.folder}/{self.file}'
