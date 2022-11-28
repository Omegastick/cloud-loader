A tool for cloning data from cloud storage providers in a configurable way.

Example config file:
```yaml
base_path: /base_path
clones:
  - name: clone_one_folder
    paths:
      - src: path/to/remote/folder
        dest: path/to/local/folder
    default: true
  - name: clone_files
    paths:
      - src: files/file.txt
        dest: remote_files/file_renamed.txt
      - src: files/file2.txt
        dest: remote_files/
```

The config file is expected to be in the current working directory and named `cloud_cloner.yaml`. This location can be set with `--config-path`.

A valid rclone config is expected at `~/.rclone`. This location can be set with `--rclone-config-path`. 

Then clone with `python -m cloud_cloner clone` or `python -m cloud_cloner clone clone_one_folder`.

See `python -m cloud_cloner --help` for more options.
