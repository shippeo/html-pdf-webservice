"""
    html-pdf-webservice

    Copyright 2014 Nathan Jones
    See LICENSE for more details
"""

# Gunicorn server config
# See http://docs.gunicorn.org/en/latest/settings.html
import multiprocessing


bind = "0.0.0.0:80"
workers = multiprocessing.cpu_count() * 2
errorlog = "-"
