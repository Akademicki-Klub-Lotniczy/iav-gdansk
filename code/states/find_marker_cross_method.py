import logging
import queue
import time
from exceptions import (EnteredFindMarkerState, EnteredFlyAlongAngleState,
                        EnteredLandingState)

from dronekit import LocationGlobalRelative

import flight_utils
import hex_utils
import nav_utils
import settings

from .state import State

logger = logging.getLogger(__name__)


class FindMarkerCrossMethod(State):
    def run(self):

        flight_utils.stop(self.vehicle)

        logger.info('Finding da marker %s', self.uuid_to_find)

        location_on_axis_1 = self.locate_beacon_on_axis(
            self.current_target_angle)  # Locate the beacon on the first axis
        logger.debug('on axis1: %f, %f', location_on_axis_1.lat,
                     location_on_axis_1.lon)
        # Fly to the predicted location
        self.vehicle.simple_goto(location_on_axis_1)
        logger.debug('flying towards the center of axis1')
        time.sleep(16)

        # Fly towards the end of the second axis
        self.vehicle.simple_goto(
            nav_utils.calculate_target_point(
                self.vehicle, self.current_target_angle + 90
            ),
            groundspeed=settings.FLIGHT_SPEED
        )

        time.sleep(5)  # Wait until the drone gets to the end of the 2nd axis

        flight_utils.stop(self.vehicle)

        # This finds the final location of the beacon, using the second axis
        beacon_location = self.locate_beacon_on_axis(
            self.current_target_angle - 90)  # Locate the beacon on the second axis
        # Go to the final location
        self.vehicle.simple_goto(beacon_location)
        time.sleep(10)
        flight_utils.stop(self.vehicle)

        logger.info('located major %s', self.major)
        if self.major == '65312':  # A normal beacon, poiting to the next beacon on the route
            raise EnteredFlyAlongAngleState(
                self.current_target_angle +
                # THIS CONVERSION IS IMPORTANT AF, DO NOT FORGET, NEVER
                hex_utils.get_angle_from_minor(self.minor)
            )

        elif self.major == '0':  # A beacon on the side of the field, poiting the drone back on the route
            raise EnteredFlyAlongAngleState(
                # THIS CONVERSION IS IMPORTANT AF, DO NOT FORGET, NEVER
                hex_utils.get_angle_from_minor(self.minor)
            )

        elif self.major == '65535':  # Final beacon
            raise EnteredLandingState(beacon_location)

    def locate_beacon_on_axis(self, angle: int) -> LocationGlobalRelative:
        logger.debug('locating along angle %i', angle)
        end_point = nav_utils.calculate_target_point(self.vehicle, angle)
        self.vehicle.simple_goto(
            end_point, groundspeed=settings.FLIGHT_SPEED_DURING_SCAN)
        # 20 times in 1s intervals with speed of 0.5m/s:
        #   that will cover the distance of 10 meters - enough to find the beacon no matter where it is,
        #   since the receiver can pick it up from 5 meters max

        highest_average_RSSI = -10000
        final_lat = 0
        final_lon = 0

        # Clear the queue before doing anything, because it MIGHT be full of some garbage
        self.clear_bt_queue()

        for i in range(20):
            logger.debug('flying on axis: %i/20', i)
            starting_lat, starting_lon = nav_utils.get_location(self.vehicle)
            # The interval we wait for the bt receiver to pick up signals during flight
            time.sleep(1)
            current_rssi_sum = 0
            current_measures_count = 0

            try:
                while True:
                    # Get all the data that the BT receiver has collected
                    uuid, major, minor, rssi = self.bluetooth_data_queue.get(
                        False)
                    current_rssi_sum += int(rssi)
                    current_measures_count += 1
                    # logger.debug('Got something on bt queue')
            except queue.Empty:
                if current_measures_count != 0:  # If there were no measurements, we don't count that region
                    average_rssi_for_current_region = current_rssi_sum / current_measures_count

                    logger.debug('current average: %i, best average: %i',
                                 average_rssi_for_current_region, highest_average_RSSI)

                    if average_rssi_for_current_region > highest_average_RSSI:
                        final_lat = (starting_lat +
                                     self.vehicle.location._lat)/2
                        final_lon = (starting_lon +
                                     self.vehicle.location._lon)/2
                        highest_average_RSSI = average_rssi_for_current_region
                else:
                    logger.warn('Nothing in bt queue on %i scanned segment', i)
        end_point = LocationGlobalRelative(
            final_lat,
            final_lon,
            settings.FLIGHT_ALTITUDE
        )

        return end_point
        # self.vehicle.simple_goto(end_point)

    def get_data_from_exception(self, exception: EnteredFindMarkerState):
        self.current_target_angle = exception.current_target_angle
        self.uuid_to_find = exception.uuid
        self.major = exception.major
        self.minor = exception.minor
