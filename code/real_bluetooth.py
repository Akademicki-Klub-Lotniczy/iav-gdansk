import socket
import logging

logger = logging.getLogger(__name__)

UDP_IP = "127.0.0.1"
UDP_PORT = 7777

def scan_bt(bt_queue):
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(128) # buffer size is 128 bytes
        uuid, major, minor, rssi = data.decode("utf-8").split(',')


        bt_queue.put( (uuid, major, minor, rssi) )
        logger.debug("received bluetooth:", uuid, major, minor, rssi)

class DummyQueue:
    def put(self, value):
        print(value)

if __name__ == '__main__':
    scan_bt(DummyQueue())
