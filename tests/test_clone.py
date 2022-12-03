from unittest.mock import Mock, call, patch

import pytest
from rclone import RClone

from cloud_cloner.clone import clone
from cloud_cloner.config import Clone, ClonePath, Config, load_config
from cloud_cloner.rclone_config import load_rclone_config


@pytest.fixture
def mock_rclone():
    with patch("cloud_cloner.clone.rclone") as mock_rclone_module:
        mock_rclone = Mock(spec=RClone)
        mock_rclone_module.with_config.return_value = mock_rclone
        yield mock_rclone


@pytest.fixture
def mock_load_config():
    with patch("cloud_cloner.clone.load_config", spec=load_config) as mock_load_config:
        yield mock_load_config


@pytest.fixture
def mock_load_rclone_config():
    with patch("cloud_cloner.clone.load_rclone_config", spec=load_rclone_config) as mock_load_rclone_config:
        yield mock_load_rclone_config


def test_clone_loads_correct_config_path(mock_load_config, mock_load_rclone_config):
    clone([], config_path="test.yaml")
    mock_load_config.assert_called_once_with("test.yaml")


def test_clone_loads_correct_rclone_config_path(mock_load_config, mock_load_rclone_config):
    clone([], rclone_config_path="test.yaml")
    mock_load_rclone_config.assert_called_once_with("test.yaml")


def test_clone_clones_one_directory(mock_rclone, mock_load_config, mock_load_rclone_config):
    mock_load_config.return_value = Config(
        base_path="base",
        clones=[
            Clone(
                name="test",
                paths=[
                    ClonePath(src="src", dest="dest"),
                ],
            ),
        ],
    )
    clone(["test"])
    mock_rclone.copy.assert_called_once_with("remote:base/src", "dest", flags=["--checksum"])


def test_none_defaults_are_ignored_by_default(mock_rclone, mock_load_config, mock_load_rclone_config):
    mock_load_config.return_value = Config(
        base_path="base",
        clones=[
            Clone(
                name="test",
                paths=[
                    ClonePath(src="src", dest="dest"),
                ],
                default=False,
            ),
        ],
    )
    clone([])
    mock_rclone.copy.assert_not_called()


def test_defaults_are_cloned_by_default(mock_rclone, mock_load_config, mock_load_rclone_config):
    mock_load_config.return_value = Config(
        base_path="base",
        clones=[
            Clone(
                name="test",
                paths=[
                    ClonePath(src="src", dest="dest"),
                ],
                default=True,
            ),
        ],
    )
    clone([])
    mock_rclone.copy.assert_called_once_with("remote:base/src", "dest", flags=["--checksum"])


def test_clone_clones_multiple_directories(mock_rclone, mock_load_config, mock_load_rclone_config):
    mock_load_config.return_value = Config(
        base_path="base",
        clones=[
            Clone(
                name="test",
                paths=[
                    ClonePath(src="src", dest="dest"),
                    ClonePath(src="src2", dest="dest2"),
                ],
            ),
        ],
    )
    clone(["test"])
    mock_rclone.copy.assert_has_calls(
        [
            call("remote:base/src", "dest", flags=["--checksum"]),
            call("remote:base/src2", "dest2", flags=["--checksum"]),
        ]
    )
