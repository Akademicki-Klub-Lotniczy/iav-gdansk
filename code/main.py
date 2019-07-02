from states.state import State
from states.calibrate_and_launch import CalibrateAndLaunchState
from states.fly_along_angle import FlyAlongAngleState
from states.find_marker_cross_method import FindMarkerCrossMethod
from states.land_on_final_marker import LandOnFinalMarkerState


from exceptions import \
    EnteredFindMarkerState, \
    EnteredFlyAlongAngleState, \
    EnteredLandingState

import logging
import logging.config
import settings

import background

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
    
    except EnteredFlyAlongAngleState as e:
        fly_along_angle_state.get_data_from_exception(e)
        current_state = fly_along_angle_state
        
    except EnteredFindMarkerState as e:
        find_marker_cross_method.get_data_from_exception(e)
        current_state = find_marker_cross_method

    except EnteredLandingState as e:
        land_on_final_marker_state.get_data_from_exception(e)
        current_state = land_on_final_marker_state
