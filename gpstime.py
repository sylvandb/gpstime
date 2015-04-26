#!/usr/bin/python

import os
import sys
import time
from gps import *


print 'Attempting to acquire GPS time...'

try:
	gpsd = gps(mode=WATCH_ENABLE)
except:
	print 'No GPSd connection. TIME NOT SET.'
	sys.exit(1)


while True:
	gpsd.next()
	if gpsd.utc:
		gpstime = gpsd.utc[0:4] + gpsd.utc[5:7] + gpsd.utc[8:10] + ' ' + gpsd.utc[11:19]
		print 'Setting system time to GPS time: %s UTC' % gpstime
		rv = os.system('date --utc --set="%s"' % gpstime)
		if rv:
			print '0x%04x: Command failed. TIME NOT SET.' % rv
			sys.exit(2)
		print 'System time set.'
		break
	time.sleep(1)

sys.exit(0)
