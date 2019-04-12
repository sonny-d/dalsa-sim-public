# log/log.py
from format.dalsa_log_format import file_handler_format
import logging
import os


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

# Creating Logs & Adding Handlers
# ==================================

# ========================
# Root
# ========================
"""dalsa_sim_log = logging.getLogger('dalsasim')  # type: logging
dalsa_sim_log.setLevel(logging.DEBUG)
dalsa_sim_log.addHandler(file_handler)"""
# dalsa_sim_log.addHandler(socket_handler)
# -------------------------------------


# ========================
# 1st Level MAY NOT NEED TO HAVE THESE PACKAGES INSTANTIATED
# ========================

# -------------------------------------


# ========================
# 2nd level
# ========================

# hint_server_log.addHandler(socket_handler)
# -------------------------------------

# Log Server (Package)
server_logserver_log = logging.getLogger('dalsasim.server.logserver')
server_logserver_log.setLevel(logging.DEBUG)
server_logserver_log.addHandler(file_handler)
# -------------------------------------

# ========================
# 3rd level
# ========================


# cli log
cli_tester_log = logging.getLogger('devtester.cli')
cli_tester_log.setLevel(logging.DEBUG)
cli_tester_log.addHandler(file_handler)

# Hint Client (Class)
hintclient_log = logging.getLogger('devtester.client.hint_client')
hintclient_log.setLevel(logging.DEBUG)
hintclient_log.addHandler(file_handler)
# hintserver_server_log.addHandler(socket_handler)
# -------------------------------------

client_log = logging.getLogger('devtester.client.hint_client')
client_log.setLevel(logging.DEBUG)
client_log.addHandler(file_handler)

camclient_log = logging.getLogger('devtester.client.camclient')
camclient_log.setLevel(logging.DEBUG)
camclient_log.addHandler(file_handler)

# Cam Server (Class)
cam_server_log = logging.getLogger('dalsasim.server.camserver.cam_server')
cam_server_log.setLevel(logging.DEBUG)
cam_server_log.addHandler(file_handler)
