#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of
the web_static folder of the AirBnB Clone repo, using the function do_pack.
"""
import os
from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: the archive path if the archive has been correctly generated.
        None: otherwise.
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        print("Packing web_static to {}".format(file_name))
        local("tar -cvzf {} web_static".format(file_name))
        file_size = os.path.getsize(file_name)
        print("web_static packed: {} -> {}Bytes".format(file_name, file_size))
        return file_name
    except Exception:
        return None
