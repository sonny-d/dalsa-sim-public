# Dalsa_Sim/dalsa_cam_server/cam_server.py

import logging
from log.log import file_handler
from server import cam_port
from server import cam_server_name
from server.server import Server

# Cam Server (Class)
cam_server_log = logging.getLogger('dalsasim.server.camserver.cam_server')
cam_server_log.setLevel(logging.DEBUG)
cam_server_log.addHandler(file_handler)


class CamServer(Server):

    def __init__(self, server_port=cam_port, server_name=cam_server_name):
        super(CamServer, self).__init__(server_port=server_port, server_name=server_name)
        cam_server_log.info('Created Hint Server: %s on Port: %s', server_port, server_name)


# Sample Code
# if module is being imported or run directly
if __name__ == '__main__':
    cam_server = CamServer()
    cam_server.create_server()
    data = cam_server.receive()
    cam_server_log.debug("On: " + cam_server.server_name + '  Received data: ' + data)
    cam_server_log.debug("Client info: " + str(cam_server.clients))
    cam_server.close()
    pass
