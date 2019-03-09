"""
A module for processing the commands that are sent from the driver.
Accepts a hint from the hint_server or a command from the cam_server.
Returns appropriate responses (like a QR code string) to cam_server.
"""


class CmdProcessor(object):

    def __init__(self, command_to_process):
        print "CmdProcessor: initialized"
        self.command = command_to_process
        self.process_cmd()

    def process_cmd(self):
        """
        Parses the command and performs the appropriate action.

        :param command_str: command from driver, should match standard ASML command set
        :return: string response from cam sim, or empty string if command was invalid.
        """

        command = self.command
        print "Server " + self.serverId + " received command " + command + " and will process..."

        # Auto_tester creates the qr_gen at boot and we use it here. Return a simple string with result
        # Match ASML camera command with correct method
        if command == "IsBarcodeReady()":
            print "Command was: " + "IsBarcodeReady()"
            response = self._is_barcode_ready()
        elif command == "ReadBarcode()":
            print "Command was: " + "ReadBarcode()"
            response = self._read_barcode()
        elif command == "GetBarcode()":
            print "Command was: " + "GetBarcode()"
            response = self._get_barcode()
        elif command == "GetVersion()":
            print "Command was: " + "GetVersion()"
            response = self._get_version()
        else:
            print "Cam_Server: Invalid command received: " + command
            response = ""
        print "SERVER.PROCESS_CMD: Response = " + str(response)
        return response

    def _is_barcode_ready(self):
        print "SERVER: Is barcode ready?"
        return self.qr_simulator.is_barcode_ready()

    def _read_barcode(self):
        print "Is barcode ready?"
        return self.qr_simulator.read_barcode()

    def _get_barcode(self):
        print "Is barcode ready?"
        return self.qr_simulator.get_barcode()

    def _get_version(self):
        """
        Returns version of this camera firmware (simulator).

        :return: string of version information.
        """
        print "GetVersion:"
        return self.server_version
