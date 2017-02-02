# -*- coding: utf-8 -*-

"""Gitolite configuration file abstraction.

This module contains functions to parse and abstract a Gitolite configuration
file.
"""

import re
from .repository import Bundle
from .rule import Rule

P_COMMENT = '^\s*#\s*([\S\s]*?)\s*$'
P_GROUP   = '^@(\S+)\s*=\s*([\S\s]*?)\s*$'
P_REPO    = '^repo\s+([\S\s]*?)\s*$'
P_INCLUDE = '^include\s+"?([\S\s]*?)"?\s*$'
P_RULE    = '^\s*(-|C|R|RW\+?(?:C?D?|D?C?)M?)\s+(\S*)?\s*=\s*([\S\s]*?)\s*$'
P_CONFIG  = '^\s*config\s*(\S+\s*=\s*.*)'
P_EMPTY   = '^\s*$'
P_TYPE    = type(re.compile('.'))

class FileError(Exception):
    """ FileError is an Exception thrown by File objects. """
    pass

class File(object):
    """ This class represents a Gitolite configuration file. """

    def __init__(self, pyolite, uri):
        """ Initialize a Gitolite configuration file. """
        # Store parent pyolite object
        self.pyolite = pyolite
        self.uri = uri
        self.tree = []
        self.last_bundle = None

    def load(self):
        """ Load this Gitolite configuration file. """
        # Instance lexer from file URI
        lexer = Lexer(self.uri)
        self.last_bundle = None

        @lexer.default
        def gotDefault(str, *args, **kwargs):
            raise FileError("Unrecognized string: '%s'" % str)

        @lexer.op([P_EMPTY, P_COMMENT])
        def gotEmptyLine(matches, *args, **kwargs):
            # Even it's an empty line, add it to our tree in order to dump it later
            self.tree.append(matches.group(0))


        @lexer.op(P_REPO)
        def gotRepo(matches, *args, **kwargs):
            name = matches.group(1)

            # Save last bundle
            self.last_bundle = Bundle([name])

            # Insert bundle into tree
            self.tree.append(self.last_bundle)
            # Insert bundle into existing repository or create it !
            self.pyolite.repos.get_or_create(name).append(self.last_bundle)

        @lexer.op(P_RULE)
        def gotRule(matches, *args, **kwargs):
            # Make sure we already parse a bundle
            if self.last_bundle == None:
                raise ValueError('Malformed Gitolite configuration')

            # Instance Rule object
            rule = Rule(matches.group(1), matches.group(2))
            # Insert its users
            rule += re.split('\s+', matches.group(3))

            # Append last parsed bundle in tree
            self.last_bundle.append(rule)

        lexer.parse()

    def __str__(self):
        def dump_entry(entry): return entry.__str__()

        return '\n'.join(map(dump_entry, self.tree))

class LexerError(Exception):
    """ LexerError is an exception thrown by Lexer objects. """
    pass

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
                        raise LexerError('duplicate regex case value \'%s\'' % regex.pattern)
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
        with open(self.uri) as fd:
            for line in fd.read().splitlines():
                self.check(line)

    def check(self, str, *args, **kwargs):
        """ Check given string with registered handler. """
        value, handler = self.search(str)

        if not handler:
            handler = self.default_handler
            value = str

        if not handler:
            raise LexerError('failure')

        return handler(value, *args, **kwargs)

    __call__ = check
