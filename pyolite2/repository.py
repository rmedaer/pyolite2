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
    def __init__(self, name, empty=False):
        self.name = name
        self.on_addeds = []
        self.on_forked_rules = []
        self.bundles = [] if empty else [Bundle([self.name])]

    def on_added(self):
        def wrapper(handler):
            self.on_addeds.append(handler)
            return handler
        return wrapper

    def on_forked_rule(self):
        def wrapper(handler):
            self.on_forked_rules.append(handler)
            return handler
        return wrapper

    def append_bundle(self, bundle, notify=True):
        # Append bundle to self list
        self.bundles.append(bundle)

        # If needed, notify handlers
        if notify:
            for handler in self.on_addeds:
                handler(bundle)

    def append_rule(self, obj, notify=True):
        explicit_bundle = None
        similar_rule_found = False
        for bundle in self.bundles:
            if len(bundle.names) == 1 and bundle.names[0] == self.name:
                explicit_bundle = bundle
                for rule in bundle:
                    if rule.likes(obj):
                        rule += obj
                        similar_rule_found = True
                        break

            if similar_rule_found:
                break

        if explicit_bundle is None:
            # If not any exclusive bundle found, instance a new one
            bundle = Bundle([self.name])
            bundle.append(obj)
            self.append(bundle, notify)
        elif not similar_rule_found:
            # If an exclusive bundle is found but not a similar rule,
            # add the rule to this bundle
            explicit_bundle.append(obj)

    def append(self, obj, notify=True):
        if isinstance(obj, Bundle):
            self.append_bundle(obj, notify)
        elif isinstance(obj, Rule):
            self.append_rule(obj, notify)

    def replace_rule(self, old_rule, new_rule):
        # Algorithm: replace => remove + add
        # Since a rule can be applied to multiple repositories it's easier
        # to reuse the "remove" algorithm and then add a new one
        self.remove_rule(old_rule)
        self.append(new_rule)

    def remove_rule(self, rule):
        for bundle in self.bundles:
            if rule in bundle:
                # We found the rule, we will now check if this rule is set
                # on a bundle with single repo or with multiple repos.
                # If there is only one repo (same then self) we can safetly
                # remove it. Otherwise we have use more complex algorithm to
                # fork (copy/paste) the rule.
                bundle.remove(rule)
                if not (len(bundle.names) == 1 and bundle.names[0] == self.name):
                    for name in bundle.names:
                        # Fork rule into other repositories
                        if name != self.name:
                            for handler in self.on_forked_rules:
                                handler(name, rule)

    def remove(self, obj):
        if isinstance(obj, Rule):
            self.remove_rule(obj)

    def rules(self):
        # Map bundles to rules and reduce them
        if not self.bundles:
            return []

        return filter(_only_rules, reduce(_concat_bundles, self.bundles))

    def configs(self):
        # Map bundles to configs and reduce them
        if not self.bundles:
            return []

        return filter(_only_configs, reduce(_concat_bundles, self.bundles))
