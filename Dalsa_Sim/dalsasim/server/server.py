# Dalsa_Sim/Dalsa_Sim/dalsa_server/dalsa_Server.py
# Created By : Benjamin Nelligan
# Date : November 20, 2018
# Last Modified : March 7, 2019 BEN
import socket
import json
import logging
from log.log import file_handler

# Creating Server Log
server_server_log = logging.getLogger('dalsasim.server.server.Server')
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
    # Send/Receive delimiters
    recv_delim = "\r"
    send_delim = recv_delim

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
        server_server_log.debug('Hostname: %s Creating Server Instance: [%s on Port: %s]', self.host_name,
                                self.server_name, self.server_port)
        pass

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
            server_server_log.debug('Created Active Server on Host: %s [Name: %s Port: %s]', str(hostname),
                                    self.server_name, str(self.server_port))

            try:
                # Trying to bind the socket to the port and hostname
                # Leaving hostname as '' allows it to accept any: "localhost", "127.0.0.1", or machine name
                # self.socket.bind((hostname, self.server_port))
                self.socket.bind(('', self.server_port))
                server_server_log.debug("Binded %s to Port %s", self.server_name, self.server_port)
                pass
                # Will return the object with the binned socket
            # Catching Errors
            except (socket.error, socket.timeout, socket.herror, socket.gaierror) as e:
                # Log
                server_server_log.error('Socket Error: %s', e)
                server_server_log.error('Socket cannot be binned...')
                pass

    # ================================= #
    # Date : February 21, 2019
    # Created By : Benjamin Nelligan
    # Description : will connect socket to a hostname and port
    # ================================= #

    def connect(self):
        # Create socket
        server_server_log.debug('Creating Socket on %s Port: %s', self.server_name, self.server_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Trying to connect socket to port and hostname
            self.socket.connect((self.host_name, self.server_port))
            server_server_log.debug(' %s is connected to %s on Port: %s', self.server_name, self.host_name,
                                    str(self.server_port))
            return self
            # Catch socket error
        except (socket.error, socket.timeout, socket.herror, socket.gaierror) as e:
            # Log socket error
            server_server_log.error('Socket error: %s on Port: %s', str(e), str(self.server_name),
                                    str(self.server_port))
            server_server_log.error('dalsa_server is most likely down :( %s', str(self.server_name))
            pass

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Will initialize the client to receive and listen to information.
    # Will try to unload data with json and return the data
    # ================================= #

    def receive(self, delimiter=recv_delim):
        result = []  # Create an array to contain result chars
        if self.socket:
            self.socket.listen(1)
            server_server_log.debug("Server %s is listening for connections...", self.server_name)
            server_server_log.debug('%s is Listening on Port: %s', self.server_name, self.server_port)
            # Waits here until a connection is accepted
            connection, client_address = self.socket.accept()
            # Adding client to list of known clients
            self.add_client(client_address)
            self.server_connection = connection
            server_server_log.debug("Server %s received a connection: %s", self.server_name, str(connection))
            # Begin Receive
            server_server_log.debug("Server receiving...")
            # Loop byte by byte and stop once delimiter received
            bite_size = 1
            char = ""
            flag = False
            while not flag:
                lil_byte = ""
                try:
                    # Try to receive 1 byte from socket buffer
                    lil_byte = connection.recv(bite_size)
                    # Check if this byte is the delimiter
                    if lil_byte == delimiter:
                        server_server_log.debug("WHOA BUDDY, thats the delimiter")
                        flag = True
                        break
                except socket.timeout as e:
                    server_server_log.error("Socket Timeout: %s", e)
                    pass
                server_server_log.debug("Type of lil_byte is: " + str(type(lil_byte)) + "and is " + str(lil_byte))
                # Add each byte to a char list named result
                if lil_byte is not "":
                    char = str(lil_byte)
                    result.append(char)
                    server_server_log.debug("Byte char: %s", char)
                else:
                    server_server_log.error("Byte is blank - so connection lost?")
                    server_server_log.error('Connection Lost: %s on: %s', self.server_name, client_address)
                    pass
            # Clean up the final result
            final_result = ''
            if result is not None:
                for x in result:
                    final_result += x
                server_server_log.info('On %s Package Received: %s', self.server_name, final_result)
                server_server_log.debug("Result string = " + final_result)
            return final_result

    def send_chunk(self, chunk):
        """
        Send a single chunk of data. Should match the method in client
        Must have a socket instantiated (which happens when we connect to hostname and port)
        TODO: Dont Repeat Yourself - lets move this to allow code reuse btw server and client
        :param chunk:
        :return:
        """
        if chunk is not None:
            package = str(chunk)
            # Check if last char in string is carriage return
            if package[-1:] != self.send_delim:
                package += self.send_delim  # TEMP should use var
            server_server_log.debug("Send_chunk, to send: " + package)
            try:
                if self.server_connection:
                    self.server_connection.sendall(package)
                    # dalsa_client_log.info('Sent: %s', package)
                    server_server_log.debug("Information Sent... Waiting for Response")
                    self.server_connection.close()
                    server_server_log.debug("Chunk sent OK")
                    return True
                else:
                    server_server_log.error("No Socket on %s", self.server_name)
                    server_server_log.error("No server socket")
                    return False
            except (socket.timeout, socket.error, socket.gaierror, socket.herror) as e:
                server_server_log.error('Information not Sent: %s', e)
                server_server_log.error('hint: its gonna be None')
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
            server_server_log.debug("%s is already known on %s", str(client_address), self.server_name)
            pass
        else:
            self.clients.append(client_address)
            server_server_log.info('Added %s to known list of Clients on %s', client_address, self.server_name)
            pass

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Will close to socket. terminating connection
    # ================================= #

    def close(self):
        # If there is a socket
        if self.socket:
            # Close socket
            server_server_log.debug("Closing Socket on %s Port %s", self.server_name, str(self.server_port))
            self.socket.close()
            self.server_connection = None
            server_server_log.debug('Closed Socket on Server: %s Port: %s', self.server_name, str(self.server_port))
            pass
        else:
            # Log
            server_server_log.error('Trying to close socket that doesnt exist on server: %s', self.server_name)
            pass

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
        server_server_log.debug("Getting Sockets on %s", self.server_name)
        return self.server_port

    def get_hostname(self):
        server_server_log.debug("Returning Hostname: %s", self.host_name)
        return self.host_name
