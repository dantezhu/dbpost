# -*- coding: utf-8 -*-

from dbpost.client import Client

#client = Client('l%t-$72o67!hs1-^!1&ayj5uf2b39s57', '127.0.0.1', 35000)
client = Client()

client.put(
    dict(
        uri='mongodb://dantezhu:dantezhu@127.0.0.1/dogrun_dev_statistic',
        tb='user',
        m=dict(
            name='dantezhu',
            password='dantezhu',
        )
    )
)

client.put(
    dict(
        uri='mysql://root@127.0.0.1/test_stat',
        tb='user',
        m=dict(
            name='dantezhu',
            password='dantezhu',
        )
    )
)
