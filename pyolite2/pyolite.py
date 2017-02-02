
from .file import File
from .repository import RepositoryCollection

class Pyolite(object):
    def __init__(self, admin_config):
        # Instance main configuration file
        self.main_file = File(self, admin_config)
        self.repos = RepositoryCollection()

    def load(self):
        """ Load Gitolite admin configuration """
        self.main_file.load()
