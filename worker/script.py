import ibapi
from ib_insync import *

ib = IB()
ib.connect('tws', 4003, clientId=1)

contract = Forex('EURUSD')
bars = ib.reqHistoricalData(contract, endDateTime='', durationStr='600 S',
        barSizeSetting='1 min', whatToShow='MIDPOINT', useRTH=True)
