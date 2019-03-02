bind = ['0.0.0.0:5000']
daemon = False
workers = 2
max_requests = 4096
max_requests_jitter = (max_requests // 100) or 100
worker_class = 'gevent'

loglevel = 'info'
reload = False
accesslog = "-"
errorlog = "-"
