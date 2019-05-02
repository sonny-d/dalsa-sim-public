import logging
import socket
import json
from server.camserver.cam_server import CamServer
from server.hintserver.hint_server import HintServer
from log.log import file_handler

# Logging for File
# ===================
sim_main_log = logging.getLogger('dalsasim.camsim.simulator_main.Simulator')
sim_main_log.setLevel(logging.DEBUG)
sim_main_log.addHandler(file_handler)
sim_main_log.debug("Created Instance of Simulator Main Log")
cmd_proc_log = logging.getLogger('dalsasim.camsim.simulator_main.CmdProcessor')  # type: logging
cmd_proc_log.setLevel(logging.DEBUG)
cmd_proc_log.addHandler(file_handler)
cmd_proc_log.debug("Created Instance of CMD Process Log")
hint_proc_log = logging.getLogger('dalsasim.camsim.simulator_main.HintProcessor')  # type: logging
hint_proc_log.setLevel(logging.DEBUG)
hint_proc_log.addHandler(file_handler)
hint_proc_log.debug("Created Instance of Hint Process Log")


# ===================


class Simulator(object):
    """
    The main class of the cam_sim. Creates the cam_server, hint_server, and cmd_processor.
    When cam_server or hint_server receive a request, they will callback to this Simulator to pass the command to the
    cmd_processor.
    """
    VERSION = 1801
    ASML_VERSION = 1

    def __init__(self, cam_primary_port, cam_secondary_port, hint_port):
        """

        :param cam_primary_port:
        :param cam_secondary_port:
        :param hint_port:
        """

        sim_main_log.debug("Dalsa Simulator: Initializing a new simulator instance")

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
        sim_main_log.debug("Simulator: Dalsa Cam Simulator is now ready to receive hints or camera commands.")

        # set test id
        self.test_id = None

        # set content - storage for a "not-yet-scanned" barcode
        self.content = None

        # set barcode - storage for a "scanned" barcode
        self.barcode = None

        # Init good/bad weather conditions - to be set via hints
        self.weather_cond = "good"
        self.err_no_response = False
        self.err_communication = False

    def get_status(self):
        status = "Simulator is running:"
        # TODO: This error handling could be better.
        try:
            status += "\n\tCamServer running on ports: " + str(self.cam_server.get_sockets())
        except socket.error as e:
            sim_main_log.error("Socket Error")
            pass

        try:
            status += "\n\tHintServer running on ports: " + str(self.hint_server.get_sockets())
        except socket.error as e:
            sim_main_log.error("Socket Error")
            pass

        return status

    def get_hostname(self):
        host = self.cam_server.get_hostname()
        return host

    def stop(self):
        """This should stop this simulator gracefully, close ports first?"""
        self = None
        # This actually stops the whole program, must be a way to kill this class?
        # sys.exit(0)

    def start_listen(self):
        # Run the test loop )
        # Loops as long as server instance exists
        # TODO: Make this smarter with subproccesses, threading
        while self.cam_server:
            data = self.cam_server.receive()
            # Waits here until data is received...
            sim_main_log.debug("On: " + self.cam_server.server_name + '  Received data: ' + str(data))
            sim_main_log.debug("sending data to cmdprocessor...")
            # Process the received data, and send a response
            CmdProcessor(self, data)
            # loops back around...

        print "DEBUG: Cam Server not running. Re-start the Simulator."
        # Disable second port for now, its just easier that way
        # data = self.cam_server.receive()
        # This is demo only, should store and handle data in future...

    def send_cam_resp(self, response):
        """
        Send a response through the primary cam server.

        :param response: String response
        :return: Boolean status
        """
        if response:
            try:
                self.cam_server.send_chunk(response)
                return True

            except socket.error as e:
                sim_main_log.error("Exception in send_cam_resp(): " + str(e))
                return False
        else:
            return False

    def send_hint_resp(self, response):
        """
        Send a response through the hint server.

        :param response: String response
        :return: Boolean status
        """
        if response:
            try:
                self.hint_server.send_chunk(response)
                return True
            except socket.error as e:
                sim_main_log.error("Socket Error: %s", e)
                return False
        else:
            return False

    def start_hint_listen(self):
        # Run the test loop
        self.hint_server.create_server()
        data = self.hint_server.receive()
        # Waits here until data is received...
        sim_main_log.debug("On: " + self.hint_server.server_name + '  Received data: ' + data)
        # This is demo only, should store and handle data in future...
        # send to cmd processor, but its a hint, not a command
        if data is not None:
            sim_main_log.debug("Creating Instance of Hint Processor w/ data: %s", str(data))
            HintProcessor(self, data)
        else:
            sim_main_log.error("Data for Hint Processor is None")

    def stop_server(self):
        self.cam_server.close()
        self.cam_server = None
        print "Dalsa Server shutdown"
        # self.cam_server2.close()
        sim_main_log.debug("Dalsa Server shutdown")
        pass

    def cmd_callback(self, server, command):
        # do some processing, then
        response = CmdProcessor(self, command)
        sim_main_log.debug("Response: %s", response)
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
            sim_main_log.debug("Creating Cam Server1 on Port %s", str(self.cam_port1))
            cam_svr = CamServer(self.cam_port1, "Cam Server 1")
            sim_main_log.debug("Binding CamServer1 to Port %s", str(self.cam_port1))
            cam_svr.create_server()
            # data = cam_svr.receive()
            sim_main_log.debug("Creating Cam Server2 on Port %s", str(self.cam_port2))
            cam_svr2 = CamServer(self.cam_port2, "Cam Server 2")
            sim_main_log.debug("Binding CamServer2 to Port %s", str(self.cam_port2))
            cam_svr2.create_server()
            # TODO: return control to the cli while this is listening
            sim_main_log.debug("Simulator: Dalsa server ports open: " + str(cam_svr.get_sockets()) + ", " +
                               str(cam_svr2.get_sockets()))
            return cam_svr
        except socket.error as e:
            sim_main_log.error("There was an error: %s", e)
            return None

    def _start_hint_server(self):
        """
        Starts a hint server using the instance values of ports
        :return: A reference to the hint server instance
        """
        hint_svr = HintServer(self.hint_svr_port, "Hint Server 1")
        sim_main_log.debug("Simulator: Hint server ports open: " + str(hint_svr.get_sockets()))
        return hint_svr

    def _start_log_server(self):
        """
        Specifications call for autologging on port 5022? More info needed, out of scope for protoype2.
        """
        pass

    def set_content(self, content):
        """
        Content is storage for a hinted QR value. Must be "scanned" before it is stored as barcode.
        :param content:
        :return:
        """
        sim_main_log.debug("Setting Content: %s", str(content))
        self.content = content
        pass

    def get_content(self):
        if self.content:
            sim_main_log.debug("Getting Content: %s", str(self.content))
            return str(self.content)
        else:
            sim_main_log.error("No Content, can't get...")
            return None

    def set_barcode(self, barcode):
        """
        Barcode is storage for a "scanned" QR value that is ready to return.
        :param barcode:
        :return:
        """
        sim_main_log.debug("Setting Barcode %s", str(self.barcode))
        self.barcode = barcode
        pass

    def get_barcode(self):
        if self.barcode:
            sim_main_log.debug("Getting Barcode %s", str(self.barcode))
            return self.barcode
        else:
            sim_main_log.error("No Barcode, can't get...")
            return None

    def set_test_id(self, value):
        self.test_id = value

    def get_test_id(self):
        return self.test_id

    def set_weather_cond(self, value):
        """
        Overall weather condition. If good, errors ignored. Else, they are processed.
        :param value: String "good" or "bad"
        :return: None
        """
        # Strip any spaces
        v = str(value).strip().lower()
        # Standardize value
        #print "DEBUG: weather cond formatted is: " + v
        sim_main_log.debug("set_weather_cond: weather cond formatted is: %s" % v)
        # Input validation
        if v not in ["bad", "good"]:
            v = "good"
            print "Hint Received: weather condition set to default: " + v
            sim_main_log.warn("set_weather_cond: weather condition did not match expected values, set to default: %s" % v)
        else:
            print "Hint Received: weather condition set: " + v
            sim_main_log.debug("set_weather_cond: weather condition set to hint: %s" % v)
        # Return result
        sim_main_log.info("Testing hint processed: weather condition set: %s" % v)
        self.weather_cond = v

    def get_weather_cond(self):
        return self.weather_cond

    def set_err_no_response(self, value):
        # Strip any spaces
        v = str(value).strip().lower()
        try:
            #print "DEBUG: err resp? " + str(v)
            sim_main_log.debug("set_err_no_response: Formatted result, is err enabled? %s" % v)
            # Convert string to boolean
            r = (v == "true")
            #print "DEBUG: err resp? " + str(r)
            sim_main_log.debug("set_err_no_response: Boolean casted result, is err enabled? %s" % r)
            if r and self.get_weather_cond() == "bad":
                print "Testing hint processed: enabled No Response error (err_no_response)"
                sim_main_log.info("Testing hint processed: enabled No Response error (err_no_response)")
        except Exception as e:
            print "Error in set_err_no_response: %s" % e
            sim_main_log.error("Error in set_err_no_response: %s" % e)
            # defaults to False in case of formatting error
            r = False
        self.err_no_response = r

    def get_err_no_response(self):
        return self.err_no_response

    def set_err_communication(self, value):
        # Strip any spaces
        v = str(value).strip().lower()
        try:
            #print "DEBUG: err comm? " + str(v)
            sim_main_log.debug("set_err_communication: Formatted result, is err enabled? %s" % v)
            # Convert string to boolean
            r = (v == "true")
            #print "DEBUG: err comm? " + str(r)
            sim_main_log.debug("set_err_communication: Boolean casted result, is err enabled? %s" % r)
            if r and self.get_weather_cond() == "bad":
                print "Testing hint processed: enabled Communication Error (err_no_response)"
                sim_main_log.info("Testing hint processed: enabled Communication Error (err_no_response)")
        except Exception as e:
            print "Error in set_err_no_response: %s" % e
            sim_main_log.info("Error in set_err_no_response: %s" % e)
            r = False
        self.err_communication = r

    def get_err_communication(self):
        return self.err_communication


class CmdProcessor(object):

    def __init__(self, source, command):
        """A class for processing camera commands.

        :param source: Reference to the object that called this
        :param command: String of cam commdand to be processed
        """
        cmd_proc_log.debug("Creating Instance of Cmd Processor")
        self.simulator_main = source
        self.command = command
        # Flag to indicate if an intentional error was caused
        self.error = False
        # Process the command
        self.process_cmd(command)

    def process_cmd(self, command):
        """
        Parses the command and performs the appropriate action.

        :param command: command from driver, should match standard ASML command set
        :return: string response from cam sim, or empty string if command was invalid.
        """
        # format string --> EVAL getBarcode()
        cmd_proc_log.debug("Server: Received command " + command + " and will process...")

        # Standardize input for matching
        # TODO: What if formatting fails? Add error handling...
        parsed_command = self._parse_command(command)
        cmd_proc_log.debug(" Formatted command is: " + command)
        if parsed_command is None:
            cmd_proc_log.debug("Cam_Server: Invalid format for command received: " + command + str(parsed_command))
            parsed_command = command

        # Match ASML camera command with correct method
        if parsed_command == "isbarcodeready()":
            cmd_proc_log.info("Command received was: " + "IsBarcodeReady()")
            response = self._is_barcode_ready()
        elif parsed_command == "readbarcode()":
            cmd_proc_log.info("Command processed was: " + "ReadBarcode()")
            response = self._read_barcode()
        elif parsed_command == "getbarcode()":
            cmd_proc_log.info("Command processed was: " + "GetBarcode()")
            response = self._get_barcode()
        elif parsed_command == "getversion()":
            cmd_proc_log.info("Command processed was: " + "GetVersion()")
            response = self._get_version()
        elif parsed_command == "getasmlversion":
            cmd_proc_log.info("Command processed was: " + "GetASMLVersion")
            response = self._get_asml_version()
        else:
            cmd_proc_log.warn("Cam_Server: Invalid command received: " + command)
            cmd_proc_log.debug("Parsed: " + parsed_command)
            cmd_proc_log.debug("Command: " + command)
            cmd_proc_log.debug("Response = 0")
            response = 0

        if not self.error:
            # Format a nice response
            cmd_proc_log.debug("Formatting the response")
            response = self._format_response(parsed_command, response)

            cmd_proc_log.debug("SERVER.PROCESS_CMD: Response = " + str(response))

            # Send response back
            status = self.simulator_main.send_cam_resp(response)
            #print "Response success? " + str(status)
            cmd_proc_log.debug("Response success? " + str(status))
        else:
            response = 0


        # Not using response, currently...
        cmd_proc_log.debug("Returning response: %s", response)
        return response

    def _parse_command(self, command):
        """
        Cleans up received command for standardized matching.

        :param command: Command to parse
        :return: Parsed command OR None if command was invalid
        """

        # First transform to lowercase
        cmd_proc_log.debug("Forcing cmd to Lowercase")
        cmd = command.lower()
        cmd_proc_log.debug("New cmd: %s", cmd)
        # Then split it up
        # TODO: Do we need to check any other conditions? Verify behavior for case where eval is missing
        if cmd.startswith("eval"):
            cmd = cmd.split(" ")[1]  ##splits at space
        else:
            cmd = None
            cmd_proc_log.debug("Non-cannon Error: command must start with eval.")

            cmd_proc_log.debug("Parser: parsed command is " + str(cmd))
        return cmd

    def _format_response(self, command, response):
        """
        Formats the response to match the Dalsa camera spec.

        :param command: Command originally received
        :param response: Int or String Response value
        :return: String of response to print for user
        """
        if not isinstance(response, (int, long)):
            cmd_proc_log.debug("Response is not a number")
            result = str(command + " , Result: %s" % response)
        else:
            cmd_proc_log.debug("Response is a number")
            result = str(command + " , Result: " + '%.6f' % response)
            cmd_proc_log.debug("Returning formatted response = " + result)
        return result

    # Begin camera commands
    def _read_barcode(self):
        """
        Start reading sequence and decoding
        :return: 0, regardless of status
        """
        #print "SERVER: Reading barcode"

        # Local var for convenience
        sim = self.simulator_main

        cmd_proc_log.debug('Scanning Barcode')
        cmd_proc_log.debug("SERVER: scanning barcode")
        cmd_proc_log.debug('Reading Barcode : %s', self)

        # Try to get barcode to simulate "reading" it
        barcode = sim.get_content()

        # Test for bad weather errors
        self.check_err_communication()
        self.check_err_no_response()
        if self.error:
            print "SERVER: Intentional error encountered during ReadBarcode."
            sim_main_log.info('Intentional error encountered during ReadBarcode.')
            return 0

        if barcode:
            cmd_proc_log.debug('Barcode Read')
            sim.set_barcode(barcode)
        else:
            cmd_proc_log.debug('Barcode could not be found or read')
            sim.set_barcode(None)

        # Always returns 0
        cmd_proc_log.debug("Returning 0...")
        return 0

    def _is_barcode_ready(self):
        """
        Signal the decoding is complete and ready for GetBarcode() command
        :return: Status code, 0 or 1
        """
        cmd_proc_log.debug('----- is barcode ready?')
        #print "SERVER: Is barcode ready?"

        # Test for bad weather errors
        self.check_err_communication()
        self.check_err_no_response()
        if self.error:
            print "SERVER: Intentional error encountered during isBarcodeReady."
            sim_main_log.info('Intentional error encountered during isBarcodeReady.')
            return 0

        cmd_proc_log.debug("SERVER: Is barcode ready?")


        if self.simulator_main.get_barcode() is None:
            cmd_proc_log.info('Barcode not ready')
            return 0
        else:
            cmd_proc_log.info('Barcode is ready')
            return 1

    def _get_barcode(self):
        """
        Return barcode_id string
        :return: Status code, 0 or 1
        """
        cmd_proc_log.debug('Retrieving Barcode')
        cmd_proc_log.debug("SERVER: getting barcode?")

        # Test for bad weather errors
        self.check_err_communication()
        self.check_err_no_response()
        if self.error:
            print "SERVER: Intentional error encountered during GetBarcode."
            sim_main_log.info('Intentional error encountered during GetBarcode.')
            return 0

        barcode = self.simulator_main.get_barcode()
        if barcode is None:
            cmd_proc_log.info('---- getBarcode() : Barcode Empty')
            return 0
        else:
            cmd_proc_log.info('----- getBarcode() : %s', barcode)
            return barcode

    def _get_version(self):
        """
        Returns version of this camera firmware (simulated).

        :return: string of version information.
        """
        cmd_proc_log.debug('----- Grabbing version : %s', self.simulator_main.VERSION)
        # Test for bad weather errors
        self.check_err_communication()
        self.check_err_no_response()
        if self.error:
            print "SERVER: Intentional error encountered during getVersion."
            sim_main_log.info('Intentional error encountered during getVersion.')
            return 0

        return self.simulator_main.VERSION

    def _get_asml_version(self):
        """
        Returns version of the ASML solution file

        :return: string of version information.
        """
        cmd_proc_log.debug('----- Grabbing version : %s', self.simulator_main.ASML_VERSION)
        # Test for bad weather errors
        self.check_err_communication()
        self.check_err_no_response()
        if self.error:
            print "SERVER: Intentional error encountered during getASMLVersion."
            sim_main_log.info('Intentional error encountered during getASMLVersion.')
            return 0

        return self.simulator_main.ASML_VERSION

    # Begin error definitions
    def check_err_communication(self):
        # local var for convenience
        sim = self.simulator_main
        if sim.get_weather_cond() == "bad" and sim.get_err_communication() is True:
            #print "DEBUG: hinted error err_communication set, causing disconnect..."
            cmd_proc_log.error("Hinted error err_communication set, causing disconnect...")
            sim.stop_server()
            self.error = True
        else:
            #print "DEBUG: No err_communication error"
            cmd_proc_log.debug("No err_communication error")

    def check_err_no_response(self):
        # local var for convenience
        sim = self.simulator_main
        if sim.get_weather_cond() == "bad" and sim.get_err_no_response() is True:
            #print "DEBUG: hinted error err_no_response set, cancelling response..."
            cmd_proc_log.error("Hinted error err_no_response set, cancelling response...")
            # sim.stop_server()
            self.error = True
            pass
        else:
            #print "DEBUG: No err_no_response error"
            cmd_proc_log.debug("No err_no_response error")


class HintProcessor(object):
    def __init__(self, source, command):
        """
        A Class for processing hint commands

        :param source: Reference to the object that called this
        :param command: String of hint (JSON format) to be processed
        """
        hint_proc_log.debug("HintProcessor: initialized")
        self.simulator_main = source
        self.command = command
        self.process_hint(command)

    def process_hint(self, command):
        """
        Processes a hint command

        :param command: String of hint command
        :return: String response
        """

        hint_proc_log.debug("Server: 0000 " + " received command " + command + " and will process...")

        # Parse JSON into dict
        json_cmd = self.parse_json(command)

        hint_proc_log.debug('json hint is: ' + str(json_cmd))
        hint_proc_log.debug("Storing hint as potential barcode content in simulator")
        #print 'DEBUG: HintProcessor.process_hint: json hint is: ' + str(json_cmd)
        response = ""

        try:
            # Apply weather conditions
            for key, value in json_cmd.iteritems():
                if key == "qr":
                    # Store QR hint as "content" in Simulator
                    #print "Key is qr"
                    #print "Storing hint as potential barcode content in simulator"
                    self.simulator_main.set_content(value)
                    response = 1
                elif key == "test-id":
                    #print "Key is " + key
                    self.simulator_main.set_test_id(value)
                    response = 1
                elif key == "weather-cond":
                    #print "Key is " + key
                    self.simulator_main.set_weather_cond(value)
                    response = 1
                    pass
                elif key == "err-no-response":
                    #print "Key is " + key
                    self.simulator_main.set_err_no_response(value)
                    response = 1
                    pass
                elif key == "err-communication":
                    self.simulator_main.set_err_communication(value)
                    response = 1
                    #print "Key is " + key
                    pass
                else:
                    #print "Other: Key = " + key + " Value = " + value
                    pass
        except KeyError:
            hint_proc_log.debug('----- process_hint() : Error in hint JSON? ' + str(json_cmd))
            response = None
        hint_proc_log.debug("SERVER.PROCESS_HINT: Hint processed, Response = " + str(response))
        # respond with a status code
        if response:
            resp = 1
            # Send response back
            status = self.simulator_main.send_hint_resp(str(resp))
            hint_proc_log.debug("Response success? " + str(status))
        else:
            resp = 0
            status = self.simulator_main.send_hint_resp(str(resp))
            hint_proc_log.debug("Response success? " + str(status))
        # response not currently used...
        hint_proc_log.debug("Returning Response: %s", response)
        return response

    def parse_json(self, json_string):
        """
        Accepts a JSON string and returns a dictionary object

        :param json_string: String of a JSON block
        :return: Dictionary object
        """
        hint_proc_log.debug("trying to parse str into dict..." + str(json_string))
        z = json.loads(json_string)
        hint_proc_log.debug("Returning json: %s", z)
        return z
