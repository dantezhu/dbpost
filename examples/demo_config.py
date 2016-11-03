# -*- coding: utf-8 -*-


# 密钥
SECRET = None

# 每个uri对应的最多的client数
# MAX_POOL_SIZE = 50

# 最多可以有多少个uri
# MAX_URI_COUNT = 50


LOG_FORMAT = '\n'.join((
    '/' + '-' * 80,
    '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d %(funcName)s]:',
    '%(message)s',
    '-' * 80 + '/',
))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'standard': {
            'format': LOG_FORMAT,
        },
    },

    'handlers': {
        'flylog': {
            'level': 'ERROR',
            'class': 'flylog.LogHandler',
            'formatter': 'standard',
            'source': 'dbpost',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },

    'loggers': {
        'dbpost': {
            'handlers': ['console', 'flylog'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
