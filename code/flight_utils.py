import logging
import time

from dronekit import VehicleMode

import settings

logger = logging.getLogger(__name__)


def arm(vehicle):
    logger.info("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        logger.debug(" Waiting for vehicle to initialise...")
        time.sleep(1)

    logger.critical("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        logger.info(" Waiting for arming...")
        time.sleep(1)


def set_speed(vehicle):
    # vehicle.airspeed = settings.FLIGHT_SPEED # Speed limit: 1 speeds #pdk
    vehicle.groundspeed = settings.FLIGHT_SPEED


def takeoff(vehicle, aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    logger.info("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        logger.info(" Altitude: %f",
                    vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            logger.info("Reached target altitude")
            break
        time.sleep(1)


def stop(vehicle, time_to_stop=5):
    vehicle.simple_goto(
        vehicle.location.global_relative_frame
    )
    time.sleep(time_to_stop)
