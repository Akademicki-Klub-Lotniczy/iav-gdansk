# pylint: disable=C0103
"""
This is where you start the whole thing
"""
import logging
import logging.config
from exceptions import (EnteredFindMarkerState, EnteredFlyAlongAngleState,
                        EnteredLandingState)

import background
import settings
from states.calibrate_and_launch import CalibrateAndLaunchState
from states.find_marker_cross_method import FindMarkerCrossMethod
from states.fly_along_angle import FlyAlongAngleState
from states.land_on_final_marker import LandOnFinalMarkerState

if __name__ == '__main__':
    background.start_background_processes()

    logging.config.dictConfig(settings.LOGGING)

    calibrate_and_launch_state = CalibrateAndLaunchState()
    fly_along_angle_state = FlyAlongAngleState()
    find_marker_cross_method = FindMarkerCrossMethod()
    land_on_final_marker_state = LandOnFinalMarkerState()

    current_state = calibrate_and_launch_state

    while True:
        try:
            current_state.run()

        except EnteredFlyAlongAngleState as ex:
            fly_along_angle_state.get_data_from_exception(ex)
            current_state = fly_along_angle_state

        except EnteredFindMarkerState as ex:
            find_marker_cross_method.get_data_from_exception(ex)
            current_state = find_marker_cross_method

        except EnteredLandingState as ex:
            land_on_final_marker_state.get_data_from_exception(ex)
            current_state = land_on_final_marker_state
