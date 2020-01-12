# installer for GPSd
# Copyright 2014 Matthew Wall
# Distributed under the terms of the GNU Public License (GPLv3)

from weecfg.extension import ExtensionInstaller

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
