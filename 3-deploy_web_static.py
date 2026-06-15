#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers.
"""
from fabric.api import *
from datetime import datetime
import os

# Configure remote hosts
env.hosts = ["54.152.40.73", "3.89.112.68"]
env.user = "ubuntu"


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
        local("tar -cvzf {} web_static".format(archive_path))
        
        # Get file size
        file_size = os.path.getsize(archive_path)
        
        # Display success message
        print("web_static packed: {} -> {}Bytes".format(archive_path, file_size))
        
        return archive_path
    except Exception as e:
        print("Error creating archive: {}".format(str(e)))
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    
    Args:
        archive_path: Path to the archive file to deploy.
    
    Returns:
        True if successful, False otherwise.
    """
    # Check if archive exists
    if not os.path.exists(archive_path):
        return False
    
    try:
        # Extract archive filename without extension
        archive_file = os.path.basename(archive_path)
        archive_name = archive_file.split('.')[0]
        
        # Define release directory
        release_dir = "/data/web_static/releases/{}".format(archive_name)
        
        # Upload archive to /tmp/
        put(archive_path, "/tmp/{}".format(archive_file))
        
        # Create release directory
        run("mkdir -p {}".format(release_dir))
        
        # Extract archive to release directory
        run("tar -xzf /tmp/{} -C {}".format(archive_file, release_dir))
        
        # Remove archive from /tmp/
        run("rm /tmp/{}".format(archive_file))
        
        # Move contents from web_static subdirectory to release directory
        run("mv {}/web_static/* {}".format(release_dir, release_dir))
        
        # Remove the empty web_static directory
        run("rm -rf {}/web_static".format(release_dir))
        
        # Remove old symbolic link
        run("rm -rf /data/web_static/current")
        
        # Create new symbolic link
        run("ln -s {}/ /data/web_static/current".format(release_dir))
        
        print("New version deployed!")
        return True
    
    except Exception as e:
        print("Error during deployment: {}".format(str(e)))
        return False


def deploy():
    """
    Creates and distributes an archive to web servers.
    
    Returns:
        The return value of do_deploy, or False if packing failed.
    """
    # Pack the web_static folder
    archive_path = do_pack()
    
    # Return False if packing failed
    if not archive_path:
        return False
    
    # Deploy the archive
    return do_deploy(archive_path)
