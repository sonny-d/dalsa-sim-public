import sys
from server.camserver.cam_server import CamServer
from server.hintserver.hint_server import HintServer
from log.log import sim_main_log
import logging
import json


class Simulator(object):
    """
    The main class of the cam_sim. Creates the cam_server, hint_server, and cmd_processor.
    When cam_server or hint_server receive a request, they will callback to this Simulator to pass the command to the
    cmd_processor.
    """
    VERSION = '1.0.1'

    def __init__(self, cam_primary_port, cam_secondary_port, hint_port):
        """

        :param cam_primary_port:
        :param cam_secondary_port:
        :param hint_port:
        """

        print "Dalsa Simulator: Initializing a new simulator instance"

        # init the variables
        self.cam_port1 = cam_primary_port
        self.cam_port2 = cam_secondary_port
        self.hint_svr_port = hint_port

        # Start the cam_server
        self.cam_server = self._start_cam_server()

        # Start the hint_server
        self.hint_server = self._start_hint_server()

        # Start the logging server? Not for prototype2
        self.log_server = None

        # Ready to handle commands
        print "Simulator: Dalsa Cam Simulator is now ready to receive hints or camera commands.\n"

        # set content - barcode storage
        self.content = None

    def get_status(self):
        status = "Simulator is running:"
        # TODO: This error handling could be better.
        try:
            status += "\n\tCamServer running on ports: " + str(self.cam_server.get_sockets())
        except Exception:
            pass

        try:
            status += "\n\tHintServer running on ports: " + str(self.hint_server.get_sockets())
        except Exception:
            pass

        return status

    def stop(self):
        """This should stop this simulator gracefully, close ports first?"""
        self = None
        # This actually stops the whole program, must be a way to kill this class?
        # sys.exit(0)

    def start_listen(self):
        # Run the test loop
        self.cam_server.create_server()
        # Loops as long as server instance exists
        # TODO: Make this smarter with subproccesses, threading
        while self.cam_server:
            data = self.cam_server.receive()
            # Waits here until data is received...
            print "On: " + self.cam_server.server_name + '  Received data: ' + data
            # Process the received data
            CmdProcessor(self, data)
            # loops back around...

        # Disable second port for now, its just easier that way
        # data = self.cam_server.receive()
        # This is demo only, should store and handle data in future...

    def start_hint_listen(self):
        # Run the test loop
        self.hint_server.create_server()
        data = self.hint_server.receive()
        # Waits here until data is received...
        print "On: " + self.hint_server.server_name + '  Received data: ' + data
        # This is demo only, should store and handle data in future...
        # send to cmd processor, but its a hint, not a command
        HintProcessor(self, data)

    def stop_server(self):
        self.cam_server.close()
        #self.cam_server2.close()
        print "Dalsa Server shutdown"

    def cmd_callback(self, server, command):
        # do some processing, then
        response = CmdProcessor(self, command)
        print response
        server.return_response(response)
        pass

    def hint_callback(self, server, command):
        # do some processing,
        response = HintProcessor(self, command)
        # then
        server.return_response(response)
        pass

    def _start_cam_server(self):
        """
        Starts a cam server using the instance values of ports

        :return: Reference to cam server instance
        """
        try:

            # Start 1 cam server for each active port
            cam_svr = CamServer(self.cam_port1, "Cam Server 1")

            cam_svr.create_server()
            # data = cam_svr.receive()

            cam_svr2 = CamServer(self.cam_port2, "Cam Server 2")
            cam_svr2.create_server()

            # Waits here until data is received...
            #print "On: " + cam_svr.server_name + '  Received data: ' + data
            #cam_svr.close()

            # Disable second port for now, its just easier that way
            #data = cam_svr.receive()
            #cam_svr2.close()
            # TODO: return control to the cli while this is listening
            #print "Dalsa Simulator: a single loop is complete"
            print "Simulator: Dalsa server ports open: " + str(cam_svr.get_sockets()) + ", " + str(cam_svr2.get_sockets())
            return cam_svr
        except Exception:
            print "There was an error."
            return None

    def _start_hint_server(self):
        """
        Starts a hint server using the instance values of ports
        :return: A reference to the hint server instance
        """
        hint_svr = HintServer(self.hint_svr_port, "Hint Server 1")
        print "Simulator: Hint server ports open: " + str(hint_svr.get_sockets())
        return hint_svr

    def _start_log_server(self):
        """
        Specifications call for autologging on port 5022? More info needed, out of scope for protoype2.
        """
        pass

    def set_content(self, content):
        self.content = content
        return self.content

    # Begin camera commands
    def is_barcode_ready(self):
        if self.content is None:
            self.status = '---- FAILED ----'
            sim_main_log.error('Barcode Status : %s', self.status)
            return 0
        else:
            self.status = '---- READY ----'
            sim_main_log.info('Barcode Status : %s', self.status)
            print 'Barcode Ready'
            return 1

    def read_barcode(self):
        # not for ptoto 2. needs to be a function that when called is calling qr_gen and 'scans' a qr code live.
        sim_main_log.info('Reading Barcode : %s', self)
        if self.content == self.content:
            sim_main_log.info('Barcode Read')
            return '1.0000'
        else:
            sim_main_log.error('Barcode could not be found or read')
            return '0.0000'

    def get_barcode(self):
        if self.content is None:
            sim_main_log.error('---- Barcode Empty : %s', self.content)
            self.status = '---- ERROR ----'
            return self.status
        else:
            sim_main_log.info('----- getBarcode() : %s', self.content)
            return self.content


class CmdProcessor(object):
    def __init__(self, source, command):
        """A class for processing camera commands.

        :param source: Reference to the object that called this
        :param command: String of cam commdand to be processed
        """
        print "CmdProcessor: initialized"
        self.simulator_main = source
        self.command = command
        self.process_cmd(command)

    def process_cmd(self, command):
        """
        Parses the command and performs the appropriate action.

        :param command: command from driver, should match standard ASML command set
        :return: string response from cam sim, or empty string if command was invalid.
        """
        # format string --> EVAL getBarcode()
        print "Server: 0000 " + " received command " + command + " and will process..."

        # Standardize input for matching
        command = self._parse_command(command)
        print "DEBUG: Formatted command is: " + command

        # Match ASML camera command with correct method
        if command == "isbarcodeready()":
            print "Command processed was: " + "IsBarcodeReady()"
            response = self._is_barcode_ready()
        elif command == "readbarcode()":
            print "Command processed was: " + "ReadBarcode()"
            response = self._read_barcode()
        elif command == "getbarcode()":
            print "Command processed was: " + "GetBarcode()"
            response = self._get_barcode()
        elif command == "getversion()":
            print "Command processed was: " + "GetVersion()"
            response = self._get_version()
        else:
             print "Cam_Server: Invalid command received: " + command
             response = ""

        # Format a nice response
        response = self._format_response(command, response)

        print "DEBUG: SERVER.PROCESS_CMD:" + str(response)
        return response

    def _parse_command(self, command):
        """
        Cleans up received command for standardized matching.

        :param command: Command to parse
        :return: Parsed command
        """

        # First transform to lowercase
        cmd = command.lower()
        # Then split it up
        # TODO: Do we need to check any other conditions?
        cmd = cmd.split(" ")[1]  ##splits at space

        print "DEBUG: parser: parsed command is " + cmd
        return cmd

    def _format_response(self, command, response):
        """
        Formats the response to match the Dalsa camera spec.

        :param command: Command originally received
        :param response: Int or String Response value
        :return: String of response to print for user
        """
        if not isinstance(response, (int, long)):
            print "DEBUG: response is not a number"
            result = str(command + " , Result: %s" % response)
        else:
            print "DEBUG: response is a number"
            result = str(command + " , Result: " + '%.6f' % response)
            print "DEBUG: formatted response = " + result
        return result

    def _is_barcode_ready(self):
        sim_main_log.info('----- is barcode ready? : %s')
        print "SERVER: Is barcode ready?"
        return self.simulator_main.is_barcode_ready()

    def _read_barcode(self):
        sim_main_log.info('----- Scanning Barcode : %s')
        print "SERVER: scanning barcode"
        return self.simulator_main.read_barcode()

    def _get_barcode(self):
        sim_main_log.info('----- Retrieving Barcode : %s')
        print "SERVER: getting barcode?"
        return self.simulator_main.get_barcode()

    def _get_version(self):
        """
        Returns version of this camera firmware (simulator).

        :return: string of version information.
        """
        sim_main_log.info('----- Grabbing version : %s')
        return self.simulator_main.VERSION


class HintProcessor(object):
    def __init__(self, source, command):
        """
        A Class for processing hint commands

        :param source: Reference to the object that called this
        :param command: String of hint (JSON format) to be processed
        """
        print "HintProcessor: initialized"
        self.simulator_main = source
        self.command = command
        self.process_hint(command)

    def process_hint(self, command):
        """
        Processes a hint command

        :param command: String of hint command
        :return: String response
        """

        print "Server: 0000 " + " received command " + command + " and will process..."

        json_cmd = self.parse_json(command)
        print 'json hint is: ' + str(json_cmd)
        response = self.simulator_main.set_content(json_cmd["qr"])
        print "Hint processed was" + command

        print "SERVER.PROCESS_HINT: Response = " + str(response)

        return response

    def parse_json(self, json_string):
        """
        Accepts a JSON string and returns a dictionary object

        :param json_string: String of a JSON block
        :return: Dictionary object
        """
        #
        print "trying to parse str into dict..." + str(json_string)
        z = json.loads(json_string)
        return z
