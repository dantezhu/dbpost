#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
启动dbpost
eg.
run_dbpost.py -p 35000 -s 'l%t-$72o67!hs1-^!1&ayj5uf2b39s57' -d
"""

import imp
import argparse

import sys
import dbpost
from dbpost.server import Server
from dbpost import constants


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--host', default=constants.SERVER_HOST, help='bind host', action='store')
    parser.add_argument('-p', '--port', default=constants.SERVER_PORT, type=int, help='bind port', action='store')
    parser.add_argument('-c', '--config', help='config file', action='store', required=False)
    parser.add_argument('-v', '--version', action='version', version='%s' % dbpost.__version__)
    return parser


def load_config(filename):
    d = imp.new_module('config')
    d.__file__ = filename
    try:
        with open(filename) as config_file:
            exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
    except IOError as e:
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise
    return d


def run():
    args = build_parser().parse_args()

    app = Server(config=load_config(args.config) if args.config else None)
    try:
        app.run(args.host, args.port)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    run()
