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

import time
import datetime
from threading import Semaphore
import SocketServer
from collections import deque, defaultdict
import pymongo
import dataset
import constants
from utils import decrypt
from log import logger


class ObjKeeper(object):
    """
    每种资源
    """

    active_time = None

    def __init__(self, max_size):
        self.active_time = time.time()
        self.lock = Semaphore(max_size)
        self.objs = deque()

    def pop(self):
        self.active_time = time.time()

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

    def __init__(self, secret=None, max_pool_size=None, max_uri_count=None):
        """
        max_pool_size   每个uri对应的最多的client数
        max_uri_count   最多可以有多少个uri
        """
        self.secret = secret
        self.max_pool_size = max_pool_size or constants.MAX_POOL_SIZE
        self.max_uri_count = max_uri_count or constants.MAX_URI_COUNT
        self.keeper_dict = defaultdict(lambda: ObjKeeper(self.max_pool_size))

    def handle_message(self, message, address):
        # TODO 等升级完删掉
        # 即时server本身支持了密钥，也要支持没有加密的数据
        try_secret_list = [self.secret, None] if self.secret else [self.secret]

        values = None
        for secret in try_secret_list:
            values = decrypt(secret, message)
            if values:
                break
        else:
            # 没有找到能正常解出values的
            logger.error('values is None. message: %r', message)
            return

        # 以后还是变回这样
        # values = decrypt(self.secret, message)
        # if not values:
        #     logger.error('values is None. message: %r', message)
        #     return

        logger.debug('values: %r', values)

        uri = self._extract_string(values['uri'])
        tb_name = self._extract_string(values['tb'])
        model = values['m']

        keeper = self.keeper_dict[uri]

        self._check_and_remove_exceed_uri()

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

    def _check_and_remove_exceed_uri(self):
        """
        检测超过的uri数量，并且删除
        多线程访问，锁的问题得考虑下
        :return:
        """
        if self.max_uri_count is None or len(self.keeper_dict) <= self.max_uri_count:
            # 不限制大小或者还没有达到限制
            return

        # 从大到小排列
        exceed_item_list = sorted(self.keeper_dict.items(), key=lambda x: -x[1].active_time)[self.max_uri_count:]

        for uri, keeper in exceed_item_list:
            # 删除
            self.keeper_dict.pop(uri, None)

    def _extract_string(self, uri):
        """
        展开string, 替换对应的占位符
        placeholder: year, month, day, hour, minute, second
        :param uri:
        :return:
        """

        now = datetime.datetime.now()

        return uri.format(
            year='%04d' % now.year,
            month='%02d' % now.month,
            day='%02d' % now.day,
            hour='%02d' % now.hour,
            minute='%02d' % now.minute,
            second='%02d' % now.second,
        )

    def run(self, host, port):
        class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
            def handle(sub_self):
                message = sub_self.request[0]
                try:
                    self.handle_message(message, sub_self.client_address)
                except:
                    logger.error('exc occur.', exc_info=True)

        server = SocketServer.ThreadingUDPServer((host, port), ThreadedUDPRequestHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        except:
            logger.error('exc occur.', exc_info=True)
