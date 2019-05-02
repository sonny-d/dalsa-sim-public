"""
A module used for starting and controlling the camera simulator.

cmd docs:
https://docs.python.org/3/library/cmd.html
https://docs.python.org/2.7/library/cmd.html
"""

import cmd
import logging
from log.log import file_handler
from camsim import simulator_main

# cli Log
cli_log = logging.getLogger('dalsasim.cli')  # type: logging
cli_log.setLevel(logging.DEBUG)
cli_log.addHandler(file_handler)


class Shell(cmd.Cmd):
    intro = '\n===\nDalsa CamSim Module: Type help or ? to start\n===\n'
    cli_log.debug("Dalsa CamSim Module")
    prompt = '(cmd)'
    sim = None  # Class variables, should be instance if we ever need to run multiple sims at same time...
    sim_port1 = 5021
    sim_port2 = 5024
    sim_hint_port = 5055

    # ----- commands -----

    def do_set_ports(self, arg):
        """Set the ports before starting a simulator instance."""
        p1 = raw_input("Enter primary camera port for sim (blank for default) --> ").strip()
        p2 = raw_input("Enter secondary camera port for sim (blank for default) --> ").strip()
        h = raw_input("Enter hinting por for sim (blank for default) --> ").strip()
        # Validate input, and only set if a non-blank entry
        if p1:
            self.sim_port1 = int(p1)
        if p2:
            self.sim_port2 = int(p2)
        if h:
            self.sim_hint_port = int(h)
        cli_log.debug("Ports have been saved.")

    def do_start(self, arg):
        """Start the Dalsa camera simulator"""
        cli_log.debug("\nDalsaSim: Starting the simulator with values:")
        print("\nDalsaSim: Starting the simulator with values:")
        cli_log.debug("  Primary port: " + str(self.sim_port1))
        print("  Primary port: " + str(self.sim_port1))
        cli_log.debug("  Secondary port: " + str(self.sim_port2))
        print("  Secondary port: " + str(self.sim_port2))
        cli_log.debug("  Hinting port: %s" % self.sim_hint_port) # This is the other way to concatenate string w/ number
        print("  Hinting port: %s" % self.sim_hint_port)
        self.sim = simulator_main.Simulator(self.sim_port1, self.sim_port2, self.sim_hint_port)
        print "Hostname of server is: "
        self.do_gethostname("")
        print "\n"

    # These have been replaced by combined do_listen, for now
    # def do_camlisten(self, arg):
    #     """Set the Dalsa simulator's server to listen for connections"""
    #     # Check if Sim has been started yet
    #     if not self.sim:
    #         print "Simulator not yet started. Starting now..."
    #         self.do_start("")
    #     self.sim.start_listen()
    #
    # def do_hintlisten(self, arg):
    #     """Set the Dalsa simulator's hint server to listen for connections"""
    #     # Check if Sim has been started yet
    #     if not self.sim:
    #         print "Simulator not yet started. Starting now..."
    #         self.do_start("")
    #     self.sim.start_hint_listen()

    def do_listen(self, arg):
        """Set the Dalsa simulator's server to listen for connections"""
        if not self.sim:
            print "Simulator not yet started. Starting now..."
            cli_log.info("Simulator not yet started. Starting now...")
            self.do_start("")
        #print "DEBUG: starting hint listen"
        cli_log.debug("Starting hint listen")
        self.sim.start_hint_listen()
        #print "DEBUG: starting command listen"
        cli_log.debug("Starting command listen")
        self.sim.start_listen()

    def do_stop_server(self, arg):
        """Stop the Dalsa simulator's server"""
        # Check if Sim has been started yet
        if not self.sim:
            print "Error: No servers running at this time. Run \"start\" command to begin."
            cli_log.error("No servers running at this time. Run \"start\" command to begin.")
            return
        self.sim.stop_server()
        pass

    def do_status(self, arg):
        """Query the simulator status"""
        if not self.sim:
            print "Error: No servers running at this time. Run \"start\" command to begin."
            cli_log.error("No servers running at this time. Run \"start\" command to begin.")
            return
        print ("cmd: Checking simulator status...")
        cli_log.error("cmd: Checking Simulator Status...")
        try:
            print (self.sim.get_status)
            cli_log.debug("Status: %s", str(self.sim.get_status()))
        except AttributeError:
            print ("No simulator is running.")
            cli_log.error("No Simulator is Running... not good")

    def do_gethostname(self, arg):
        """Query the simulator server hostname"""
        if not self.sim:
            cli_log.error("No servers running at this time. Run \"start\" command to begin.")
            print "Error: No servers running at this time. Run \"start\" command to begin."
            pass
        host = self.sim.get_hostname()
        cli_log.debug("Hostname: %s", host)
        return host

    def do_stop(self, arg):
        """Stop the simulator"""
        print ("cmd: Attepting to stop simulator...")
        cli_log.debug("cmd: Attempting to Stop Sim")
        try:
            del self.sim
            cli_log.debug("Stopped Sim")
            self.do_status('')
        except AttributeError:
            print ("Error: No simulator is running.")
            cli_log.error("No Simulator is Running...")

    def do_exit(self, arg):
        """Stop any running simulator and exit"""
        print ("\n\nAdios, amigo...")
        cli_log.debug("EXIT... Adios, amigo")
        # self.do_stop('')  # This is optional, I think...
        # Returning True signals cmd module to quit. Can make a fancier function if we need later.
        return True

    # ----- processing functions -----
    # def precmd(self, line):
    #     """
    #     Runs before any command.
    #     This one just repeats the command entered, for debugging
    #     """
    #     line = line.lower()
    #     print "A line was entered: " + line
    #     return line


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
