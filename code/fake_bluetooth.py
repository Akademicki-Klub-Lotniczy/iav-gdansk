import multiprocessing
import sys
import time
from geopy.distance import geodesic
from beacon_simulator import BeaconSimulator
from states.state import State
from dronekit import mavutil
import logging 

logger = logging.getLogger(__name__)

def scan_bt(bluetooth_data_queue: multiprocessing.Queue, location_data_queue: multiprocessing.Queue, beacons_to_simulate):
    while location_data_queue.empty():
        logger.debug('waiting for GPS')
        time.sleep(1)
    logger.info('GPS reached')

    lat, lon = location_data_queue.get()

    while True:
        try:
            lat, lon = location_data_queue.get(False)
        except:
            pass
        finally:
            
            for b in beacons_to_simulate:
                distance = geodesic([lat, lon], [b.lat, b.lon]).m
                
                logger.debug(b.uuid , distance)

                if b.will_tick_100_ms(distance):
                    logger.debug(b.uuid, 'tick!')
                    bluetooth_data_queue.put(
                        (b.uuid, b.major, b.minor, b.get_rssi_for(distance))
                    )

            time.sleep(0.1)


if __name__ == '__main__':
    scan_bt(None)
