#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to the web servers, using the function do_deploy.
"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['34.239.0.61', '3.87.217.227']


def do_deploy(archive_path):
    """Distributes an archive to the web servers.

    Args:
        archive_path (str): the path of the archive to deploy.

    Returns:
        bool: True if all operations have been done correctly,
        otherwise False.
    """
    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/{}'.format(file_name))
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_ext))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False