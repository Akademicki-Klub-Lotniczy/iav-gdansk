from abc import ABC, abstractmethod
import multiprocessing


from exceptions import \
    EnteredFindMarkerState, \
    EnteredFlyAlongAngleState, \
    EnteredLandingState


from dronekit import \
    connect, \
    VehicleMode, \
    LocationGlobalRelative

import flight_utils
import nav_utils
import settings
import time
import sys
# import background
import hex_utils
from dronekit import Vehicle
import queue


'''

    Drone is driven by a state-based system, with each state representing another behaviour,
    that is required for the contest.

    If the state decides, that its done its work and is ready to transition,
    it raises an Exception that indicates:
    * what should the next state be (defined by the type of exception, eg: EnteredFlyAlongAngleState enters the FlyAlongAngleState)
    * what data is passed to the next state (defined by the custom exception fields, eg: angle in the exception above)

+---------------------------------------------------------------------------------------------------------------------------------------+

    Flow of the states

     +-------+
     \ Start \ 
     +---+---+
         \ 
         \ 
         v
+----------------------------+                                        +--------------------------+
|                            |                                        |                          |
|  CalibrateAndLaunchState   |                                        | FlyAlongAngleState       |
|                            |    EnteredFlyAlongAngleState (angle)   |                          |
| Arms the drone,            |                                        | Drives the drone towards |
| reads the starting heading +--------------------------------------->+ a given angle, until     |
| and takes off              |                                        | a beacon is detected     |
|                            |                                        |                          |
+----------------------------+                                        +----+------------+--------+
                                                                           ^            |
                                                                           |            |
                                                                           |            |
                                         EnteredFlyAlongAngleState (angle) |            | EnteredFindMarkerState(angle)
                                                                           |            |
                                                                           |            |
                                                                           |            v
+----------------------------+                                        +----+------------+--------+
|                            |                                        |                          |
| LandOnFinalMarkerState     |   EnteredLandingState (lat, lon)       | FindMarkerCrossMethod    |
|                            |                                        |                          |
| Positions the drone above  +<---------------------------------------+ Locates a marker and     |
| the final marker,          |                                        | flies right above it     |
| then lands, voila!         |                                        |                          |
|                            |                                        | Then reads the marker    |
+---------+------------------+                                        | data and decides to land |
          \                                                           | or to continue searching |
          \                                                           |                          |
          v                                                           +--------------------------+
       +-----+
       \ End \ 
       +-----+
'''


class State(ABC):
    '''
    bluetooth_data_queue, location_data_queue and vehicle are static 
    objects, shared across all states and accessible in all states
    '''
    bluetooth_data_queue = multiprocessing.Queue()
    location_data_queue = multiprocessing.Queue()

    connection_string = '127.0.0.1:14550'
    if len(sys.argv) > 1:
        connection_string = sys.argv[1]

    vehicle = connect(connection_string, baud=57600, wait_ready=True)

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def get_data_from_exception(self, exception):
        pass

    def clear_bt_queue(self):
        try:
            while True:
                self.bluetooth_data_queue.get(False)
        except queue.Empty:
            return