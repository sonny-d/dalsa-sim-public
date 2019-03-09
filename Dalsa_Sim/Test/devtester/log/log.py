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
    for x in range(0, 3):
        file_path = os.path.split(file_path)[0]
        print str(file_path)
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
# Server (Package)
"""server_log_main = logging.getLogger('dalsasim.server')  # type: logging
server_log_main.setLevel(logging.DEBUG)
server_log_main.addHandler(file_handler)"""
# -------------------------------------

# Command Process (Package)
"""cmd_process_log_main = logging.getLogger('dalsasim.cmdprocess')  # type: logging
cmd_process_log_main.setLevel(logging.DEBUG)
cmd_process_log_main.addHandler(file_handler)"""
# -------------------------------------

# Camera Server (Package)
"""primary_server_log = logging.getLogger('dalsasim.server.camserver')
primary_server_log.setLevel(logging.DEBUG)
primary_server_log.addHandler(file_handler)
# primary_server_log.addHandler(socket_handler)"""
# -------------------------------------


# ========================
# 2nd level
# ========================

# Main Structure Client Log (Class)


# Main Structure Server Log (Class)


# Command Process

# Cam Server


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


# Dalsa_Sim.dalsa_log_server
dalsa_log_server = logging.getLogger('dalsasim.server.logserver.log_server_main')  # type: logging
dalsa_log_server.setLevel(logging.DEBUG)
dalsa_log_server.addHandler(file_handler)



# Hint Server (Class)
hintserver_server_log = logging.getLogger('dalsasim.server.hintserver.hint_server')
hintserver_server_log.setLevel(logging.DEBUG)
hintserver_server_log.addHandler(file_handler)
# hintserver_server_log.addHandler(socket_handler)
# -------------------------------------


# Cam Server (Class)
cam_server_log = logging.getLogger('dalsasim.server.camserver.cam_server')
cam_server_log.setLevel(logging.DEBUG)
cam_server_log.addHandler(file_handler)
