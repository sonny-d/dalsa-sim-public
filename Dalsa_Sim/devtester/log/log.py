# log/log.py
from format.dalsa_log_format import file_handler_format
import logging
import os, datetime


# Created By : Benjamin Nelligan
# Date : January 15, 2019
# Description : this holds all of the log variables to be imported throughout simulation. Will also make error
# and debugging easier. Allows user to change logging levels for each log.


def get_file_path():
    """
    Created By: Brendino
    Find relative path to make the log folder.
    This is probably more complex than it needs to be. But it works.
    :return: File path of folder containing the Python project
    """
    file_path = os.path.dirname(__file__)
    # Go up 2 dirs
    for x in range(0, 2):
        file_path = os.path.split(file_path)[0]
        #print "DEBUG: Logger: Current file path is: " + str(file_path)
    # Return the result
    if len(file_path) is 0:
        #print "Log path not found, trying relative path..."
        file_path = ".."
    return file_path


# Ports
# ==================================
log_port = 5023
# ==================================

# Log path and filename
# ==================================
log_file = 'Tester_Log.txt'
log_path = get_file_path() + '/Dalsa_Log_Result/'
# ==================================

# Creating log Location
# ==================================
log_location = log_path + log_file
# ==================================

# Creating instances of the handlers
# ==================================
file_handler = logging.FileHandler(log_location)
# socket_handler = logging.handlers.SocketHandler(hostname, log_port)
# ==================================

# Setting format
# ==================================
# socket_handler.setFormatter(socket_handler_format)
file_handler.setFormatter(file_handler_format)
# ==================================





