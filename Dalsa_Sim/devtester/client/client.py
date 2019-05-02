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
    # Send/Receive delimiters
    recv_delim = "\r"
    send_delim = recv_delim

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
        server_client_log.debug('Hostname: %s Created Client: %s on Port: %s', self.host_name, self.client_name,
                                self.client_port)

    # ================================= #
    # Date : February 15, 2019
    # Created By : Benjamin Nelligan
    # Description : Will serialize and send package to connected socket
    # ================================= #

    def send(self, package):
        final_result = False
        if self.client_socket:
            if package is not None:
                if self.client_connection:
                    result = self._send_chunk(package)
                    #print "DEBUG: send() - result of _send_chunk = " + str(result)
                    server_client_log.info("send() - result of _send_chunk = %s", str(result))
                    if result is not True:
                        print "ERROR: Unable to send package"
                        server_client_log.error("Unable to send package.")
                    else:
                        # If result is good, put into receive mode for response
                        server_client_log.info("Information Sent... Waiting for Response")
                        print "DEBUG: client.send() - Trying to receive a response package..."
                        server_client_log.info("send() - Trying to receive response package")
                        response = self._receive_response()
                        print "DEBUG: Response from Server = " + str(response)
                        server_client_log.debug("Response from Server: %s", str(response))
                        # TODO: What should we do with Response from server? probably parse success/fail?
                        final_result = str(response)
        return final_result

    def _send_chunk(self, chunk):
        """
        Send a single chunk of data
        :param chunk:
        :return:
        """
        if chunk is not None:
            package = str(chunk)
            # Check if last char in string is carriage return
            if package[-1:] != self.send_delim:
                package += self.send_delim  # TEMP should use var
            #print "DEBUG: send_chunk, to send: " + package
            server_client_log.debug("send_chunk: Chunk to send: %s", package)
            try:
                if self.client_socket:
                    self.client_socket.sendall(package)
                    server_client_log.debug("Information Sent %s... Waiting for Response", package)
                    #print "DEBUG: chunk sent OK"
                    server_client_log.debug("Chunk sent... OK")
                    return True
                else:
                    server_client_log.error("No Socket on %s", self.client_name)
                    print "ERROR: no client socket"
                    server_client_log.error("No client Socket")
                    return False
            except (socket.timeout, socket.error, socket.gaierror, socket.herror) as e:
                server_client_log.error('Information not Sent: %s', e)
                return False
        else:
            return False

    def _receive_response(self, delimiter=recv_delim):
        """
        Duplicates the receive method in server.
        TODO: DRY
        :return:
        """
        result = []  # Create an array to contain result chars
        if self.client_socket:
            try:
                #print "DEBUG: _receive_response: Client Listening for a Response from Server..."
                server_client_log.debug("_receive_response: Client Listening for a Response from Server...")
                # Loop byte by byte and stop once delimiter received
                bite_size = 1
                char = ""
                flag = False
                while not flag:
                    lil_byte = ""
                    try:
                        # Try to receive 1 byte from socket buffer
                        lil_byte = self.client_socket.recv(bite_size)
                        # Check if this byte is the delimiter
                        if lil_byte == delimiter:
                            #print "WHOA BUDDY, thats the delimiter"
                            flag = True
                            break
                    except socket.timeout as e:
                        server_client_log.error("Socket Timeout: %s", e)
                        pass
                    # This logger is VERY wordy, saved for troubleshooting.
                    #server_client_log.debug("Type of lil_byte is: " + str(type(lil_byte)) + "and is " + str(lil_byte))
                    # Add each byte to a char list named result
                    if lil_byte is not "":
                        char = str(lil_byte)
                        result.append(char)
                        server_client_log.debug("Byte char: %s", char)

                    else:
                        server_client_log.error("Byte is blank - so connection lost?")
                        server_client_log.error('Connection Lost: %s on: %s', self.client_name, self.host_name)
                # Clean up the final result
                final_result = ''
                if result is not None:
                    for x in result:
                        final_result += x
                    server_client_log.info('On %s Package Received: %s', self.client_name, final_result)
                    print "DEBUG: Result string = " + final_result
            except (socket.error, socket.timeout, socket.gaierror, socket.herror) as e:
                print "ERROR: Socket error when receiving. See logs."
                server_client_log.error("Socket Error When Receiving: %s", e)
                return False

            server_client_log.debug("Data: %s", final_result)
            if final_result is not "":
                return final_result
            else:
                print "Error receiving response from server"
                server_client_log.error("Data is None.... it's a problem")
                return False
        else:
            print "ERROR: client_socket not OK"
            server_client_log.error("_receive_response: self.client_socket not alive... ")
            return False

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
