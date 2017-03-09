# -*- coding: utf-8 -*-

import os
import sys
import click
from . import __version__
from .pyolite import Pyolite

class CLIContext(object):
    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.pyolite = Pyolite(os.path.join(self.config_dir, u'gitolite.conf'))
        self.pyolite.load()

@click.group()
@click.option(
    u'-c', u'--config-dir',
    help=u'Admin configuration directory path.',
    default=u'conf',
    type=click.Path(exists=True)
)
@click.pass_context
def main(ctx, config_dir):
    # Transfer config parameter to context
    ctx.obj = CLIContext(config_dir)

@main.group()
@click.pass_context
def config(ctx, **kwargs):
    pass

@config.command()
@click.argument('files', nargs=-1, required=False)
@click.option(
    u'-a', u'--all',
    help=u'dump all files',
    is_flag=True
)
@click.pass_context
def dump(ctx, files, all):
    if not files and not all:
        ctx.fail('You have to provide at least one file or add --all option')

    if all:
        for file in ctx.obj.pyolite.files:
            print file
    else:
        for file in files:
            found = False
            for pyofile in ctx.obj.pyolite.files:
                if os.path.join(ctx.obj.config_dir, file) == pyofile.uri:
                    print pyofile
                    found = True
                    break

            if not found:
                ctx.fail('Configuration file \'%s\' not found' % file)

@main.group()
@click.pass_context
def repo(ctx, **kwargs):
    pass

@repo.command()
@click.pass_context
def list(ctx, **kwargs):
    for repo in ctx.obj.pyolite.repos:
        print repo.name

if __name__ == "__main__":
    main()
