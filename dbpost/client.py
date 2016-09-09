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

        # 为了兼容老版本
        self.put = self.post

    def post(self, msg):
        """
        发送数据
        这里考虑后还是决定不捕获异常，由调用方负责
        :param msg:
        :return: 发送成功的字节数
        """
        data = encrypt(self.secret, msg)
        # 返回的发送成功的字节数
        return self.sock.sendto(data, (self.host, self.port))
