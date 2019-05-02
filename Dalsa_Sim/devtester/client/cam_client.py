# Dalsa_Sim/dalsa_hint_server/hint_server_client.py
"""
This is a straight copy of hint_client_main
"""
import logging
from client import Client
from log.log import file_handler

cam_client_log = logging.getLogger('devtester.client.cam_client')
cam_client_log.setLevel(logging.DEBUG)
cam_client_log.addHandler(file_handler)
cam_client_log.debug("Created Instance of Cam_Client_Log")


class CamServerClient(Client):

    def __init__(self, cam_hostname, cam_port, cam_client_name):
        # Inheriting dalsa_client and instantiating it to cam port with appropriate name
        super(CamServerClient, self).__init__(server_hostname=cam_hostname, client_port=cam_port, client_name=cam_client_name)


# Sample Code
# if module is being imported or run directly
if __name__ == "__main__":
    port = 5021
    client_name = "Dalsa Client"
    hostname = "localhost"
    cam_client = CamServerClient(hostname, port, client_name)
    print "Hostname is: " + cam_client.host_name
    cam_client.connect()
    response = cam_client.send('Hello')
    print "On: " + cam_client.client_name + "  Success Status: " + str(response)
    cam_client.close()
