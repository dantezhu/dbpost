# -*- coding: utf-8 -*-

"""
为网络使用，封装了一下常用的算法，直接用base64返回，就没那么多复杂的事了

depends:
    pycrypto
"""

import base64

from Crypto.Cipher import ARC4


class ARC4Wrapper(object):
    """
    ARC4算法的封装
    之所以在机密和解密函数都要新生成crypto_obj，是因为用同一个obj加密然后解密的结果不对
    """

    _secret = None

    def __init__(self, secret):
        self._secret = secret

    def encrypt64(self, src):
        crypto_obj = ARC4.new(self._secret)

        binary = crypto_obj.encrypt(src)
        return base64.encodestring(binary)
        
    def decrypt64(self, src):
        crypto_obj = ARC4.new(self._secret)

        binary = base64.decodestring(src)
        return crypto_obj.decrypt(binary)

    def encrypt_hex(self, src):
        crypto_obj = ARC4.new(self._secret)

        binary = crypto_obj.encrypt(src)
        return binary.encode('hex')
        
    def decrypt_hex(self, src):
        crypto_obj = ARC4.new(self._secret)

        binary = src.decode('hex')
        return crypto_obj.decrypt(binary)


if __name__ == '__main__':
    obj = ARC4Wrapper('sfsfsdf')

    x = obj.encrypt64('wokao')
    print x

    y = obj.decrypt64(x)
    print y 
