# Dalsa_Sim/dalsa_log_server/log_client.py

import logging
from server.client import client
from server import log_client_name
from log.log import log_port
from log.log import file_handler


# Log Client (Class)
logserver_client_log = logging.getLogger('Dalsa_Sim.server.logserver.log_client_main')
logserver_client_log.setLevel(logging.DEBUG)
logserver_client_log.addHandler(file_handler)
# -------------------------------------


class LogClient(client):

    # Helping python understand what objects to expect
    log_client = log_client  # type: str
    log_port = log_port  # type: int

    def __init__(self):
        # Inheriting dalsa_client with attributes of log_client_name and log_port.
        # Will create a new subclass of dalsa_client named log_client_main
        super(LogClient, self).__init__(client_name=log_client_name, client_port=log_port)
        logserver_client_log.info("Created instance of Log Client on Port: %s", self.client_port)


# If module is being imported
if __name__ == '__main__':
    # Creating instance of the log client
    log_client = LogClient()

