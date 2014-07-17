# -*- coding: utf-8 -*-
"""
传输格式为:
    uri 连接mongodb的uri，格式:
            mongodb://user:password@example.com:port/the_database
            mysql://user:password@localhost/mydatabase
            sqlite:///mydatabase.db
    tb  表名
    m   数据(dict)
"""

import logging
from gevent.server import DatagramServer
from gevent.lock import Semaphore
from collections import deque, defaultdict
import pymongo
import dataset
import constants
from utils import decrypt

logger = logging.getLogger('dbpost')


class ObjKeeper(object):
    """
    每种资源
    """

    def __init__(self, max_size):
        self.lock = Semaphore(max_size)
        self.objs = deque()

    def pop(self):
        # 获取锁
        self.lock.acquire()

        try:
            return self.objs.popleft()
        except:
            # 代表外面要重新生成新的
            return None

    def push(self, obj):
        if obj:
            self.objs.append(obj)

        # 无论如何都要释放
        self.lock.release()


class Server(object):
    keeper_dict = None

    def __init__(self, secret=None, max_pool_size=None):
        """
        max_pool_size   每个uri对应的最多的client数
        """
        self.secret = secret
        self.max_pool_size = max_pool_size or constants.MAX_POOL_SIZE
        self.keeper_dict = defaultdict(lambda: ObjKeeper(self.max_pool_size))

    def process(self, data, address):
        values = decrypt(self.secret, data)
        if not values:
            logger.error('values is None. data: %s', data)
            return
        logger.debug('values: %s', values)

        uri = values['uri']
        tb_name = values['tb']
        model = values['m']

        keeper = self.keeper_dict[uri]

        saver = None
        try:
            saver = keeper.pop()

            # 要根据对应的uri生成saver
            if uri.startswith('mongodb'):
                if not saver:
                    saver = pymongo.MongoClient(uri)

                # uri 里面写的那个db
                db = saver.get_default_database()
                tb = getattr(db, tb_name)
                tb.save(model)
            else:
                if not saver:
                    saver = dataset.connect(uri)

                tb = saver[tb_name]
                tb.insert(model)
        except:
            logger.error('exc occur', exc_info=True)
        finally:
            keeper.push(saver)

    def run(self, host, port):
        server = DatagramServer((host, port), self.process)
        server.serve_forever()
