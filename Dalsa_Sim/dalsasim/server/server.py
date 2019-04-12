# Dalsa_Sim/Dalsa_Sim/dalsa_server/dalsa_Server.py
# Created By : Benjamin Nelligan
# Date : November 20, 2018
# Last Modified : March 7, 2019 BEN
import socket
import json
import logging
from log.log import file_handler

# Creating Server Log
server_server_log = logging.getLogger('dalsasim.server.server')
server_server_log.setLevel(logging.DEBUG)
server_server_log.addHandler(file_handler)

# -------------------------------------
hostname = socket.gethostname()

# ================================= #
# Date : February 10, 2019
# Created By : Benjamin Nelligan
# Description : Will create a object of the dalsa_server, using init of dalsa_main_server.
# This class holds methods to connect, send, and receive information
# ================================= #


class Server(object):
    server_port = None  # type: int
    server_name = None  # type: str
    server_socket = None  # type: socket
    SUCCESS_MSG = "SUCCESS"
    FAIL_MSG = "FAILURE"

    def __init__(self, server_port, server_name, server_connection=None, server_socket=None):
        super(Server, self).__init__()
        self.server_port = server_port
        # This variable will be used to differentiate between servers
        self.server_name = server_name
        self.server_connection = server_connection
        # Creating array of client connections
        self.clients = []
        self.host_name = hostname
        self.socket = server_socket
        server_server_log.info('Hostname: %s Creating Server Instance: [%s on Port: %s]', self.host_name,
                               self.server_name, self.server_port)

        # ================================= #
        # Date : February 15, 2019
        # Created By : Benjamin Nelligan
        # Description : will create a server on the socket.
        # Will allow this class to produce both client and server.
        # ================================= #

    def create_server(self):
        # If there is not a socket created, create one and log the info
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_server_log.info('Created Active Server on Host: %s [Name: %s Port: %s]', str(hostname),
                                   self.server_name, str(self.server_port))

            try:
                # Trying to bind the socket to the port and hostname
                # Leaving hostname as '' allows it to accept any: "localhost", "127.0.0.1", or machine name
                # self.socket.bind((hostname, self.server_port))
                self.socket.bind(('', self.server_port))
                # Will return the object with the binned socket
            # Catching Errors
            except (socket.error, socket.timeout, socket.herror, socket.gaierror) as e:
                # Log
                server_server_log.error('Socket Error: %s', e)
                server_server_log.error('Socket cannot be binned...')

    # ================================= #
    # Date : February 21, 2019
    # Created By : Benjamin Nelligan
    # Description : will connect socket to a hostname and port
    # ================================= #

    def connect(self):
        # Create socket
        server_server_log.info('Creating Socket...')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Trying to connect socket to port and hostname
            self.socket.connect((self.host_name, self.server_port))
            server_server_log.info(' %s is connected to %s on Port: %s', self.server_name, self.host_name,
                                  str(self.server_port))
            return self
            # Catch socket error
        except (socket.error, socket.timeout, socket.herror, socket.gaierror) as e:
            # Log socket error
            server_server_log.error('Socket error: %s on Port: %s', str(e), str(self.server_name), str(self.server_port))
            server_server_log.error('dalsa_server is most likely down :(')

    # ================================= #
    # Date : NFebruary 15, 2019
    # Created By : Benjamin Nelligan
    # Description : Will serialize the package and send it.
    # Must have a socket instantiated (which happens when we connect to hostname and port)
    # ================================= #

    def send(self, package):
        if self.socket:
            if package is not None:
                # Try to serialize package
                # dalsa_server_log.info('Serializing Package: %s', package)
                length_package = len(package)
                # format length as 3 digit number, with leading zeros

                if self.socket:
                    try:
                        self.socket.send(str(length_package))
                        self.socket.send(package)
                        return True
                # Catching exceptions
                    except (socket.error, socket.timeout, socket.gaierror, socket.herror) as e:
                        server_server_log.error('Information not Serialized: %s Error: %s', package, e)
            else:
                server_server_log.error('Package provided to %s is None', self.server_name)
                server_server_log.error('Package not sent because there is nothing to send...')
            return False

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Will initialize the client to receive and listen to information.
    # Will try to unload data with json and return the data
    # ================================= #

    def receive(self):
        result = []  # Create an array to contain result chars
        if self.socket:
            self.socket.listen(1)
            print "DEBUG: Server listening for connections..."
            server_server_log.info('%s is Listening on Port: %s', self.server_name, self.server_port)
            # Waits here until a connection is accepted
            connection, client_address = self.socket.accept()

            self.add_client(client_address)
            self.server_connection = connection
            print "DEBUG: Server received a connection"

            # Begin Receive
            print "DEBUG: Server receiving..."
            #data_length = connection.recv(1024)
            # Expect 3 char header with the length of the data
            data_length = connection.recv(3)
            data_length = data_length.strip()
            if len(data_length) == 0:
                server_server_log.error('Received nothing from: %s on Port: %s', client_address, str(self.server_port))
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
                    server_server_log.debug("Data: %s", str(lil_byte))
                else:
                    print "ERROR: lil_byte is 0 - so connection lost?"
                    server_server_log.error('Connection Lost: %s on: %s', self.server_name, client_address)
                data_recv = data_recv + len(lil_byte)
            # Clean up the result
            final_result = ''
            if result is not None:
                for x in result:
                    final_result = final_result + x
                server_server_log.info('On %s Package Received: %s', self.server_name, final_result)
                print "DEBUG: Result string = " + final_result

                # Send a response back to client
                return_package = self.SUCCESS_MSG
                print "DEBUG: return package to send to client = " + return_package
                return_result = self._send_chunk(return_package)
                print "DEBUG: Response sent without error? " + str(return_result)

            return final_result

    def _send_chunk(self, chunk):
        """
        Send a single chunk of data. Should match the method in client
        TODO: Dont Repeat Yourself - lets move this to allow code reuse btw server and client
        :param chunk:
        :return:
        """
        package = chunk
        length_package = len(package)
        if package is not None:
            try:
                # Send header: 3 digit string that = length of main package string
                package_length = str(length_package).zfill(3)  # zfill adds zeros to front so string is 3 char total
                self.server_connection.send(package_length)
                # self.server_connection.send(str(length_package))
                server_server_log.info('Outgoing Package length: %s', length_package)
                # Sending the rest of the package
                try:
                    self.server_connection.sendall(package)
                    # dalsa_client_log.info('Sent: %s', package)
                    server_server_log.info("Information Sent... Waiting for Response")
                    return True
                except (socket.timeout, socket.error, socket.gaierror, socket.herror) as e:
                    server_server_log.error('Information not Sent: %s', e)
                    server_server_log.info('hint: its gonna be None')
                    return False
            except(socket.timeout, socket.error, socket.gaierror, socket.herror) as e:
                server_server_log.error('Socket Error Length of Package not Sent: %s', e)
                return False
        else:
            return False

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Will initialize the client to receive and listen to information.
    # Will try to unload data with json and return the data
    # ================================= #
    def add_client(self, client_address):
        if client_address in self.clients:
            pass
        else:
            self.clients.append(client_address)
            server_server_log.info('Added %s to known list of Clients on %s', client_address, self.server_name)

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Will close to socket. terminating connection
    # ================================= #

    def close(self):
        # If there is a socket
        if self.socket:
            # Close socket
            self.socket.close()
            self.server_connection = None
            # Log
            server_server_log.info('Closed Socket on Server: %s Port: %s', self.server_name, str(self.server_port))
        else:
            # Log
            server_server_log.error('Trying to close socket that doesnt exist on server: %s', self.server_name)

    # ================================= #
    # Date : February 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Will serialize data using json
    # ================================= #

    def decode(self, package):
        try:
            data = json.dumps(package)
            server_server_log.info("Decoded Package on %s", self.server_name)
            return data
        except (ValueError, TypeError) as e:
            server_server_log.error('Error: %s when Decoding Package: %s [Client: %s Port:%s]', e, package,
                                    self.server_name,
                                    str(self.server_port))
            server_server_log.error("Returning None")
            return None

    # ================================= #
    # Date : February 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Will encode data using json
    # ================================= #

    def encode(self, package):
        try:
            package = json.loads(package)
            server_server_log.info("Encoded Package on %s", self.server_name)
            return package
        except (ValueError, TypeError) as e:
            server_server_log.error('Error: %s when Encoding Package: %s [Client: %s Port:%s]', e, package,
                                    self.server_name,
                                    str(self.server_port))
            server_server_log.error("Returning None")
            return None

    def get_sockets(self):
        """
        Return active server socket port numbers.
        :return:
        """
        return self.server_port;