# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys
import socket


import bluetooth._bluetooth as bluez
socke=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dev_id = 1
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
	returnedList = blescan.parse_events(sock, 1)
	# print "----------"
	for beacon in returnedList:
		socke.sendto(beacon.encode('utf8'),("127.0.0.1" ,7777))
		# print beacon.encode('utf8')
