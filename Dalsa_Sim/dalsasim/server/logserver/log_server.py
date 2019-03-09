# Dalsa_Sim/dalsa_server/dalsa_log_server/log_server_main.py

from server.server import server
from server import log_server_name
from log.log import log_port
import logging
from log.log import file_handler


# Log Server (Class)
logserver_server_log = logging.getLogger('dalsasim.server.logserver.log_server')
logserver_server_log.setLevel(logging.DEBUG)
logserver_server_log.addHandler(file_handler)
# dalsa_log_server.addHandler(socket_handler)
# -------------------------------------


class LogServer(server):
    # Helping python understand what objects to expect
    log_port = log_port  # type: int
    log_server_name = log_server_name  # type: str

    def __init__(self):
        # inheriting dalsa_server and instantiating a new object with server name and port
        super(LogServer, self).__init__(server_port=log_port, server_name=log_server_name)


# If module is being imported
if __name__ == "__main__":
    log_server_main = LogServer()
    log_server_main.create_server()
