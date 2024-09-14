from multiprocessing import cpu_count

 # Socket Path
bind = 'unix:/projects/auth_module/gunicorn.sock'

 # Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

 # Logging Options
loglevel = 'debug'
accesslog = '/projects/auth_module/access_log'
errorlog =  '/projects/auth_module/error_log'
