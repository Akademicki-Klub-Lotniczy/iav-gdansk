import time
from exceptions import EnteredLandingState

from dronekit import VehicleMode

from .state import State


class LandOnFinalMarkerState(State):
    def run(self):
        # TODO: ACTUALLY LAND ON THE BEACON, ON THE PLACE YOU'RE CURRENTLY ABOVE
        self.vehicle.mode = VehicleMode('LAND')
        time.sleep(10)
        # background.end_background_processes()
        self.vehicle.close()
        exit(0)

    def get_data_from_exception(self, exception: EnteredLandingState):
        self.beacon_location = exception.beacon_location


if __name__ == '__main__':
    a = FlyAlongAngleState(12)
    print(a.vehicle.mode)
