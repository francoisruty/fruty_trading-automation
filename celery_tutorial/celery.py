from __future__ import absolute_import, unicode_literals

from celery.schedules import crontab
import os, sys, logging
import time, datetime, pytz
from datetime import datetime as dt
from datetime import datetime
import pandas as pd
import numpy as np
from random import randint
from importlib import reload
from ib_insync import *
import asyncio
util.logToConsole(logging.INFO)
util.patchAsyncio()
import mysql.connector
from io import StringIO

# sys.path.remove('/opt/project/_docker/ML-IB-Trading-Docker/celery_tutorial')
# sys.path.remove('/opt/project/_docker/ML-IB-Trading-Docker/celery_tutorial')
# sys.path.remove('/opt/project/_docker/ML-IB-Trading-Docker/celery_tutorial/C')
from celery import Celery
# sys.path.append('/opt/project/_docker/ML-IB-Trading-Docker/celery_tutorial')

from .fnLibrary import setPandas, fnOdbcConnect, fnUploadSQL
setPandas()

app = Celery('celery_tutorial', broker=os.environ['BROKER'], backend='rpc://',include=['celery_tutorial.ibClient.main'])

# --------------------------------------------------------------------------------------------------
# connect to db

connTrading = fnOdbcConnect('defaultdb')

CELERYBEAT_SCHEDULE = {
    'fnIBTrader': {
        'task': 'celery_tutorial.ibClient.main.fnRunIBTrader',
        'schedule': crontab(
                # hour ='*/',
                            minute='*/10',
                day_of_week = '1,2,3,4,5'),
        'args': ()
    },
}

app.conf.update(
        CELERYD_PREFETCH_MULTIPLIER = 1,
        CELERYD_CONCURRENCY = 1,
        CELERY_ACKS_LATE = True,
        C_FORCE_ROOT = True,
        CELERYBEAT_SCHEDULE = CELERYBEAT_SCHEDULE,
        CELERY_TIMEZONE = 'US/Central'
)


# --------------------------------------------------------------------------------------------------
# tasks

@app.task
def sleep(seconds):
    time.sleep(seconds)

@app.task
def echo(msg, timestamp=False):
    return "%s: %s" % (datetime.now(), msg) if timestamp else msg

@app.task
def error(msg):
    raise Exception(msg)
