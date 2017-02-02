# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyolite2',
    version='0.1.0',
    description='Gitolite admin repository manager.',
    long_description=readme,
    author='Raphael Medaer (Escaux)',
    author_email='rme@escaux.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

