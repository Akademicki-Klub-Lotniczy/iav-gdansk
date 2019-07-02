import numpy as np
import random
import time

TREND_POLYNOMIAL_DATA = [0.07203093,  -1.19743153,
                         8.5113106,  -26.83310929, -65.60632184]
STD_POLYNOMIAL_DATA = [0.1585723,  -1.62866816,
                       5.98260543, -9.59278432, 9.74901499]

MEASURE_COUNT_POLYNOMIAL_DATA = [10.21428571, -112.15714286, 383.02857143]


class BeaconSimulator:
    def __init__(self, lat, lon, uuid='beacon', tx=-65, major='65535', minor='0'):
        self.uuid = uuid
        self.tx = tx
        self.major = major
        self.minor = minor
        self.lat = lat
        self.lon = lon

        self.trend_poly = np.poly1d(TREND_POLYNOMIAL_DATA)
        self.std_poly = np.poly1d(STD_POLYNOMIAL_DATA)
        self.measure_count_poly = np.poly1d(MEASURE_COUNT_POLYNOMIAL_DATA)

    def get_rssi_for(self, distance: float) -> int:
        return int(np.random.normal(
            self.trend_poly(distance),
            self.std_poly(distance)
        ))

    def will_tick_100_ms(self, distance: float) -> bool:
        '''
        Returns a random value determining if a beacon signal
        will be received.

        Should be invoked every 100ms.
        '''

        # Measurements took 120s, so 1200 s^(-1)
        if distance > 5:
            return False

        return (random.randrange(0, 101)/100) < (self.measure_count_poly(distance) / 1200)
        #


if __name__ == '__main__':

    distance = 2

    b = BeaconSimulator()
    

    for _ in range(1200):
        if b.will_tick_100_ms(distance):
            rssi = b.get_rssi_for(distance)
        time.sleep(0.1)
