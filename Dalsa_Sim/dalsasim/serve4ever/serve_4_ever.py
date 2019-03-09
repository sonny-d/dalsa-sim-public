# Dalsa_Sim/dalsa_server/dalsa_server_4_ever/serve_4_ever.py

import socket
from server import serve4ever_port
from server import serve4ever_server_name
from log import serve4ever_log
from server.server import Server


class Serve4Ever(Server):

    # overriding the initialization and creating inheritance
    def __init__(self, server_port=serve4ever_port, server_name=serve4ever_server_name):
        super(Serve4Ever, self).__init__(server_port=server_port, server_name=server_name)
        serve4ever_log.info('%s is ready to start serving the boys', serve4ever_server_name)

    # ================================= #
    # Date : February 16, 2019
    # Created By : Benjamin Nelligan
    # Description : Will initialize the server to wait and listen for a command to come in
    # ================================= #
    def serve(self):
        if self.socket:
            self.create_server()
            self.socket.listen(1)
            while True:
                connection, client_address = self.socket.accept()
                try:
                    serve4ever_log.info('On %s Connected by: %s', self.server_name, connection)
                    data = self.socket.recv(1024)
                    if data:
                        serve4ever_log.info('Data Received from: %s on Port: %s', connection, self.server_port)
                        return data
                    else:
                        serve4ever_log.info('Data received... but its nothing From: %s', client_address)
                        break
                except socket.error as e:
                    serve4ever_log.error('Socket Error: %s', e)
            self.close()


# When class is called, it will create a server and start serving forever
if __name__ == "__main__":
    server = Serve4Ever()
    server.create_server()
    data = server.serve()
    print(data)
