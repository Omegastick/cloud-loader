from unittest.mock import mock_open, patch

from cloud_cloner.config import Clone, ClonePath, Config, load_config


def test_load_config_loads_basic_config_yaml():
    yaml = """
    base_path: base
    clones:
      - name: test
        paths:
          - src: src
            dest: dest
    """
    with patch("builtins.open", mock_open(read_data=yaml)):
        config = load_config("test.yaml")

    assert config == Config(
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
