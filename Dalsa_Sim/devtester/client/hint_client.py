# Dalsa_Sim/dalsa_hint_server/hint_server_client.py

from client import Client
# from . import cam_client_name
# from . import cam_port
from log.log import file_handler
import logging


# Hint Client (Class)
hintserver_client_log = logging.getLogger('dalsasim.server.hintserver.hint_client_main')
hintserver_client_log.setLevel(logging.DEBUG)
hintserver_client_log.addHandler(file_handler)
# hintserver_client_log.addHandler(socket_handler)
# -------------------------------------


class HintClient(Client):

    def __init__(self, cam_hostname, hint_port, hint_client_name):
        # Inheriting dalsa_client and instantiating it to hint port with appropriate name
        super(HintClient, self).__init__(server_hostname=cam_hostname, client_port=hint_port, client_name=hint_client_name)
        hintserver_client_log.info('Created Instance of %s on Port %s', self.client_name, self.client_port)


# Sample Code
# if module is being imported or run directly
if __name__ == "__main__":
    port = 5024
    client_name = "Hint Client"
    hostname = "localhost"
    hint_client = HintClient(hostname, port, client_name)
    print "Hostname is: " + hint_client.host_name
    hintserver_client_log.debug("Hostname is: %s", hint_client.host_name)
    hint_client.connect()
    response = hint_client.send('Hello my name is brendino 20380y89h349f93n4f834nf930$')
    print "On: " + hint_client.client_name + "  Success Status: " + str(response)
    hint_client.close()