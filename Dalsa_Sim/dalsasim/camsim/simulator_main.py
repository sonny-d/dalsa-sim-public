import sys
from server.camserver.cam_server import CamServer
from server.hintserver.hint_server import HintServer
from cmdprocess import cmd_processor


class Simulator(object):
    """
    The main class of the cam_sim. Creates the cam_server, hint_server, and cmd_processor.
    When cam_server or hint_server receive a request, they will callback to this Simulator to pass the command to the
    cmd_processor.
    """

    def __init__(self, cam_primary_port, cam_secondary_port, hint_port):
        """

        :param cam_primary_port:
        :param cam_secondary_port:
        :param hint_port:
        """

        print "SIMULATOR: initing a new simulator object"

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
        print "Dalsa Simulator is now ready to receive hints or camera commands."

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
        data = self.cam_server.receive()
        # Waits here until data is received...
        print "On: " + self.cam_server.server_name + '  Received data: ' + data
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

    def stop_server(self):
        self.cam_server.close()
        #self.cam_server2.close()
        print "Dalsa Server shutdown"

    def handle_cam_cmd_callback(self, server, command):
        # do some processing, then
        response = cmd_processor.CmdProcessor(command)
        server.return_response(response)
        pass

    def handle_hint_cmd_callback(self, server, command):
        # do some processing,
        response = cmd_processor.CmdProcessor(command)
        # then
        server.return_response(response)
        pass

    def _start_cam_server(self):
        #print "This is where we start a Cam Server"
        try:
            # fake error for testing
            # badnum = 1/0
            #cam_svr = cam_server.CamServer(self.cam_port1, self.cam_port2, self)

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
        #print "This is where we start a Hint Server"
        # hint_svr = hint_server_main.HintServerMain(self.hint_svr_port, self)
        hint_svr = HintServer(self.hint_svr_port, "Hint Server 1")
        print "Simulator: Hint server ports open: " + str(hint_svr.get_sockets())
        return hint_svr

    def _start_log_server(self):
        """
        Specifications call for autologging on port 5022? More info needed, out of scope for protoype2.
        """
        pass
