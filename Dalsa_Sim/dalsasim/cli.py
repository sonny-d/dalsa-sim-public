"""
A module used for starting and controlling the camera simulator.

cmd docs:
https://docs.python.org/3/library/cmd.html
https://docs.python.org/2.7/library/cmd.html
"""

import cmd
# import sys
from camsim import simulator_main


class Shell(cmd.Cmd):
    intro = '\n===\nDalsa CamSim Module: Type help or ? to start\n===\n'
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
        print "Ports have been saved."

    def do_start(self, arg):
        """Start the Dalsa camera simulator"""
        print("\nDalsaSim: Starting the simulator with values:")
        print ("  Primary port: " + str(self.sim_port1))
        print ("  Secondary port: " + str(self.sim_port2))
        print ("  Hinting port: %s" % self.sim_hint_port) # This is the other way to concatenate string w/ number
        self.sim = simulator_main.Simulator(self.sim_port1, self.sim_port2, self.sim_hint_port)

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
            self.do_start("")
        print "DEBUG: starting hint listen"
        self.sim.start_hint_listen()
        print "DEBUG: starting command listen"
        self.sim.start_listen()

    def do_stop_server(self, arg):
        """Stop the Dalsa simulator's server"""
        # Check if Sim has been started yet
        if not self.sim:
            print "Error: No servers running at this time. Run \"start\" command to begin."
            return
        self.sim.stop_server()

    def do_status(self, arg):
        """Query the simulator status"""
        if not self.sim:
            print "Error: No servers running at this time. Run \"start\" command to begin."
            return
        print ("cmd: Checking simulator status...")
        try:
            print (self.sim.get_status())
        except AttributeError:
            print ("No simulator is running.")

    def do_stop(self, arg):
        """Stop the simulator"""
        print ("cmd: Attepting to stop simulator...")
        #self.sim.stop()
        try:
            del self.sim
            self.do_status('')
        except AttributeError:
            print ("Error: No simulator is running.")

    def do_exit(self, arg):
        """Stop any running simulator and exit"""
        print ("\n\nAdios, amigo...")
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
    'Convert a series of zero or more numbers to an argument tuple - not yet being used'
    return tuple(map(int, arg.split()))


# Main method
def main():
    Shell().cmdloop()


# Main pointer... I dunno, it's a Python thing.
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
    main()
