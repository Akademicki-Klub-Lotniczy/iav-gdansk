import logging
import time
from exceptions import EnteredFindMarkerState, EnteredFlyAlongAngleState

import nav_utils
import settings

from .state import State

logger = logging.getLogger(__name__)


class FlyAlongAngleState(State):

    def __init__(self):
        self.markers_found = []

    def run(self):
        while True:
            try:
                uuid, major, minor, rssi = self.bluetooth_data_queue.get(False)

                if uuid not in self.markers_found:
                    self.markers_found.append(uuid)
                else:
                    #print('already in')
                    raise ValueError  # Dirty whatever exception, just to keep the loop goin
            except:
                self.vehicle.simple_goto(
                    nav_utils.calculate_target_point(
                        self.vehicle, self.targetAngle
                    ), groundspeed=settings.FLIGHT_SPEED
                )
                time.sleep(0.5)
                continue

            logging.info('Detected', uuid)
            raise EnteredFindMarkerState(self.targetAngle, self.starting_angle, uuid, major, minor)

    def get_data_from_exception(self, exception: EnteredFlyAlongAngleState):
        self.targetAngle = exception.new_target_angle

        if exception.starting_angle is not None:
            self.starting_angle = exception.starting_angle

        if exception.reset_found_beacons:
            self.markers_found = []