# Dalsa_Sim/dalsa_barcode_gen/Barcode.py
# Created By : Benjamin Nelligan
# Created : November 20, 2018
# Last Modified : Benjamin Nelligan
# Last Modified Date : February 10, 2019
import camsim.barcode.qr
from log import log


# ================================= #
# Date : November 20, 2018
# Created By : Benjamin Nelligan Description : This will create a Barcode object
# wih a QR as its content. It will return true/false based upon validity of status
# MUST USE GLODAL VARIABLE FOR INIT. Because it holds class methods, there will only be one barcode simulated at a time.
# May need to alter that to satisfy multi-test
# Last Modified : December 3, 2018
# ================================= #

class Barcode(camsim.barcode.qr.QR):
    # Creating class variables & Log variables
    # Creating qr object| Could have options here
    # Status variable
    status = '---- NOTSET ----'

    def __init__(self):
        # Creating inheritance
        super(Barcode, self).__init__(self)

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : checks if the barcode is ready... Meaning is there content in the Barcode
    # Added logging for error control
    # Last Modified : Feb 10
    # ================================= #
    def is_barcode_ready(self):
        if self.content is None:
            self.status = '---- FAILED ----'
            log.error('Barcode Status : %s', self.status)
            return self
        else:
            self.status = '---- READY ----'
            log.info('Barcode Status : %s', self.status)
            return self

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : reads the barcode object
    # Added logging for error control
    # Last Modified : Feb 10
    # ================================= #
    def read_barcode(self):
        log.info('Reading Barcode : %s', self)
        if self.content == self.content:
            log.info('Barcode Confirmed')
        else:
            log.error('Barcode is not the same')

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : gets the barcode, Added logging for error control
    # Last Modified : Feb 10
    # ================================= #
    def get_barcode(self):
        if self.content is None:
            log.error('---- Barcode Empty : %s', self.content)
            self.status = '---- ERROR ----'
            return self.status
        else:
            log.info('----- getBarcode() : %s', self.content)
            return self.__str__()
