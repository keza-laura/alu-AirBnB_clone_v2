#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers."""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['34.239.0.61', '3.87.217.227']


def do_deploy(archive_path):
    """Deploy archive to web servers."""
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"

        put(archive_path, "/tmp/{}".format(file_name))

        run("mkdir -p {}{}".format(path, no_ext))

        run("tar -xzf /tmp/{} -C {}{}".format(file_name, path, no_ext))

        run("rm /tmp/{}".format(file_name))

        run("mv {}{}/web_static/* {}{}".format(path, no_ext, path, no_ext))

        run("rm -rf {}{}/web_static".format(path, no_ext))

        run("rm -rf /data/web_static/current")

        run("ln -s {}{} /data/web_static/current".format(path, no_ext))

        print("New version deployed!")

        return True

    except Exception:
        return False
