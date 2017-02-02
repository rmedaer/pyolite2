# -*- coding: utf-8 -*-

""" Repository module.

This module contains classes which define Repository.
"""

from .bundle import Bundle

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
        def extract(bundle):
            return bundle.rules

        def concat(a, b):
            return a + b

        # Map bundle to rule and reduce them
        return reduce(concat, map(extract, self.bundles))

class RepositoryCollection(list):
    def __getitem__(self, key):
        return self.get(key)

    def get(self, name):
        for repo in self.repos:
            if repo.name == name:
                return repo

        raise ValueError('Unable to find repository')

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
