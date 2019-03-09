# Dalsa_Sim/dalsa_hint_server/hint_server_client.py
"""
This is a straight copy of hint_client_main
"""

from client import Client
from . import cam_client_name
from . import cam_port


class CamServerClient(Client):

    def __init__(self, c_port=cam_port, cam_client_nam=cam_client_name):
        # Inheriting dalsa_client and instantiating it to cam port with appropriate name
        super(CamServerClient, self).__init__(client_port=c_port, client_name=cam_client_nam)


# Sample Code
# if module is being imported or run directly
if __name__ == "__main__":
    port = 5021
    client_name = "Dalsa Client"
    cam_client = CamServerClient(port, client_name)
    cam_client.connect()
    response = cam_client.send('Hello')
    print "On: " + cam_client.client_name + "  Success Status: " + str(response)
    cam_client.close()