#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    scripts=('bin/debian-devel-changes-bot.sh',),
    packages=find_packages(),
)
