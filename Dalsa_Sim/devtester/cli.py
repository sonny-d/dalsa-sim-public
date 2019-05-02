"""
A SUPER SIMPLE tester module used for testing interacitons with the camera simulator package.

cmd docs:
https://docs.python.org/3/library/cmd.html
https://docs.python.org/2.7/library/cmd.html
"""

from log.log import file_handler
from tester_main import Tester
import cmd
import json
import logging


# cli log
cli_tester_log = logging.getLogger('devtester.cli')
cli_tester_log.setLevel(logging.DEBUG)
cli_tester_log.addHandler(file_handler)


class Shell(cmd.Cmd):
    intro = '\n===\nDalsa CamSim DEV TESTER CLIENT: Type help or ? to start\n===\n'
    prompt = '(cmd)'  # type: str
    sim = None  # Class variables, should be instance if we ever need to run multiple sims at same time...
    sim_port1 = 5021  # type: int
    sim_port2 = 5024  # type: int
    sim_hint_port = 5055  # type: int
    host = "localhost"
    tester = None

    # ----- commands -----
    def do_set_ports(self, arg):
        """Set the ports before starting a simulator instance."""
        p1 = raw_input("Enter primary camera port for sim (blank for default) --> ").strip()
        p2 = raw_input("Enter secondary camera port for sim (blank for default) --> ").strip()
        h = raw_input("Enter hinting por for sim (blank for default) --> ").strip()
        # Validate input, and only set if a non-blank entry
        if p1:
            self.sim_port1 = p1
        if p2:
            self.sim_port2 = p2
        if h:
            self.sim_hint_port = h
        print "Ports have been saved."
        cli_tester_log.debug("Ports have been saved")

    def do_start(self, arg):
        """Start the Tester main class"""
        # Accept input of hostname
        if arg:
            print "Hostname argument received: " + arg
            cli_tester_log.debug("Hostname argument recv: %s", arg)
            self.host = arg
        else:
            self.host = raw_input("Enter hostname of Dalsa cam or simulator (blank for localhost) --> ").strip()
        # Set host to default
        # TODO: Check if hostname conatins any spaces...
        if self.host == "":
            self.host = "localhost"

        print("\nDevTester: Starting the simulator with values:")
        cli_tester_log.debug("DevTester: Starting the simulator with values:")
        print ("  Hostname: %s" + str(self.host))
        cli_tester_log.debug("Hostname: %s" + str(self.host))
        print ("  Primary port: %s" + str(self.sim_port1))
        cli_tester_log.debug("Primary port: %s" + str(self.sim_port1))
        print ("  Secondary port: " + str(self.sim_port2))
        cli_tester_log.debug("Secondary port: %s" + str(self.sim_port2))
        print ("  Hinting port: " + str(self.sim_hint_port))  # This is the other way to concatenate string w/ number
        cli_tester_log.debug("Hinting port: %s", self.sim_hint_port)
        self.tester = Tester(self.host, self.sim_port1, self.sim_port2, self.sim_hint_port)
        cli_tester_log.debug("Created New instance of Tester...")

    def do_sendhint(self, arg):
        """Start a Hint Client and send hint argument"""
        # Check if Tester has been started yet
        if not self.tester:
            self.do_start("")
        if arg:
            print "Received argument: " + arg + " Ignoring. Will prompt for hint values..."
            cli_tester_log.debug("Received argument: %s Ignoring. Will prompt for hint values...", arg)

        # Get hint API spec
        # TODO: Enhance this to walk through the json levels...
        json_spec = self.tester.get_json_spec()
        print "DEBUG: json API spec + " + str(json_spec)
        cli_tester_log.debug("json API spec + " + str(json_spec))
        hint_json = {}  # The dictionary object to store our hint params

        # Prompt user for the hint parameters
        print "\nHint command requires %s parameters:" % len(json_spec)
        cli_tester_log.debug("Hint command requires %s parameters", len(json_spec))
        print "\nEnter values or press enter to leave blank"
        for key in json_spec:
            # Started an attempt at traversing nested JSON...
            # print "key:" + str(key)
            # print "key value? " + str(json_spec[key])
            # if isinstance(json_spec[key], dict):
            #     pass
            value = raw_input("Enter " + str(key) + " --> ")
            hint_json[key] = value
        # Convert that dictionary into a nice string
        # Sendit
        print "DevTester: Starting the client with values:"
        cli_tester_log.debug("Starting Values...")
        print "  Hinting port: %s" % self.sim_hint_port
        cli_tester_log.debug("Hinting Port: %s", self.sim_hint_port)
        print "  Hostname: %s" % self.host
        cli_tester_log.debug("Hostname : %s", self.host)
        hint_string = json.dumps(hint_json)
        cli_tester_log.debug("Dumping dictionary into str")
        print "  DEBUG: Hint to send: " + str(hint_string)
        cli_tester_log.debug("Hint to send: %s", str(hint_string))
        print "\n"
        # Store the hint parameter JSON dict in tester
        self.tester.set_hints(hint_json)
        # Send the hint via client
        self.tester.send_hint(hint_string)
        cli_tester_log.debug("Hint Sent")
        pass

    def do_sendcmd(self, arg):
        """Start a Camera Client and send command argument. ex: sendcmd getBarcode()"""
        # Check if Tester has been started yet
        if not self.tester:
            self.do_start("")
        # Check if a cmd was entered
        if not arg:
            arg = raw_input("Enter camera command to send --> ")
            # TODO: format into JSON here? or in tester_main...
        print "DEBUG: Trying to send cmd: " + arg
        cli_tester_log.debug("Trying to send cmd: %s", str(arg))
        self.tester.send_cmd(str(arg))
        cli_tester_log.debug("%s sent", str(arg))

    def do_exit(self, arg):
        """Stop any running client and exit"""
        print ("\n\nAdios, amigo...")
        cli_tester_log.debug("Exiting... Adios, amigo")
        # self.do_stop('')  # This is optional, I think...
        # Returning True signals cmd module to quit. Can make a fancier function if we need later.
        return True

    def do_test_suit(self, arg):
        if not self.tester:
            self.do_start("")
        if arg:
            print "Received argument: " + arg + " Ignoring. Will prompt for hint values..."
        json = tester_main.fill_json(self.tester)
        print json
        pass


# Parses arguments for each command
def parse(arg):
    """Convert a series of zero or more numbers to an argument tuple - not yet being used"""
    return tuple(map(int, arg.split()))


# Main method
def main():
    Shell().cmdloop()


# Main pointer... I dunno, it's a Python thing.
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
    main()
