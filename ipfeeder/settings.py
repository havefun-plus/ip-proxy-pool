import os
from logging.config import dictConfig

# ----- general settings -----

# 定时任务所在路径
CRONJOBS_MODULE = 'ipfeeder.cronjobs'

# queue 配置

# use redis queue
JOB_QUEUE_NAME = 'default'

REDIS_SETTINGS = dict(
    host=os.getenv('REDIS_HOSTNAME', '0.0.0.0'),
    port=6379,
    db=0,
    password=None,
)

# QUEUE_CONFIG = dict(queue_type='redis', config=REDIS_SETTINGS)

# use `queue` or `multiprocessing.Queue`
QUEUE_CONFIG = dict(queue_type='redis', config=REDIS_SETTINGS)
# QUEUE_CONFIG = dict(queue_type='process', config=None)


# gevent worker queue size
DEFAULT_TASK_QUEUE_SIZE = 100

# ----- spider job settings -----

# 是否使用代理
ENABLE_PROXY = False

# 针对每个请求的时间限制，不同于requests的timeout
REQUEST_TIMEOUT = 30

# 爬取失败或者http code错误时候需要重试的次数
RETRY_TIMES = 10

# 是否需要更换user agent
ENABLE_REPLACE_USER_AGENT = True


# ---- urls for validate https -----
VALIATE_HTTPS_URLS = ['https://httpbin.org/ip', 'https://eu.httpbin.org/ip']
VALIATE_HTTP_URLS = ['http://httpbin.org/ip', 'http://eu.httpbin.org/ip']


# ---- logging settings ----
LOGGING_SETTINGS = dict(
    version=1,
    formatters={
        'default': {
            '()': 'cronjob.utils.utils.Formatter',
            'format':
            '[{asctime}][{levelname}][{module}][{funcName}]: {message}',
            'style': '{'
        },
    },
    handlers={
        'stdout': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
        },
    },
    loggers={
        'cronjob': {
            'handlers': ['stdout'],
            'level': 'INFO',
        },
        'ipfeeder': {
            'handlers': ['stdout'],
            'level': 'DEBUG',
        },
    },
)

dictConfig(LOGGING_SETTINGS)
