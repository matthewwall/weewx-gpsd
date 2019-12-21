#!/usr/bin/python
# $Id: gpsd.py 1377 2015-10-27 22:32:30Z mwall $
# Copyright 2014 Matthew Wall

import math
import syslog
import threading
import time

from gps import *

import weewx.drivers

DRIVER_NAME = "GPSd"
DRIVER_VERSION = "0.3"

def logmsg(dst, msg):
    syslog.syslog(dst, 'gpsd: %s' % msg)

def logdbg(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)

def loader(config_dict, engine):
    return GPSd(**config_dict['GPSd'])


gps_schema = [('dateTime',  'INTEGER NOT NULL UNIQUE PRIMARY KEY'),
              ('usUnits',   'INTEGER NOT NULL'),
              ('interval',  'INTEGER NOT NULL'),
              ('latitude',  'REAL'),
              ('longitude', 'REAL'),
              ('altitude',  'REAL'),
              ('speed',     'REAL'),
              ('climb',     'REAL'),
              ('numsat',    'REAL')]


class GPSPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gps = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True

    def run(self):
        while self.running:
            self.gps.next()


class GPSd(weewx.drivers.AbstractDevice):

    def __init__(self, **stn_dict):
        loginf("driver version is %s" % DRIVER_VERSION)
        self.poll_interval = float(stn_dict.get('poll_interval', 30))
        loginf("polling interval is %s" % self.poll_interval)

        self.poller = GPSPoller()
        logdbg("starting the polling thread")
        self.poller.start()

    def closePort(self):
        logdbg("tell poller to stop running")
        self.poller.running = False
        logdbg("waiting for polling thread to complete")
        self.poller.join()

    def genLoopPackets(self):
        while True:
            _packet = {'dateTime': int(time.time() + 0.5),
                       'usUnits': weewx.US}
            for n in ['latitude', 'longitude', 'altitude', 'speed', 'climb']:
                _packet[n] = getattr(self.poller.gps.fix, n)
                if math.isnan(float(_packet[n])):
                    _packet[n] = None
            _packet['numsat'] = len(self.poller.gps.satellites)
            yield _packet
            time.sleep(self.poll_interval)

    @property
    def hardware_name(self):
        return "GPSd"

# To test this driver, do the following:
#   PYTHONPATH=/home/weewx/bin python /home/weewx/bin/user/gpsd.py
if __name__ == "__main__":
    import weeutil.weeutil
    station = GPSd()
    try:
        for packet in station.genLoopPackets():
            print weeutil.weeutil.timestamp_to_string(packet['dateTime']), packet
    finally:
        station.closePort()
