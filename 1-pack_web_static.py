#!/usr/bin/python3
"""
Fabric script to pack the web_static directory into a compressed archive.
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    
    Returns:
        The archive path if successful, None otherwise.
    """
    try:
        # Create versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")
        
        # Create archive name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}".format(timestamp)
        archive_path = "versions/{}.tgz".format(archive_name)
        
        # Display the packing action
        print("Packing web_static to {}".format(archive_path))
        
        # Create the archive
        result = local("tar -cvzf {} web_static".format(archive_path), capture=True)
        
        # Get file size
        file_size = os.path.getsize(archive_path)
        
        # Display success message
        print("web_static packed: {} -> {}Bytes".format(archive_path, file_size))
        
        return archive_path
    except Exception as e:
        print("Error creating archive: {}".format(str(e)))
        return None
