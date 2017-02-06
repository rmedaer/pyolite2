# -*- coding: utf-8 -*-

""" Repository module.

This module contains classes which define Repository.
"""

from .rule import Rule
from .bundle import Bundle

# Some filters and mapping functions for Repository class
def _only_rules(item): return isinstance(item, Rule)
def _only_configs(item): return isinstance(item, Config)
def _concat_bundles(a, b): return a + b

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
