from paramiko import SSHClient, SFTPClient


class Session():
    def __init__(self):
        self.client: SSHClient = SSHClient()
        self.sftp: SFTPClient or None = None
        self.isActive: bool = False

    def transfer_filelist(self, files):
        self.sftp = self.client.open_sftp()

    def probe_dir(self, path: str):
        self._open_sftp()
        try:
            return self.sftp.listdir(path)
        except FileNotFoundError:
            return None

    def _open_sftp(self):
        if not self.sftp:
            self.sftp = self.client.open_sftp()

