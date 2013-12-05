#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

from catcher._version import __version__

setup(
    name='python-catcher',
    version=__version__,
    install_requires=[
        'requests', 'Mako',
    ],
    description='Beautiful stack traces for Python',
    author='Eugene Pankov',
    author_email='e@ajenti.org',
    url='http://ajenti.org/',
    packages=find_packages(exclude=['*test*']),
)
