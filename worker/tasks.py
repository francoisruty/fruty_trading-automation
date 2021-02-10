from worker.celery import app
import psycopg2
import datetime
import os
from random import randint
import ibapi
from ib_insync import *

ib = IB()
#we cannot hardcode client id since this code will be run by multiple containers
id = randint(0, 9999)
ib.connect('tws', 4003, clientId=id)
contract = Forex('EURUSD')

conn = psycopg2.connect("dbname='trading' user='trading' host='postgres' password='trading'")
conn.autocommit = True

app.conf.beat_schedule = {
    'fetch-historic-data': {
        'task': 'fetch',
        'schedule': 60.0, #every 1min
        'args': ()
    },
}

def logger(filename, string):
    # trigger str method only if string is int. If string is a string, it may fail when special chars are present
    # We cannot use .encode all the time since it does not work on ints
    if string is None:
        return ''

    string = str(string)
    filename = "/logs/" + filename + ".txt"

    if os.path.exists(filename):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    try:
        file = open(filename, append_write)
        file.write(string.encode('utf-8') + '\n')
        file.close()
    except:
        return 'ERROR LOGGING STUFF'
    return ''


def insertRecordsDB(rows):
    try:
        cur = conn.cursor()
    except:
        raise ValueError('Unable to connect to DB')

    #we fill with the new records
    columnsNb = len(rows[0])
    stri = "(DEFAULT,"
    for k in range(0,columnsNb-1):
        stri = stri + "%s,"
    stri = stri + "%s)"
    for row in rows:
        args_str = cur.mogrify(stri, row).decode('utf-8')
        sql = "INSERT INTO " + "forex_data_EURUSD" + " VALUES " + args_str + " ON CONFLICT DO NOTHING"
        print(sql)
        cur.execute(sql)

@app.task(name='fetch')
def fetch():
    #we fetch historic data of last 300s (5min), with granularity 1min
    bars = ib.reqHistoricalData(contract, endDateTime=datetime.datetime.now(), durationStr='300 S',
            barSizeSetting='1 min', whatToShow='MIDPOINT', useRTH=True)
    rows = [[bar.date, bar.open] for bar in bars]
    print(rows)
    insertRecordsDB(rows)
