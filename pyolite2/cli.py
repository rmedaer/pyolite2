# -*- coding: utf-8 -*-

import os
import sys
import click
from . import __version__
from .pyolite import Pyolite
from .switcher import ContextSwitcher

def version_msg():
    """ Returns the Pyolite2 version, location and Python powering it. """
    # [NOTE] Usage of click is inspired from cookicutter project
    python_version = sys.version[:3]
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    message = u'Pyolite2 %(version)s from {} (Python {})'
    return message.format(location, python_version)

# Defining command and options
@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.version_option(__version__, u'-V', u'--version', message=version_msg())
@click.argument(u'context')
@click.argument(u'command')
@click.option(
    u'-c', u'--config',
    help=u'main adming configuration path',
    default=u'gitolite.conf'
)
def main(context, command, config):
    # Instance a Pyolite object from admin configuration URI
    pyolite = Pyolite(config)
    pyolite.load()

    # Instance switcher to select context/command
    switcher = ContextSwitcher()

    # Define contexts and commands
    @switcher.command('repo', 'list')
    def list_repositories():
        """ List Git repositories. """
        for repo in pyolite.repos:
            print repo.name

    # Let's switch !
    switcher.switch(context, command)

if __name__ == "__main__":
    main()
