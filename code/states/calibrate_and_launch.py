from exceptions import EnteredFlyAlongAngleState

import flight_utils
import settings

from .state import State


class CalibrateAndLaunchState(State):
    def run(self):
        flight_utils.arm(self.vehicle)

        flight_utils.set_speed(self.vehicle)

        # Direction the vehicle was heading when started from the ground
        start_heading = self.vehicle.heading
        flight_utils.takeoff(self.vehicle, settings.FLIGHT_ALTITUDE)

        raise EnteredFlyAlongAngleState(start_heading)

    def get_data_from_exception(self, exception):
        pass
