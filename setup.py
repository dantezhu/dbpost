# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
setup(
    name="dbpost",
    version="0.2.19",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['pymongo', 'dataset'],
    scripts=['dbpost/bin/run_dbpost.py'],
    url="https://github.com/dantezhu/dbpost",
    license="BSD",
    author="dantezhu",
    author_email="zny2008@gmail.com",
    description="proxy for save db data. support mysql、sqlite、mongodb",
)
