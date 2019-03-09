"""
A SUPER SIMPLE tester module used for testing interacitons with the camera simulator package.

cmd docs:
https://docs.python.org/3/library/cmd.html
https://docs.python.org/2.7/library/cmd.html
"""

import cmd
# import sys
from tester_main import Tester



class Shell(cmd.Cmd):
    intro = '\n===\nDalsa Sim Module: CLI... Type help or ? to start\n===\n'
    prompt = '(cmd)'
    sim = None  # Class variables, should be instance if we ever need to run multiple sims at same time...
    sim_port1 = 5021
    sim_port2 = 5024
    sim_hint_port = 5055

    # ----- commands -----
    def do_set_hint_port(self, arg):
        pass

    def do_start(self, arg):
        """Start the Tester main class simulator"""
        print("cmd: Starting the simulator with values:")
        print ("Primary port: " + str(self.sim_port1))
        print ("Secondary port: " + str(self.sim_port2))
        print ("Hinting port: %s" % self.sim_hint_port) # This is the other way to concatenate string w/ number
        self.tester = Tester(self.sim_port1, self.sim_port2, self.sim_hint_port)

    def do_sendhint(self, arg):
        """Start a Hint Client and send hint argument"""
        print("cmd: Starting the client with values:")
        print ("Hinting port: %s" % self.sim_hint_port)
        self.tester = Tester(self.sim_port1, self.sim_port2, self.sim_hint_port)  # Duplicate
        self.tester.send_hint(str(arg))

    def do_sendcmd(self, arg):
        """Start a Camera Client and send command argument. ex: sendcmd getBarcode()"""
        self.tester = Tester(self.sim_port1, self.sim_port2, self.sim_hint_port)
        self.tester.send_cmd(str(arg))

    def do_exit(self, arg):
        """Stop any running client and exit"""
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
