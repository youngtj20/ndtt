import multiprocessing
import os

bind = os.environ.get('GUNICORN_BIND', '127.0.0.1:8088')
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
threads = int(os.environ.get('GUNICORN_THREADS', '2'))
worker_class = 'sync'
backlog = 512
timeout = 60
loglevel = os.environ.get('GUNICORN_LOGLEVEL', 'info')
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
