from log.log import file_handler
import socket
from client.hint_client import HintClient
from client.cam_client import CamServerClient
import logging

tester_log = logging.getLogger('devtester.tester_main.Tester')
tester_log.setLevel(logging.DEBUG)
tester_log.addHandler(file_handler)
tester_log.debug("Created instance of Tester Log")


class Tester(object):
    """
    The main class of the devtester. Creates the clients and controls interactions with the simulator package.
    """

    # Hint API v1, simplified. Used by CLI to prompt user for hint values
    json = {"test-id": None, "qr": None, "weather-cond": None, "err-no-response": None, "err-communication": None}

    def __init__(self, cam_hostname, cam_primary_port, cam_secondary_port, hint_port):
        """

        :param cam_primary_port:
        :param cam_secondary_port:
        :param hint_port:
        """
        # init the variables
        self.host_name = cam_hostname
        self.cam_port1 = cam_primary_port
        self.cam_port2 = cam_secondary_port
        self.hint_svr_port = hint_port
        self.hints = {}
        print "Dev Tester: Initialized a new tester instance\n"
        tester_log.debug("Initialized a new tester instance")

    def get_json_spec(self):
        return self.json

    def send_hint(self, hint):
        """
        Start a hint_client and send the hint string.
        TODO: This will need to be able to set certain variables, and send as a JSON string. Later...

        :param hint:
        :return:
        """
        print "DEBUG: Trying to connect client to Server..."
        tester_log.debug("Trying to connect client to Server...")
        client_name = "Hint Client"
        tester_log.debug("Creating Instance of HintClient")
        hint_client = HintClient(self.host_name, self.hint_svr_port, client_name)
        tester_log.debug("Connecting HintClient to ports: %s", str(self.hint_svr_port))
        hint_client.connect()
        tester_log.debug("Sending hint and waiting for response...")
        response = hint_client.send(hint)
        tester_log.debug("Response: %s", str(response))

        # print "On: " + hint_client.client_name + "  Success Status: " + str(response)
        # tester_log.debug("On %s  Success Status: %s", hint_client.client_name, str(response))
        # print "DEBUG: Hint processed code: %s" % str(response)
        # tester_log.debug("Hint processed code: %s", str(response))
        if response:
            try:
                if int(response) is 1:
                    print "Hint processed successfully"
                    tester_log.debug("Hint Processed Right")
                    pass
                else:
                    print "Hint not processed successfully... check the logs."
                    tester_log.error("Hint not Processed Right... check logs")
                    pass
            except Exception as e:
                tester_log.error("Exception: %s", e)
                print "Hint not processed successfully... check the logs."
                tester_log.error("Hint not Processed Right... check logs")
                pass
        else:
            print "Hint not processed successfully... check the logs."
            tester_log.error("Hint not Processed Right... check logs")
            pass

        # TODO: shouldn't need to close this yet.
        tester_log.debug("Closing Hint Client")
        hint_client.close()

        # try:
        #     response = hint_client.send(hint)
        #     print "On: " + hint_client.client_name + "  Success Status: " + str(response)
        #     print "DEBUG: Hint processed code: %s" % str(response)
        #     if response:
        #         if int(response) is 1:
        #             print "Hint processed successfully"
        #         else:
        #             print "Hint not processed successfully... check the logs."
        #     # TODO: shouldn't need to close this yet.
        #     hint_client.close()
        # except socket.error as e:
        #     print "Socket Error: %s", e

    def send_cmd(self, cmd):
        """
        Start a cam_client and send the Dalsa command.

        :param cmd: A string command to send to Cam Sim
        :return:
        """
        print "DEBUG: Trying to connect client to Server..."
        tester_log.debug("Trying to connect client to Server")
        client_name = "Dalsa Client"
        tester_log.debug("Creating instance of Cam_Client")
        cam_client = CamServerClient(self.host_name, self.cam_port1, client_name)
        tester_log.debug("Connecting Cam_Client")
        cam_client.connect()
        tester_log.debug("Sending cmd, and waiting for response")
        response = cam_client.send(cmd)
        print "\nResponse: \n" + str(response) + "\n"
        tester_log.debug("Response: %s", str(response))

        # Compare result w/ expected value
        cmd, result = self.parse_response(response)

        self.compare_result(cmd, result, self.hints)

        # Current design closes client socket after each command
        tester_log.debug("Closing Cam Client")
        cam_client.close()

    def set_hostname(self, server_hostname_or_ip):
        """
        Description : Set hostname/IP of remote server
        Date : April 4, 2019
        Created By : Brendan Dunne

        :param server_hostname_or_ip: string of IP address or hostname of server
        :return:
        """
        if server_hostname_or_ip:
            tester_log.debug("Setting Hostname: %s", server_hostname_or_ip)
            self.host_name = server_hostname_or_ip
        else:
            print "Invalid server hostname"
            tester_log.error("Did not Set Hostname... Check Log")

    def set_hints(self, json_obj):
        """
        Accept the dict of JSON key:value pairs sent as hints to server.
        :param json_obj:
        :return:
        """
        self.hints = json_obj

    def parse_response(self, response):
        """
        Accept a response from camera response, and return the relevant result portion.
        Example response: isbarcodeready() , Result: 0.000000
        :param response: String response from server/camsim
        :return: Tuple: cmd, result
        """
        cmd = ""
        result = ""
        # First transform to lowercase
        #tester_log.debug("Forcing response to lowercase")
        #r = response.lower().strip()
        r = str(response).strip()
        tester_log.debug("New string: %s", r)

        # Then split it up
        if r:
            res_list = r.split(" ")  ##splits at spaces
            # Standard response should split into 4 items: "isbarcodeready() , Result: 0.000000"
            if len(res_list) >= 4:
                cmd = res_list[0]
                result = res_list[3]
                tester_log.info("parse_response: Parsed cmd = %s, result = %s", cmd, result)
            else:
                tester_log.error("parse_response:Unexpected response format received, cannot be parsed.")
        else:
            cmd = ""
            tester_log.error("parse_response: No response received")

        tester_log.debug("parse_response: parsed result is " + str(result))
        return cmd, result

    def compare_result(self, command, result, stored_hints):
        """
        Compare result from camera with the hinted value expected.
        TODO: Very simple comparison, should also take into account good/bad weather...
        A smart comparison involves keep a record of commands executed. Maybe a simple list or stack...
        :param command: The command processed
        :param result: The result from camera
        :param stored_hints: The dict of the hint sent to simulator
        :return:
        """

        # Based on JSON hint params, just check QR for now
        if stored_hints["test-id"]:
            test_id = stored_hints["test-id"]
        else:
            test_id = "01"
        if command in ["GetBarcode()", "getbarcode()"]:
            if result and stored_hints["qr"]:
                # Ignore numerical response codes
                if result in ["0.000000", "1.000000"]:
                    tester_log.info("Non QR value received for GetBarcode, likely no barcode ready.")
                    pass
                else:
                    # Must be a QR value, so compare
                    print "Test ID " + str(test_id) + ", Comparing GetBarcode() response to expected value:"
                    if result == stored_hints["qr"]:
                        print "  PASS: Result barcode returned matches the expected/hinted value.\n"
                        tester_log.info("Result barcode returned matches the expected/hinted value.")
                    else:
                        print "  FAIL: Result barcode does not match the expected/hinted value.\n"
                        tester_log.info("FAIL: Result barcode does not match the expected/hinted value.")
            else:
                if result:
                    print "Unable to compare result automatically. Compare manually:"
                    print "  Result from camera:" % result
                    print "  hint: %s" % str(stored_hints)
                    tester_log.error("Unable to automatically match result and hint. Printing out for human comparison.")
                else:
                    tester_log.error("Unable to compare results... Result missing or null")
                    print "ERROR: unable to compare results..."


test_dictionary = {
    "Test_1": "abinvruienviugvimpome943\t|/vin., okpo`-012i`j12n`;42kr.4m2lg vp42;o5j0tu1enrviunkjdnf",
    "Test_2": "wefwefwibiu\n\n\n\n\n\n\n\\n\n\n\n\n\nnn\n\n\nbiubiu",
    "Test_3": "wein34242oweincoi34wencoiw43242342341nweoicwne",
    "Test_4": "wein4134135434g24v4ctc34c2c5we    qoweincoiw234`1342encoiwncoinweoicwne",
    "Test_5": "/\/\/\/\/\/\/\/\/\/\\\n\n\n\n\n\\\\\\t\t\g\\\s\er\trf\g\t\g\nh\/",
    "Test_6": "MAtthew_W",
    "Test_7": "Bren}din{}{oc}hinobino"
    }


def fill_json(tester, json_dictionary=None):
    struct = {"testid": None,
              "qr": None}
    final_result = {}
    if json_dictionary is None:
        for key, value in test_dictionary.items():
            struct["testid"] = key
            struct["qr"] = value
            final_result.update(struct)
            tester.send_hint(str(struct))
    return final_result

