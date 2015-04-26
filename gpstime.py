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


# gpsd.utc looks like: 2015-04-01T23:43:21.000Z
# extracting the fields should not be needed
#gpstime = gpsd.utc[0:4] + gpsd.utc[5:7] + gpsd.utc[8:10] + ' ' + gpsd.utc[11:19]

rv = 0
while True:
	gpsd.next()
	if gpsd.utc:
		gpstime = gpsd.utc[0:19]
		systime = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
		print '     GPS time: %s\n  System time: %s' % (gpstime,systime)
		if gpstime == systime:
			print 'System time matches GPS time. Not resetting.'
			break
		print 'Setting system time to GPS time'
		rv = os.system('date --utc --set="%s"' % gpstime)
		if rv:
			print '0x%04x: Command failed. TIME NOT SET.' % rv
			break
		print 'System time set.'
		break
	time.sleep(1)

sys.exit(rv)
