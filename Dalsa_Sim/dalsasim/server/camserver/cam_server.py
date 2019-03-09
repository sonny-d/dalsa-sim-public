# Dalsa_Sim/dalsa_cam_server/cam_server.py

from server import cam_port
from log.log import cam_server_log
from server import cam_server_name
from server.server import Server


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
    print "On: " + cam_server.server_name + '  Received data: ' + data
    print "Client info: " + str(cam_server.clients)
    cam_server.close()