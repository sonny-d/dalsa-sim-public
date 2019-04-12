# Dalsa_Sim/dalsa_server/dalsa_main_server.py

import socket
import json
import logging
from log.log import file_handler


# Creating Log For the class
server_client_log = logging.getLogger('dalsasim.server.client')
server_client_log.setLevel(logging.DEBUG)
server_client_log.addHandler(file_handler)

# -------------------------------------
hostname = socket.gethostname()


# =====================================
# Created By : Benjamin Nelligan
# Date : February 5, 2018
# Description : Will create an object of the dalsa_client with attributes of client_name, client_port, host_name
# and socket.
# Usage : mainly as a structure to create subclasses for our other clients. Holds methods to connect, send, recieve,
# and close which will be inherited by the sub classes. This will allow us to have a basic structure of client and be
# able to override methods depending on each subclass needs
# Subclassed By : log_client_main, hint_client_main, primary_client_main
# =====================================


class Client(object):
    # Hinting python what objects to expect
    client_socket = None  # type: socket
    client_name = None  # type: str
    client_port = None  # type: int
    SUCCESS_MSG = "SUCCESS"  # TODO: constants should be defined at module level
    FAIL_MSG = "FAILURE"

    # ================================= #
    # Date : February 1, 2019
    # Created By : Benjamin Nelligan
    # Description : Will instantiate an instance of the client. Will super the client, itself
    # Must be connected to server
    # ================================= #

    def __init__(self, server_hostname, client_name, client_port, client_connection=None, client_socket=None):
        # Calling super to create inheritance smoother
        super(Client, self).__init__()
        self.client_port = client_port
        # This variable will be used to differentiate between clients
        self.client_name = client_name

        # Set hostname of the server to connect to
        self.host_name = server_hostname
        self.client_connection = client_connection
        # Creating a socket with None. Will prevent from sending without connecting
        #  Creating a actual socket when calling .connect()
        self.client_socket = client_socket
        server_client_log.info('Hostname: %s Created Client: %s on Port: %s', self.host_name, self.client_name,
                               self.client_port)

    # ================================= #
    # Date : February 15, 2019
    # Created By : Benjamin Nelligan
    # Description : Will serialize and send package to connected socket
    # ================================= #

    def send(self, package):

        # Creating final result variable
        final_result = ''
        # If there is a socket
        final_result = False
        if self.client_socket:
            # Grabbing length of package
            length_package = len(package)
            if package is not None:
                if self.client_connection:
                    if length_package != 0:
                        result = self._send_chunk(package)

                        print "DEBUG: send() - result of _send_chunk = " + str(result)
                        if result is not True:
                            print "ERROR: Unable to send package"
                            server_client_log.error("Unable to send package.")
                        else:
                            server_client_log.info("Information Sent... Waiting for Response")
                            print "DEBUG: Trying to receive a response package..."

                            response = self._receive_response()
                            print "DEBUG: Response from Server = " + str(response)

                            if response == self.SUCCESS_MSG:
                                final_result = True
        return final_result

    def _send_chunk(self, chunk):
        """
        Send a single chunk of data
        :param chunk:
        :return:
        """
        package = chunk
        length_package = len(package)
        if package is not None:
            try:
                # Send header: 3 digit string that = length of main package string
                package_length = str(length_package).zfill(3)  # zfill adds zeros to front so string is 3 char total
                print "DEBUG: package to send = " + package + "  Length = " + str(package_length)
                self.client_socket.send(package_length)
                # self.client_socket.send(str(length_package))
                server_client_log.info('Outgoing Package length: %s', length_package)
                # Sending the rest of the package
                try:
                    self.client_socket.sendall(package)
                    server_client_log.info("Information Sent... Waiting for Response")
                    # dalsa_client_log.info('Sent: %s', package)
                    return True
                except (socket.timeout, socket.error, socket.gaierror, socket.herror) as e:
                    server_client_log.error('Information not Sent: %s', e)
                    server_client_log.info('hint: its gonna be None')
                    return False
            except(socket.timeout, socket.error, socket.gaierror, socket.herror) as e:
                server_client_log.error('Socket Error Length of Package not Sent: %s', e)
                return False
        else:
            return False

    def _receive_response(self):
        """
        Duplicates the receive method in server.
        TODO: DRY
        :return:
        """
        result = []  # Create an array to contain result chars
        if self.client_socket:
            try:
                print "DEBUG: Client Listening for a Response from Server..."
                connection = self.client_socket

                # Begin Receive
                # Expect 3 char header with the length of the data
                data_length = connection.recv(3)
                #print "DEBUG: data_length = " + str(data_length)
                data_length = data_length.strip()
                if len(data_length) == 0:
                    server_client_log.error('Received nothing in response')
                data_recv = 1
                # TODO: Add error handling for if first 3 chars are not numbers... ie base10 error
                # Receive the specified number of characters
                data_length = int(data_length)
                while data_recv <= data_length:
                    # May be better to receive 2 + bytes at a type according to docs...
                    lil_byte = connection.recv(1)
                    # Append the byte to the result string
                    # TODO: Test this error handling logic
                    if lil_byte != 0:
                        result.append(str(lil_byte))
                        server_client_log.debug("Data: %s", str(lil_byte))
                    else:
                        print "ERROR: lil_byte is 0 - so connection lost?"
                        server_client_log.error('Connection Lost')
                    data_recv = data_recv + len(lil_byte)
                # Clean up the result
                final_result = ''
                if result is not None:
                    for x in result:
                        final_result = final_result + x
                    server_client_log.info('On %s Result from Server Received: %s', self.client_name, final_result)
                    #print "DEBUG: Result string = " + final_result

                    return final_result
            except (socket.error, socket.timeout, socket.gaierror, socket.herror) as e:
                server_client_log.error("Socket Error When Receiving: %s", e)
        else:
            return False

    # ================================= #
    # Date : February 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Will initialize the client to receive and listen to information.
    # Will try to unload data with json and return the data
    # ================================= #

    def receive(self):
        result = []
        if self.client_socket:
            server_client_log.info('%s is Listening on Port: %s', self.client_name, self.client_port)
            # Accepting new Connection
            # The first is the length of the data
            data_length = self.client_socket.recv(1024)
            data_length = data_length.strip()
            if len(data_length) == 0:
                server_client_log.error('Received nothing from: %s on Port: %s', self.client_connection,
                                        str(self.client_port))
            data_recv = 1
            data_length = data_length.strip()
            data_length = len(data_length)
            while data_recv < data_length:
                data = self.client_socket.recv(data_recv)
                if data != 0:
                    result.append(str(data))
                else:
                    server_client_log.error('Connection Lost: %s on: %s', self.client_name, self.client_connection)
                    self.client_connection = None
                data_recv = data_recv + len(str(data))
            server_client_log.info('On %s Package Received: %s', self.client_name, result)
            final_result = ''
            if result is not None:
                for x in result:
                    final_result = final_result + x
            server_client_log.info('On %s Package Received: %s', self.client_name, final_result)
            return final_result

    # ================================= #
    # Date : February 21, 2019
    # Created By : Benjamin Nelligan
    # Description : Will connect socket to hostname and port
    # ================================= #

    def connect(self):
        # Create socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_client_log.info('Socket Created on [Client: %s]', self.client_name)
        try:
            # Try to connect
            self.client_socket.connect((self.host_name, self.client_port))
            # Creating boolean for connection
            self.client_connection = True
            # Logging
            server_client_log.info('On %s, Connected [Client %s on Port: %s]', self.client_name, self.host_name,
                                   str(self.client_port))
            pass
        # Catch socket error
        except (socket.error, socket.herror, socket.gaierror, socket.timeout) as e:
            # Log socket error
            server_client_log.error('Socket error: %s [Client: %s on Port: %s]', e, self.client_name,
                                    str(self.client_port))
            server_client_log.error('dalsa_server is most likely down :(')
            self.client_connection = False
            pass

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Will close to socket. terminating connection
    # ================================= #

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_connection = None
            server_client_log.info('Closed [Client: %s] on Port: %s', self.client_name, str(self.client_port))
            return True
        else:
            server_client_log.error('Trying to close socket that doesnt exist on [Client: %s]', self.client_name)
            return False

    # ================================= #
    # Date : February 21, 2019
    # Created By : Benjamin Nelligan
    # Description : Will set Socket to listen
    # ================================= #

    def listen(self, number_of_request):
        if self.client_socket:
            self.client_socket.listen(number_of_request)
            pass
        else:
            server_client_log.error('No socket to listen on: [%s Port: %s]', self.client_name, str(self.client_port))
            pass

    # ================================= #
    # Date : February 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Will encode data using json
    # ================================= #
    def encode(self, package):
        try:
            package = json.loads(package)
            server_client_log.info('Package Encoded on %s', self.client_name)
            return package
        except (ValueError, TypeError) as e:
            server_client_log.error('Error: %s when Encoding Package: %s [Client: %s Port:%s]', e, package,
                                    self.client_name, str(self.client_name))
            server_client_log.error("Returning None")
            return None

    # ================================= #
    # Date : February 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Will decode data using json
    # ================================= #

    def decode(self, package):
        try:
            result = json.dumps(package)
            server_client_log.info('Package Decoding on: %s', self.client_name)
            return result
        except (ValueError, TypeError) as e:
            server_client_log.error('Error: %s when Encoding Package: %s [Client: %s Port:%s]', e, package,
                                    self.client_name, str(self.client_name))
            server_client_log.error("Returning None")
            return None



