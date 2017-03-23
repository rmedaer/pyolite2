# -*- coding: utf-8 -*-

""" TODO: to be documented """

class Option(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return '\toption ' + self.key + ' = ' + self.value
