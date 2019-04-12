

from client.hint_client import HintClient
from client.cam_client import CamServerClient


class Tester(object):
    """
    The main class of the devtester. Creates the clients and controls interactions with the simulator package.
    """

    json = {"test-id": None, "qr": None}  # Hint API v1, simplified

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
        print "Dev Tester: Initialized a new tester instance\n"

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
        client_name = "Hint Client"
        hint_client = HintClient(self.host_name, self.hint_svr_port, client_name)
        hint_client.connect()

        response = hint_client.send(hint)
        print "On: " + hint_client.client_name + "  Success Status: " + str(response)
        hint_client.close()

    def send_cmd(self, cmd):
        """
        Start a cam_client and send the Dalsa command.

        :param cmd: A string command to send to Cam Sim
        :return:
        """
        print "DEBUG: Trying to connect client to Server..."
        client_name = "Dalsa Client"
        cam_client = CamServerClient(self.host_name, self.cam_port1, client_name)
        cam_client.connect()
        response = cam_client.send(cmd)
        print "On: " + cam_client.client_name + "  Success Status: " + str(response)
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
            self.host_name = server_hostname_or_ip
        else:
            print "Invalid server hostname"
