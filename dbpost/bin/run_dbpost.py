#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
启动dbpost
eg.
run_dbpost.py -p 35000 -s 'l%t-$72o67!hs1-^!1&ayj5uf2b39s57' -d
"""

import argparse

import sys
import dbpost
from dbpost.server import Server
from dbpost import constants
from dbpost.log import logger


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--host', default=constants.SERVER_HOST, help='bind host', action='store')
    parser.add_argument('-p', '--port', default=constants.SERVER_PORT, type=int, help='bind port', action='store')
    parser.add_argument('-s', '--secret', help='secret', action='store')
    parser.add_argument('-m', '--max_pool_size', help='max_pool_size', type=int, action='store')
    parser.add_argument('-c', '--max_uri_count', help='max_uri_count', type=int, action='store')
    parser.add_argument('-v', '--version', action='version', version='%s' % dbpost.__version__)
    return parser


def run():
    args = build_parser().parse_args()

    logger.info("Running dbpost on %(host)s:%(port)s" % dict(
        host=args.host, port=args.port)
    )

    app = Server(args.secret, max_pool_size=args.max_pool_size, max_uri_count=args.max_uri_count)
    try:
        app.run(args.host, args.port)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    run()
