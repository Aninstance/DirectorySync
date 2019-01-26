#!/usr/bin/env python
import os
import subprocess

"""
Simple script to sync the contents of all subdirectories in the current working directory to a specified location.
This calls rsync - which is required to be installed on both local and
remote servers (can use rsync over SSH in usual format if syncing to a remote server).
"""

_VERSION = 1.1
_CURRENT_WORKING_DIR = f'{os.path.dirname(os.path.realpath(__file__))}/'  # current working directory
_TARGET_DIR = f'/home/me/example_backup/'  # target sync directory
_IGNORE_FILES = []  # filenames or directory names to exclude from the sync


def inject_exclusion(val, cmd):
    """
    Injects the exclude argument into the rsync command
    :param val: name of file or dir to exclude (str)
    :param cmd: existing rsync command
    :return: True|False
    """
    if isinstance(cmd, list) and isinstance(val, str):
        cmd.insert(3, '--exclude')
        cmd.insert(4, val)
        return True
    return False


def sync(local_dir_name, remote_dir_name, delete_on_remote=False, dry_run=False):
    """
    Syncs local_dir_name to remote_dir_name.
    :param local_dir_name: name of local directory to be synced (String)
    :param remote_dir_name: name of remote directory in which local directory copy is/will be located (String)
    :param delete_on_remote: whether to delete files existing in remote copy that no longer exist in local (True|False)
    :param dry_run: whether to run the rsync command in dry-run mode to check all is working (True|False)
    :return True|False
    """

    if local_dir_name and remote_dir_name:

        remote_del = '--delete-after' if delete_on_remote else None
        test_run = '--dry-run' if dry_run else None

        # ensure slashes all present & correct
        if remote_dir_name[-1:] != '/':
            remote_dir_name += '/'
        if local_dir_name[-1:] != '/':
            local_dir_name += '/'

        # define base command
        cmd = ['rsync', '-av', '--progress', local_dir_name, f'{remote_dir_name}{local_dir_name}']

        # add optional command args
        if remote_del:
            cmd.insert(3, remote_del)
        if test_run:
            cmd.insert(3, test_run)
        if _IGNORE_FILES:
            [inject_exclusion(val, cmd) for val in _IGNORE_FILES]

        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

        if p.stderr:
            print(f'Error: {p.stderr}')
        return True
    return False


def run():
    """
    Iterates subdirectories in current directory and syncs to the remote directory
    :return: [True|False ...]
    """
    return [sync(local_dir_name=d, remote_dir_name=_TARGET_DIR, delete_on_remote=False, dry_run=True)
            for d in next(os.walk(_CURRENT_WORKING_DIR))[1]]


run()
