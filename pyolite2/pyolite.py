
from .file import File
from .bundle import Bundle
from .repository_collection import RepositoryCollection

class Pyolite(object):
    def __init__(self, admin_config):
        # Instance main configuration file
        self.main_file = File(self, admin_config)
        self.files = [self.main_file]
        self.repos = RepositoryCollection()

        @self.repos.on_added()
        def on_repo_added(repo):
            for bundle in repo.bundles:
                self.main_file.tree.append(bunble)

        @self.repos.on_removed()
        def on_repo_removed(repo):
            for bundle in repo.bundles:
                bundle.drop_name(repo.name)

        @self.repos.on_bundle_added()
        def on_bundle_added(bundle):
            self.main_file.tree.append(bundle)

    def load(self):
        """ Load Gitolite admin configuration """
        self.main_file.load()

    def save(self):
        for file in self.files:
            file.save()
