# $Id: install.py 1490 2016-05-03 14:39:16Z mwall $
# installer for GPSd
# Copyright 2014 Matthew Wall

from setup import ExtensionInstaller

def loader():
    return GPSdInstaller()

class GPSdInstaller(ExtensionInstaller):
    def __init__(self):
        super(GPSdInstaller, self).__init__(
            version="0.3",
            name='gpsd',
            description='driver for gpsd',
            author="Matthew Wall",
            author_email="mwall@users.sourceforge.net",
            files=[('bin/user', ['bin/user/gpsd.py'])]
            )
