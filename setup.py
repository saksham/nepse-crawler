#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def read_file(filename):
    with open(path.join(here, filename)) as f:
        return f.read()

setup(name='nepse-crawler',
      version='0.0.1',
      description='Crawls websites for Nepal Stock Exchange and loads them to SQLite3 database',
      long_description=read_file('README.md'),
      url='https://github.com/saksham/nepse-crawler',
      install_requires=read_file('requirements.txt'),
      author='Saksham',
      author_email='saksham@no-reply.github.com',
      license='MIT',
      packages='crawler',
      entry_points={
            'console_scripts': [
                  'crawler.__main__'
            ]
      })
