# -*- coding: utf-8 -*-

from .repository import Repository
from .rule import Rule
from .config import Config
from .errors import RepositoryNotFoundException, RepositoryDuplicateException

class RepositoryCollection(list):
    def __init__(self):
        super(RepositoryCollection, self).__init__()
        self.on_addeds = []
        self.on_removeds = []
        self.on_bundle_addeds = []

    def __getitem__(self, key):
        return self.get(key)

    def get(self, name):
        if isinstance(name, Repository):
            name = name.name

        for repo in self:
            if repo.name == name:
                return repo

        raise RepositoryNotFoundException('Repository \'%s\' could not be found' % name)

    def on_added(self):
        def wrapper(handler):
            self.on_addeds.append(handler)
            return handler
        return wrapper

    def on_removed(self):
        def wrapper(handler):
            self.on_removeds.append(handler)
            return handler
        return wrapper

    def on_bundle_added(self):
        def wrapper(handler):
            self.on_bundle_addeds.append(handler)
            return handler
        return wrapper

    def exists(self, name):
        for repo in self:
            if repo.name == name:
                return True
        return False

    def append(self, repo, notify=True):
        if not isinstance(repo, Repository):
            raise ValueError('Given value is not a Repository')

        if self.exists(repo.name):
            raise RepositoryDuplicateException('Duplicate repository \'%s\'' % repo.name)

        super(RepositoryCollection, self).append(repo)

        # Hook "bundle added" event on repositories added to this collection
        @repo.on_added()
        def on_bundle_added_to_repo(bundle):
            for handler in self.on_bundle_addeds:
                handler(bundle)

        # This callback is reached when we have to fork a rule into repo bundles
        @repo.on_forked_rule()
        def duplicate_rule_to_repo(repo_name, rule):
            try:
                repo = self.get(repo_name)
            except RepositoryNotFoundException:
                repo = Repository(name)
                self.append(repo)

            repo.append(rule)

        if notify:
            for handler in self.on_addeds:
                handler(repo)

    def remove(self, name, notify=True):
        repo = self.get(name)
        list.remove(self, repo)

        if notify:
            for handler in self.on_removeds:
                handler(repo)
