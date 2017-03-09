# -*- coding: utf-8 -*-

""" TODO: to be documented """

class Rule(list):
    def __init__(self, perm, refex):
        self.perm = perm
        self.refex = refex
        super(list, self).__init__()

    def likes(self, rule):
        return self.perm == rule.perm and self.refex == rule.refex

    def __str__(self):
        return ('\t' + self.perm + (' ' + self.refex if self.refex else '')
                + ' = ' + ' '.join(self))
