# -*- coding: utf-8 -*-

from .repository import Repository
from .rule import Rule
from .config import Config

# Exceptions
class RepositoryNotFoundError(Exception): pass
class RepositoryDuplicateError(Exception): pass

class RepositoryCollection(list):
    def __init__(self):
        super(RepositoryCollection, self).__init__()
        self.on_addeds = []

    def __getitem__(self, key):
        return self.get(key)

    def get(self, name):
        for repo in self:
            if repo.name == name:
                return repo

        raise RepositoryNotFoundError('Unable to find repository.')

    def get_or_create(self, name):
        try:
            return self.get(name)
        except:
            repo = Repository(name)
            self.append(repo)
            return repo

    def _get_or_create(self, name):
        try:
            return self.get(name)
        except:
            repo = Repository(name)
            super(RepositoryCollection, self).append(repo)
            return repo

    def on_added(self):
        def wrapper(handler):
            self.on_addeds.append(handler)
            return handler
        return wrapper

    def exists(self, name):
        for repo in self:
            if repo.name == name:
                return True
        return False

    def append(self, repo):
        self._append(repo)

        for handler in self.on_addeds:
            handler(repo)

    def _append(self, repo):
        if not isinstance(repo, Repository):
            raise ValueError('Given value is not a Repository')

        if self.exists(repo.name):
            raise RepositoryDuplicateError('Duplicate repository \'%s\'' % repo.name)

        super(RepositoryCollection, self).append(repo)
