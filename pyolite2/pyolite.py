
from .file import File
from .bundle import Bundle
from .repository_collection import RepositoryCollection

class Pyolite(object):
    def __init__(self, admin_config):
        # Instance main configuration file
        self.main_file = File(self, admin_config)
        self.repos = RepositoryCollection()

        @self.repos.on_added()
        def on_repo_added(repo):
            # When a repo has been added, we automatically assign it a Bundle
            self.main_file.tree.append(Bundle([repo.name]))

    def load(self):
        """ Load Gitolite admin configuration """
        self.main_file.load()
