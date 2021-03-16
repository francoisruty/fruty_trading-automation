# main.py
#
# created by joe.loss, November 2020
# --------------------------------------------------------------------------------------------------
# Parameters

ticker = 'EURUSD'
ticker_at = 'EQT'
LOG_LEVEL = 'INFO'

# --------------------------------------------------------------------------------------------------
# Module Imports

import os, sys, logging
import pandas as pd
import numpy as np
from datetime import datetime as dt
from ib_insync import Stock, ContFuture, Future, Forex

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from celery_tutorial.fnLibrary import setPandas, fnOdbcConnect, setLogging, fnUploadSQL
from celery_tutorial.ibClient.models.ibAlgo import HftModel1


# --------------------------------------------------------------------------------------------------
# create IB contract symbiology

def fnCreateIBSymbol(ticker_tk=None, ticker_at=None):

    if not ticker_tk:
        ticker_tk = 'SPY'
    if not ticker_at:
        ticker_at = 'EQT'

    symIB = None

    if ticker_at == 'EQT':
        symIB = [ticker_tk, Stock(ticker_tk, 'SMART', 'USD')]
    elif ticker_at == 'FUT':
        symIB = [ticker_tk, Future(ticker_tk, 'SMART', 'USD')]
    elif ticker_at == 'FX':
        symIB = [ticker_tk, Forex(ticker_tk,'IDEALPRO')]

    return symIB

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# run main

from celery_tutorial.celery import app

@app.task
def fnRunIBTrader():

    setPandas()
    setLogging(LOGGING_DIRECTORY = os.path.join('../logging/', dt.today().strftime('%Y-%m-%d')),
               LOG_FILE_NAME = os.path.basename(__file__),
               level = LOG_LEVEL)

    logging.info('Running script {}'.format(os.path.basename(__file__)))
    logging.info('Process ID: {}'.format(os.getpid()))
    curDate = dt.today().strftime('%Y-%m-%d')

    try:
        TWS_HOST = os.environ.get('TWS_HOST', 'tws')
        TWS_PORT = os.environ.get('TWS_PORT', 4003)
        logging.info('Connecting on host: {} port: {}'.format(TWS_HOST, TWS_PORT))

        tickerIB = fnCreateIBSymbol(ticker_tk = 'SPY', ticker_at = 'EQT')
        ib = IB()

        # connect
        connTrading = fnOdbcConnect(user = 'admin', password = 'password', host = '127.0.0.1', port = '3306', dbName = 'trading')

        while True:
            if not ib.isConnected():
                try:
                    id = randint(0, 9999)
                    ib.connect('tws', 4003, clientId=id, timeout=60)
                    ib.waitonupdate(timeout=0.1)
                    ib.sleep(3)
                    break
                except Exception as e:
                    print(e)
                    ib.waitonupdate(timeout=0.1)
                    ib.sleep(3)
                    continue

            else:
                contract = Forex('EURUSD')
                bars = ib.reqHistoricalData(contract, endDateTime='', durationStr='600 S', barSizeSetting='1 min', whatToShow='MIDPOINT', useRTH=False, keepUpToDate = False)
                bars = util.df(bars)

                bars['date'] = pd.to_datetime(bars['date']).dt.tz_localize('UTC').dt.strftime('%Y-%m-%d %H:%M:%S')
                bars = bars[['date', 'open', 'high', 'low', 'close', 'volume', 'average']]
                fnUploadSQL(bars, connTrading, 'forex_data_EURUSD', 'REPLACE', None, unlinkFile = True)


        logging.info('----- END PROGRAM -----')

    except Exception as e:
        logging.error(str(e), exc_info=True)

    # CLOSE LOGGING
    for handler in logging.root.handlers:
        handler.close()
    logging.shutdown()
