"""
This may duplicate simulatior.py.
"""
# Dalsa_Sim/CamSim/camsim.py
import json
import socket

from server import hostname
from camsim.barcode.barcode import Barcode


class camsim(object):

    socket_one = None  # type: socket
    socket_two = None  # type: socket
    barcode = None  # type: Barcode

    def __int__(self, camsim_port, barcode):
        self.socket_one = None
        self.socket_two = None
        self.port = camsim_port
        self.hostname = hostname
        self.barcode = barcode
        self.status = '---- NOT SET ----'

    def create_sockets(self):
        if self.socket_one is None:
            self.socket_one = socket.socket()
            # Add logging
        if self.socket_two is None:
            self.socket_two = socket.socket()
            # Add logging

    def close_sockets(self):
        self.socket_one.close()
        self.socket_two.close()
        self.socket_one = None
        self.socket_two = None

    def connect(self, port):
        if self.socket_one:
            self.socket_one.connect
        if self.socket_two:
            self.socket_two.connect

    def send(self):
        try:
            data = self.barcode
            serialized_data = json.dumps(data)
            self.socket_one.send(serialized_data)
        except (ValueError, TypeError) as e:
            print e
