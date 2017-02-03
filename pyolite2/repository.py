# -*- coding: utf-8 -*-

""" Repository module.

This module contains classes which define Repository.
"""

from .rule import Rule

# Some filters and mapping functions for Repository class
def _only_rules(item): return isinstance(item, Rule)
def _only_configs(item): return isinstance(item, Config)
def _concat_bundles(a, b): return a + b

class RepositoryNotFoundError(Exception): pass

class Repository(object):
    def __init__(self, name):
        self.name = name
        self.bundles = []

    def append(self, obj):
        if isinstance(obj, Bundle):
            self.bundles.append(obj)
        elif isinstance(obj, Rule):
            # It's complicate
            pass

    def rules(self):
        # Map bundles to rules and reduce them
        return filter(_only_rules, reduce(_concat_bundles, self.bundles))

    def configs(self):
        # Map bundles to configs and reduce them
        return filter(_only_configs, reduce(_concat_bundles, self.bundles))

class RepositoryCollection(list):
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

class Bundle(list):
    def __init__(self, repos):
        super(list, self).__init__()
        self.repos = repos

    def __str__(self):
        def dump_entry(entry): return entry.__str__()

        return 'repo ' + ' '.join(self.repos) + ('\n' if self else '') + '\n'.join(map(dump_entry, self))
