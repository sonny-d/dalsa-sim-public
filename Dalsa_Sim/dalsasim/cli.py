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
    intro = '\n===\nDalsa Sim Module: CLI... Type help or ? to start\n===\n'
    prompt = '(cmd)'
    sim = None  # Class variables, should be instance if we ever need to run multiple sims at same time...
    sim_port1 = 5021
    sim_port2 = 5024
    sim_hint_port = 5055

    # ----- commands -----
    def do_test(self, arg):
        # This command has docs defined externally, in help_test()
        print("This is a test")
        # This shows how arguments could be parsed
        # test(*parse(arg))

    def help_test(self):
        print("This is the manually defined help string for \'test\' command.")

    def do_other_test(self, arg):
        # This command has no documentation defined
        print("This is also a test with arg = " + str(arg))
        # This shows how arguments could be parsed
        # test(*parse(arg))

    def do_set_hint_port(self, arg):
        pass

    def do_start(self, arg):
        """Start the Dalsa camera simulator"""
        print("cmd: Starting the simulator with values:")
        print ("Primary port: " + str(self.sim_port1))
        print ("Secondary port: " + str(self.sim_port2))
        print ("Hinting port: %s" % self.sim_hint_port) # This is the other way to concatenate string w/ number
        self.sim = simulator_main.Simulator(self.sim_port1, self.sim_port2, self.sim_hint_port)

    def do_camlisten(self, arg):
        """Set the Dalsa simulator's server to listen for connections"""
        self.sim.start_listen()

    def do_hintlisten(self, arg):
        """Set the Dalsa simulator's hint server to listen for connections"""
        self.sim.start_hint_listen()

    def do_stop_server(self, arg):
        self.sim.stop_server()

    def do_status(self, arg):
        """Query the simulator status"""
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


# We may not need this unless we start accepting input arguments with commands
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
