# -*- coding: utf-8 -*-

""" TODO: to be documented """

class Rule(object):
    def __init__(self, perm, refex):
        self.perm = perm
        self.refex = refex
        self.users = []

    def append(self, users):
        # Be sure users is an array
        users = [ users ] if not hasattr(users, '__iter__') else users
        self.users += users

    def likes(self, rule):
        return self.perm == rule.perm and self.refex == rule.refex
