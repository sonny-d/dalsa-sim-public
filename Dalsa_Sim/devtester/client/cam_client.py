# Dalsa_Sim/dalsa_hint_server/hint_server_client.py
"""
This is a straight copy of hint_client_main
"""

from client import Client
# from . import cam_client_name
# from . import cam_port


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
