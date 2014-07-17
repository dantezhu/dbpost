# -*- coding: utf-8 -*-

import pickle
from crypto_helper import ARC4Wrapper


def encrypt(secret, dict_data):
    dumps_data = pickle.dumps(dict_data)
    if not secret:
        return dumps_data

    client = ARC4Wrapper(secret)
    return client.encrypt_hex(dumps_data)


def decrypt(secret, plain_data):
    if not secret:
        dumps_data = plain_data
    else:
        client = ARC4Wrapper(secret)
        try:
            dumps_data = client.decrypt_hex(plain_data)
        except:
            return None

    try:
        return pickle.loads(dumps_data)
    except:
        return None
