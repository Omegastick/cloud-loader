import asyncio
import os
from functools import partial, wraps
from pathlib import Path
from typing import Coroutine, List

import rclone
import typer

from cloud_cloner.bootstrap import app
from cloud_cloner.config import ClonePath, Config, load_config
from cloud_cloner.rclone_config import load_rclone_config


def make_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


async def clone_path(path: ClonePath, base_dest_path: Path, config: Config, rclone_config: str) -> None:
    src_path = Path(config.base_path) / Path(path.src)
    dest_path = base_dest_path / Path(path.dest)
    dest_directory = dest_path if dest_path.is_dir() else dest_path.parent

    if not os.path.exists(dest_directory):
        print(f"Making directory {dest_directory}...")
        os.makedirs(dest_directory)

    print(f"Cloning {src_path} to {dest_path}...", end="\x1b[1K\r", flush=True)
    loop = asyncio.get_event_loop()
    rclone_runner = rclone.with_config(rclone_config)
    copy_func = partial(rclone_runner.copy, f"{path.remote}:{src_path}", str(dest_path), flags=["--checksum"])
    await loop.run_in_executor(None, copy_func)
    print(f"Cloned {src_path} to {dest_path}")


@app.command()
@make_async
async def clone(
    clones: List[str] = typer.Argument(None),
    base_dest_path: str = "./",
    config_path: str = "cloud_cloner.yaml",
    rclone_config_path: str = "~/.rclone",
    ignore_default: bool = False,
) -> None:
    config = load_config(config_path)
    rclone_config = load_rclone_config(rclone_config_path)

    tasks: List[Coroutine] = []

    for clone in config.clones:
        if (clone.default and not ignore_default) or clone.name in clones:
            print(f"Cloning {clone.name}...")
            for path in clone.paths:
                tasks.append(clone_path(path, Path(base_dest_path), config, rclone_config))
    
    await asyncio.gather(*tasks)
