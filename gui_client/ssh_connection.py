__author__ = "Team B"
__status__ = "Working Module"
__version__ = "1.0"

""" This module handles the SSH session used by gui_manager.py"""

from paramiko import SSHClient, SFTPClient


class Session():
    """Class that creates and handles ssh/sftp connections"""
    def __init__(self):
        self.client: SSHClient = SSHClient()
        self.sftp: SFTPClient or None = None
        self.isActive: bool = False

    def probe_dir(self, path: str):
        """Checks if dir exists"""
        self._open_sftp()
        try:
            return self.sftp.listdir(path)
        except FileNotFoundError:
            return None

    def _open_sftp(self):
        """ Executes SSHClient.open_sftp and adds object to self.sftp"""
        if not self.sftp:
            self.sftp = self.client.open_sftp()
