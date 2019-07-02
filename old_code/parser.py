from pymavlink import mavutil
from multiprocessing import Process, Pipe
import time

def parser_thread(conn):
    # tworze obiekt slownikowy
    # if type(pars) is not dict:
    #   pars = dict()

    pars = dict()

    # utworz definicje slownika (anti fuckup)
    pars['lon'] = 0
    pars['lat'] = 0
    pars['wind_s'] = 0
    pars['wind_dir'] = 0
    pars['height'] = 0
    pars['speed'] = 0

    # ustanawiam polaczenie z PIXHAWKIEM
    the_connection = mavutil.mavlink_connection('udp:127.0.0.1:14551')

    # dopoki nie otrzymam potwierdzenia ze transmisja jest ustanowiona nie startuje z programem
    print("Czekam na heartbeat!")
    the_connection.wait_heartbeat()
    print("Otrzymalem heartbeat!")

    # glowna petla
    while True:
        time.sleep(0.01)
        # odbierz i sparsuj wiadomosc
        msg = the_connection.recv_match(blocking=False)
        # jest jest pusty odpusc
        if not msg:
            continue
        # pobierz typ wiadomosci
        msg_type = msg.get_type()
        # wyluskaj dane
        if msg_type is "GPS_RAW_INT":
            pars['lon'] = (float(msg.lon) * 10e-8)
            pars['lat'] = (float(msg.lat) * 10e-8)
            #conn.send(pars)
            print(pars)
            # conn.send( (pars['lon'],pars['lat']) )  # debug purposes
        if msg_type is "WIND":
            pars['wind_s'] = msg.speed
            pars['wind_dir'] = msg.direction
        if msg_type is "TERRAIN_REPORT":
            pars['height'] = msg.current_height
        if msg_type is "VFR_HUD":
            pars['speed'] = msg.groundspeed

if __name__ == '__main__':
    parser_thread(None)
