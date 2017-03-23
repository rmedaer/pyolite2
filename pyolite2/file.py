# -*- coding: utf-8 -*-

"""Gitolite configuration file abstraction.

This module contains functions to parse and abstract a Gitolite configuration
file.
"""

import re
from .repository import Repository
from .bundle import Bundle
from .rule import Rule
from .config import Config
from .option import Option
from .errors import (
    ConfigurationFileException,
    PyoliteLexerException
)

P_COMMENT = '^\s*#\s*([\S\s]*?)\s*$'
P_GROUP   = '^@(\S+)\s*=\s*([\S\s]*?)\s*$'
P_REPO    = '^repo\s+([\S\s]*?)\s*$'
P_INCLUDE = '^include\s+"?([\S\s]*?)"?\s*$'
P_RULE    = '^\s*(-|C|R|RW\+?(?:C?D?|D?C?)M?)\s+(\S*)?\s*=\s*([\S\s]*?)\s*$'
P_CONFIG  = '^\s*config\s*(\S+)\s*=\s*(.*)'
P_OPTION  = '^\s*option\s*(\S+)\s*=\s*(.*)'
P_EMPTY   = '^\s*$'
P_TYPE    = type(re.compile('.'))

class File(object):
    """ This class represents a Gitolite configuration file. """

    def __init__(self, pyolite, uri):
        """ Initialize a Gitolite configuration file. """
        # Store parent pyolite object
        self.pyolite = pyolite
        self.uri = uri
        self.tree = []
        self.last_bundle = None

    def get_last_bundle(self):
        # Make sure we already parsed a bundle
        if self.last_bundle == None:
            raise ConfigurationFileException('Malformed Gitolite configuration')

        return self.last_bundle

    def load(self):
        """ Load this Gitolite configuration file. """
        # Instance lexer from file URI
        lexer = Lexer(self.uri)
        self.last_bundle = None

        @lexer.default
        def gotDefault(str, *args, **kwargs):
            raise ConfigurationFileException("Unrecognized string: '%s'" % str)

        @lexer.op([P_EMPTY, P_COMMENT])
        def gotEmptyLine(matches, *args, **kwargs):
            # Even it's an empty line, add it to our tree in order to dump it later
            self.tree.append(matches.group(0))


        @lexer.op(P_REPO)
        def gotRepo(matches, *args, **kwargs):
            names = re.split('\s+', matches.group(1))

            # Save last bundle
            self.last_bundle = Bundle(names)

            # Insert bundle into tree
            self.tree.append(self.last_bundle)

            for name in names:
                # Insert bundle into existing repository or create it !
                try:
                    # Get repo if already exists
                    repo = self.pyolite.repos.get(name)
                except:
                    # Initialize EMPTY repository
                    repo = Repository(name, True)
                    # Append repo to collection (without notify the whole config)
                    self.pyolite.repos.append(repo, False)

                # Append last_bundle into this repo (without notification)
                repo.append(self.last_bundle, False)

        @lexer.op(P_RULE)
        def gotRule(matches, *args, **kwargs):
            # Instance Rule object and insert its users
            rule = Rule(matches.group(1), matches.group(2))
            rule += re.split('\s+', matches.group(3))

            # Append to last parsed bundle in tree
            self.get_last_bundle().append(rule)

        @lexer.op(P_CONFIG)
        def gotConfig(matches, *args, **kwargs):
            # Instance Config object
            config = Config(matches.group(1), matches.group(2))

            # Append config in last bundle of the tree
            self.get_last_bundle().append(config)

        @lexer.op(P_OPTION)
        def gotConfig(matches, *args, **kwargs):
            # Instance Option object
            option = Option(matches.group(1), matches.group(2))

            # Append option in last bundle of the tree
            self.get_last_bundle().append(option)

        lexer.parse()

    def save(self):
        with open(self.uri, 'w') as fd:
            fd.write(self.__str__())

    def __str__(self):
        def dump_entry(entry): return entry.__str__()

        return '\n'.join(map(dump_entry, self.tree)) + '\n'

class Lexer(object):
    """ Lexer class; this lexer expose decorators to switch parser regex.

    This "lexer" is basically a switch for File parser. It's using decorator
    to expose regex handler.
    """

    def __init__(self, uri):
        """ Initialize a Lexer object. """
        self.uri = uri
        self.regexes = []
        self.default_handler = None

    def default(self, handler):
        """ Default handler decorator.

        Please use this method as decorator to define default handler.
        """
        self.default_handler = handler
        return handler


    def op(self, patterns):
        """ Operator handler decorator.

        Please use this method as decorator to handle given regex.
        """
        def wrap(handler):
            """ Operator decorator wrapper. """
            # Cast case value to array
            regexes = [ patterns ] if not hasattr(patterns, '__iter__') else patterns

            for regex in regexes:
                # If this item is not a compiled regular expression, compile it.
                if type(regex) != P_TYPE:
                    regex = re.compile(regex)

                # Raise SwitchError on a duplicate case regex.
                for previous, _ in self.regexes:
                    if regex.pattern == previous.pattern:
                        raise PyoliteLexerException('Duplicate regex case value \'%s\'' % regex.pattern)
                self.regexes.append((regex, handler))

            return handler
        return wrap

    def search(self, value):
        """ Search the first matching pattern from registered regexes. """
        for regex, handler in self.regexes:
            matches = regex.search(value)
            if matches is not None:
                return (matches, handler)
        return (None, None)

    def parse(self):
        """ Parse file line by line. """
        try:
            with open(self.uri, 'r') as fd:
                for line in fd.read().splitlines():
                    self.check(line)
        except IOError:
            raise ConfigurationFileException(
                'Failed to read configuration file \'%s\'' % self.uri
            )

    def check(self, str, *args, **kwargs):
        """ Check given string with registered handler. """
        value, handler = self.search(str)

        if not handler:
            handler = self.default_handler
            value = str

        if not handler:
            raise PyoliteLexerException('Not any handler found, please provide a default handler')

        return handler(value, *args, **kwargs)

    __call__ = check
