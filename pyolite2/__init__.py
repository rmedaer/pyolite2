# -*- coding: utf-8 -*-

"""Pyolite 2

Python module to manage Gitolite; a centralized Git hosting server.

"""

__version__ = '0.1.0'

from .file import File
from .pyolite import Pyolite
from .rule import Rule
from .repository import (
    Repository,
    RepositoryCollection,
    RepositoryNotFoundError
)
