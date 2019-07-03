import logging
from math import cos, radians, sin

from dronekit import LocationGlobalRelative, VehicleMode, connect
from geopy.distance import geodesic

import settings

logger = logging.getLogger(__name__)


def calculate_carthesian_coefficient(vehicle):
    lat = vehicle.location._lat
    lon = vehicle.location._lon

    lat2 = lat + 0.0001
    lon2 = lon + 0.0001

    latdiff = geodesic([lat, lon], [lat2, lon]).m
    londiff = geodesic([lat, lon], [lat, lon2]).m

    return latdiff/londiff


def calculate_target_point(vehicle, angle: int, multiplier=0.0001) -> LocationGlobalRelative:
    coefficient = calculate_carthesian_coefficient(vehicle)
    #angle = -angle
    x_dir = sin(radians(angle)) * multiplier * coefficient
    y_dir = cos(radians(angle)) * multiplier  # coefficient

    # print(type(angle))
    logger.debug('flying towards %i', angle)

    return LocationGlobalRelative(
        vehicle.location._lat + y_dir,
        vehicle.location._lon + x_dir,
        settings.FLIGHT_ALTITUDE
    )


def get_location(vehicle):
    return vehicle.location._lat, vehicle.location._lon
