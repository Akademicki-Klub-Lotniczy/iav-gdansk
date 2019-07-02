import logging

logger = logging.getLogger(__name__)


class EnteredFindMarkerState(Exception):
    def __init__(self, current_target_angle: int, uuid: str, major: str, minor: str):
        logger.info('entering locating marker state')
        super().__init__()
        self.current_target_angle = current_target_angle
        self.uuid = uuid
        self.major = major
        self.minor = minor


class EnteredFlyAlongAngleState(Exception):
    def __init__(self, new_target_angle: int):
        logger.info('entering flying along angle state')
        
        super().__init__()
        self.new_target_angle = new_target_angle


class EnteredLandingState(Exception):
    def __init__(self, beacon_location):
        logger.info('entering landing state')
        super().__init__()
        self.beacon_location = beacon_location

if __name__ == '__main__':
    try:
        raise EnteredFindMarkerState(12)
    except EnteredFindMarkerState as e:
        print(e.target_angle)