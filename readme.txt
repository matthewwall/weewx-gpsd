gpsd - driver for gpsd
Copyright 2014 Matthew Wall
Distributed under terms of the GPLv3

Installation instructions:

0) install the python bindings for gpsd:

sudo apt-get install python-gps

1) run the installer:

wee_extension --install weewx-gps.tgz

2) modify weewx.conf, mapping database fields to devices, for example:

[Station]
    station_type = GPSd

[GPSd]
    driver = user.gpsd
    [[sensor_map]]
        windBatteryStatus = latitude
        rainBatteryStatus = longitude
        outTempBatteryStatus = altitude

3) start weewx

sudo /etc/init.d/weewx start
