import os

import rclone
from rich import print

from cloud_loader.bootstrap import app


def load_rclone_config(rclone_config_path: str) -> str:
    print(f"Loading rclone config from {rclone_config_path}")
    with open(os.path.expanduser(rclone_config_path), "r") as config_file:
        return config_file.read()


@app.command()
def load(remote_directory: str, destination_directory: str, rclone_config_path: str = "~/.rclone") -> None:
    rclone_config = load_rclone_config(rclone_config_path)

    print(f"Syncing {remote_directory} to {destination_directory}")
    rclone.with_config(rclone_config).copy(f"remote:{remote_directory}", destination_directory, flags=["-P"])
    print(f"Synced {remote_directory} to {destination_directory}")
