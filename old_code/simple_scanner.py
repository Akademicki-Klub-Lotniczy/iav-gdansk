"""
Outputs the rssi to stdout

Just rssi - no mac or anything
"""

import sys
import asyncio
import argparse
import re
import aioblescan as aiobs
from aioblescan.plugins import EddyStone

import os
import time

import numpy as np
        
x_dim = int(input("X dim "))
y_dim = int(input("Y dim "))
time_for_segment = int(input("Time for each segment "))

rssi_measurements = np.zeros((y_dim, x_dim))

current_segment_time = time.time() + 1

current_x = 0
current_y = 0

direction = 1
number_of_measurements_this_segment = 0

def my_process(data):
    global current_x
    global current_y
    global direction
    global time_for_segment
    global current_segment_time
    global number_of_measurements_this_segment

    ev=aiobs.HCI_Event()
    xx=ev.decode(data)

    #print(xx)
    #return
    
    beacon=EddyStone().decode(ev)
    if beacon:
        #print("Google Beacon {}".format(beacon))
        rssi = beacon['rssi']
        #print(rssi)

        rssi_measurements[current_y][current_x] += rssi
        number_of_measurements_this_segment += 1
        # TODO SAVE RSSI
    
    if time.time() - current_segment_time > time_for_segment:
        
        print('MOVE')

        for i in range(0, 6):
            os.system('echo 1 >/sys/class/leds/led0/brightness')        
            time.sleep(0.1)
            os.system('echo 0 >/sys/class/leds/led0/brightness')        
            time.sleep(0.1)

        rssi_measurements[current_y][current_x] /= number_of_measurements_this_segment
        number_of_measurements_this_segment = 0

        current_x += direction
        if current_x == -1 or current_x == x_dim:
            current_x -= direction
            direction *= -1
            current_y += 1

        current_segment_time = time.time()

        print('moving to sector', current_x, current_y)


    if current_y == y_dim:
        print('ALL DONE')
        np.savetxt("foo.csv", rssi_measurements, delimiter=",")
        exit(0)
       
    #     #update_time = time.time() % 1000
        #print("{0}, {1}".format(rssi, update_time))
        

    
    #ev.show(0)

event_loop = asyncio.get_event_loop()

#First create and configure a raw socket
# 0th device by default -> in the case of RPi, that means the build-in bt antenna
mysocket = aiobs.create_bt_socket(0)

# create a connection with the raw socket
# This used to work but now requires a STREAM socket.
# fac=event_loop.create_connection(aiobs.BLEScanRequester,sock=mysocket)
# Thanks to martensjacobs for this fix
fac=event_loop._create_connection_transport(mysocket,aiobs.BLEScanRequester,None,None)
#Start it
conn,btctrl = event_loop.run_until_complete(fac)
#Attach your processing
btctrl.process=my_process


#Probe
btctrl.send_scan_request()

try:
    # event_loop.run_until_complete(coro)
    event_loop.run_forever()
except KeyboardInterrupt:
    print('keyboard interrupt')
finally:
    print('closing event loop')
    btctrl.stop_scan_request()
    conn.close()
    event_loop.close()
