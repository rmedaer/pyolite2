# -*- coding: utf-8 -*-

""" TODO: to be documented """

class Config(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return '\tconfig ' + self.key + ' = ' + self.value
