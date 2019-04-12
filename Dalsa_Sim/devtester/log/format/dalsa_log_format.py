# /Dalsa_Sim/Log/dalsa_log_format.py

import logging
# ADD COLOR TO LEVELNAME
# File Handler format
# ==================================
socket_handler_format = logging.Formatter('%(asctime)s: |@%(name)s| - %(levelname)s: %(message)s')
# ==================================

# File Handler format
# ==================================
file_handler_format = logging.Formatter('%(asctime)s: |@%(name)s| - %(levelname)s: %(message)s')
# ==================================
