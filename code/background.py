from states.state import State
from multiprocessing import Process
import real_bluetooth
import fake_bluetooth
import settings
from dronekit import Command, mavutil
from beacon_simulator import BeaconSimulator
import logging

logger = logging.getLogger(__name__)

def _debug_location_data_callback(self, name, msg):
    logger.debug(msg.lat, msg.lon)
    State.location_data_queue.put((msg.lat, msg.lon))


bt_process = Process(target=real_bluetooth.scan_bt,
                     args=(State.bluetooth_data_queue,))


if settings.SIMULATE_BEACON:
    logger.critical('Using simulated beacons')
    cmds = State.vehicle.commands
    cmds.download()
    cmds.wait_ready()
    
    beacons_to_simulate = []

    logger.debug('Placing simulated beacons on:')
    for index, command in enumerate(cmds):
        logger.debug(command.x, command.y)
        beacons_to_simulate.append(
            BeaconSimulator(command.x, command.y, 'beacon_' + str(index))
        ) 

    logger.info('loaded', len(beacons_to_simulate), 'beacons to simulate!')


    bt_process = Process(target=fake_bluetooth.scan_bt, args=(
        State.bluetooth_data_queue, State.location_data_queue, beacons_to_simulate))

    State.vehicle.add_attribute_listener(
        'location.global_frame', _debug_location_data_callback)
else:
    logger.critical('Using real beacons')

def start_background_processes():
    bt_process.start()


def end_background_processes():
    bt_process.terminate()
