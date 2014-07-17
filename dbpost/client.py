# -*- coding: utf-8 -*-

import socket
from utils import encrypt
import constants


class Client(object):
    host = None
    port = None
    secret = None

    sock = None

    def __init__(self, secret=None, host=None, port=None):
        self.host = host or constants.SERVER_HOST
        self.port = port or constants.SERVER_PORT
        self.secret = secret

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def put(self, msg):
        data = encrypt(self.secret, msg)
        self.sock.sendto(data, (self.host, self.port))
