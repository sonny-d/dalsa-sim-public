# Dalsa_Sim/dalsa_hint_server/hint_server.py

from server import hint_port
from server import hint_server_name
from server.server import Server
from log.log import file_handler
import logging


# Hint Server (Package)
hintserver_server_log = logging.getLogger('dalsasim.server.hint_server')
hintserver_server_log.setLevel(logging.DEBUG)
hintserver_server_log.addHandler(file_handler)


class HintServer(Server):

    def __init__(self, server_port=hint_port, server_name=hint_server_name):
        super(HintServer, self).__init__(server_port=server_port, server_name=server_name)
        hintserver_server_log.info('Created Hint Server: %s on Port: %s', server_port, server_port)


# Sample Code
# if module is being imported or run directly
if __name__ == '__main__':
    hint_server = HintServer()
    hint_server.create_server()
    data = hint_server.receive()
    hint_server.server_connection.send(data)
    print "On: " + hint_server.server_name + '  Received data: ' + data
    print "Client info: " + str(hint_server.clients)
    hint_server.close()