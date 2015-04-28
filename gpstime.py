#!/usr/bin/python

import sys
import time
from gps import *

USE_DATE_COMMAND = False
#USE_DATE_COMMAND = True



print 'Attempting to acquire GPS time...'

try:
	gpsd = gps(mode=WATCH_ENABLE)
except:
	print 'No GPSd connection. TIME NOT SET.'
	sys.exit(1)


if USE_DATE_COMMAND:
	from subprocess import call
	# timestr looks like:  2015-04-01T23:43:21
	# extracting the fields should not be needed for 'date'
	def set_time(timestr):
		#timestr = timestr[0:4] + timestr[5:7] + timestr[8:10] + ' ' + timestr[11:19]
		return call(['date', '--utc', '--set', timestr])
else:
	# man 2 settimeofday
	import ctypes
	import ctypes.util
	import struct
	from calendar import timegm
	libc = ctypes.CDLL(ctypes.util.find_library('c'))
	def set_time(timestr):
		tsec = timegm(time.strptime(timestr, '%Y-%m-%dT%H:%M:%S'))
		# nanoseconds delay from gps msg to set - a fractional second
		tfrac = 800000000
		tpack = struct.pack('2q', tsec, tfrac)
		# (Q=u64, q=s64, l=s32, L=u32)
		return libc.settimeofday(tpack, None)
		#libc.gettimeofday(tpack, None)




# gpsd.utc looks like: 2015-04-01T23:43:21.000Z

rv = 0
while True:
	gpsd.next()
	if gpsd.utc:
		gpstime = gpsd.utc[0:19]
		systime = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
		print '     GPS time: %s\n  System time: %s' % (gpstime,systime)
		if gpstime == systime or \
		   (gpstime[:18] == systime[:18] and \
		    abs(int(gpstime[18]) - int(systime[18])) < 2):
			print 'System time near enough to GPS time. Not resetting.'
			break
		print 'Setting system time to GPS time'
		rv = set_time(gpstime)
		if rv:
			print '0x%04x: Command failed. TIME NOT SET.' % (0xffff & rv)
			break
		print 'System time set.'
		break
	time.sleep(0.4)

sys.exit(rv)
