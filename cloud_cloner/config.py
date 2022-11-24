from typing import List

import yaml
from pydantic import BaseModel


class ClonePath(BaseModel):
    src: str
    dest: str


class Clone(BaseModel):
    name: str
    paths: List[ClonePath]
    default: bool = False


class Config(BaseModel):
    base_path: str = ""
    clones: List[Clone]


def load_config(path: str) -> Config:
    with open(path) as f:
        config = yaml.safe_load(f)
    return Config(**config)
