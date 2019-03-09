import csv
import os
import json

from log import dalsa_qr_log
from camsim.barcode import test_file


# ================================= #
# Date : November 20, 2018
# Created By : Benjamin Nelligan
# Description : This will create a QR object wih appropriate attributes of content, version, error_level, and encoding.
# This class also has a .fill_data() that will grab information from a csv file, instantiated above.
# MUST USE GLODAL VARIABLE FOR INIT
# Could send object of QR_LOG to QR
# Last Modified : Feb 11, 2018
# ================================= #

class QR(object):

    # ================================= #
    # Date : February 14, 2018
    # Created By : Benjamin Nelligan
    # Description : initializes a qr with blank contents. Must fill data with methods
    # Last Modified : February 14, 2018 BEN (Added logging)
    # ================================= #
    def __init__(self, content, width=None, height=None, trigger_method=None, color=None, contrast=None,
                 brightness=None, exposure=None):
        # Initially I set all of the attributes to null because I want the attributes to be coded in. .fill_data()
        # handles instantiating the attributes
        super(QR, self).__init__()
        self.content = content
        self.width = width
        self.height = height
        self.trigger_method = trigger_method
        self.color = color
        self.contrast = contrast
        self.brightness = brightness
        self.exposure = exposure
        self.status = '---- READY ----'
        if len(self.content) != 0:
            dalsa_qr_log.info('Creating QR object with Content: %s', self.content)
        else:
            self.status = '---- ERROR ----'
            dalsa_qr_log.error('Created QR with blank content: %s', self.status)
        # Will serialize itself once created

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : return content
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def get_content(self):
        if self.content is None:
            dalsa_qr_log.error('QR lacks content, cant getContent')
            self.status = '--- ERROR ----'
        return self.content

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : sets the content
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def set_content(self, content):
        if content is not None:
            dalsa_qr_log.info('Setting content of QR: %s', content)
            self.content = content
        else:
            dalsa_qr_log.error('Contents provided are None, Setting contents to: %s', content)
            self.content = content

    # ================================= #
    # Date : November 20, 2018
    # Created By : Benjamin Nelligan
    # Description : Sets the Version
    # Last Modified : February 14, 2018 BEN (added Logging)
    # ================================= #
    def set_dimension(self, width=None, height=None):
        # Allowing to set either width or height. Dont need to provide both to method
        if width is None:
            self.height = height
            dalsa_qr_log.info('Setting height %s', height)
        if height is None:
            self.width = width
            dalsa_qr_log.info('Setting Width: %s', width)
        if width or height is not None:
            self.width = width
            self.height = height
            dalsa_qr_log.error('Width or Height provided is None, Setting Width: %s Height: %s', width, height)

    # ================================= #
    # Date : November 20, 2018
    # Name : getVersion
    # Created By : Benjamin Nelligan
    # Description : gets the Version
    # # Last Modified : February 14, 2018 BEN
    # ================================= #
    def get_dimension(self):
        if self.width or self.height is None:
            dalsa_qr_log.error('Width: %s or Height: %s is None', self.width, self.height)
        dalsa_qr_log.info('Returning Dimensions: %s %s', self.width, self.height)
        return self.width, self.height

    # ================================= #
    # Date : November 20, 2018
    # Name : setError
    # Created By : Benjamin Nelligan
    # Description : Set the Error Level
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def set_trigger_method(self, trigger_method):
        if self.trigger_method is None:
            dalsa_qr_log.error('Trigger Method is None: %s', self.trigger_method)
        self.trigger_method = trigger_method

    # ================================= #
    # Date : November 20, 2018
    # Name : getError
    # Created By : Benjamin Nelligan
    # Description :gets the Error Level
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def get_trigger_method(self):
        if self.trigger_method is None:
            dalsa_qr_log.error('Trigger Method is None: %s', self.trigger_method)
        else:
            dalsa_qr_log.info('Setting Trigger Method to: %s', self.trigger_method)
        return self.trigger_method

    # ================================= #
    # Date : November 20, 2018
    # Name : setEncoding
    # Created By : Benjamin Nelligan
    # Description : sets the encoding
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def set_color(self, color):
        if color is None:
            dalsa_qr_log.error('Setting Color to None: %s', color)
            self.color = color
        else:
            dalsa_qr_log.info('Setting Version to: %s', color)
            self.color = color

    # ================================= #
    # Date : November 20, 2018
    # Name : get_color
    # Created By : Benjamin Nelligan
    # Description : gets the color
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def get_color(self):
        if self.color is None:
            dalsa_qr_log.error('Color is None: %s', self.color)
        dalsa_qr_log.info('Color: %s', self.color)
        return self.color

    # ================================= #
    # Date : November 20, 2018
    # Name : get_color
    # Created By : Benjamin Nelligan
    # Description : gets the color
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def set_brightness(self, brightness):
        if brightness is None:
            dalsa_qr_log.error('Brightness provided is None')
        self.brightness = brightness

    # ================================= #
    # Date : November 20, 2018
    # Name : get_color
    # Created By : Benjamin Nelligan
    # Description : gets the color
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def get_brightness(self):
        dalsa_qr_log.info('Brightness: %s', self.brightness)
        return self.brightness

    # ================================= #
    # Date : November 20, 2018
    # Name : set_contrast
    # Created By : Benjamin Nelligan
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def set_contrast(self, contrast):
        if contrast is None:
            dalsa_qr_log.error('Contrast provided is None')
        self.contrast = contrast

    # ================================= #
    # Date : November 20, 2018
    # Name : get_contrast
    # Created By : Benjamin Nelligan
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def get_contrast(self):
        dalsa_qr_log.info('Contrast: %s', self.contrast)
        return self.contrast

    # ================================= #
    # Date : November 20, 2018
    # Name : get_exposure
    # Created By : Benjamin Nelligan
    # Description : gets the exposure time(milliseconds)
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def set_exposure(self, exposure):
        if exposure is None:
            dalsa_qr_log.error('Exposure provided is None')
        self.exposure = exposure

    # ================================= #
    # Date : November 20, 2018
    # Name : fill_data
    # Created By : Benjamin Nelligan
    # Description : This method will parse a line of a csv and place it into the attributes of the QR.
    # 0:content 1:width 2:heigth 3:trigger_method 4:color 5:brightness 6:contrast 7:exposure
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    @staticmethod
    def fill_data_from_csv():
        # Add logging data
        dalsa_qr_log.info('---- Opening file : %s', test_file)
        dalsa_qr_log.info('---- Assigning Attributes from CSV to QR')
        with open(test_file) as f:
            # record_count = sum(1 for row in f)
            csv_data = csv.reader(f)  # data in using csv reader
            # Will cycle through whole file and make barcodes for each
            for row in csv_data:
                dalsa_qr_log.info('%s RECORDS FOUND')
                content = row[0]
                dalsa_qr_log.info('Content: %s', content)
                width = row[1]
                dalsa_qr_log.info('Width: %s', width)
                height = row[2]
                dalsa_qr_log.info('Height: %s', height)
                trigger_method = row[3]
                dalsa_qr_log.info('Trigger Method: %s', trigger_method)
                color = row[4]
                dalsa_qr_log.info('Color: %s', color)
                brightness = row[4]
                dalsa_qr_log.info('Brightness: %s', brightness)
                contrast = row[5]
                dalsa_qr_log.info('Contrast: %s', contrast)
                exposure = row[6]
                temp_qr = QR(content, width, height, trigger_method, color, brightness, contrast, exposure)
                if temp_qr.content is not None:
                    dalsa_qr_log.info('Returning QR to Barcode:  %s', temp_qr)
                else:
                    dalsa_qr_log.error('Qr has no Content: %s', temp_qr)
                return temp_qr
            f.close()
        dalsa_qr_log.warning('QR info CSV file not found here: %s', str(os.getcwd()))

    # ================================= #
    # Date : November 20, 2018
    # Name : fill_data
    # Created By : Benjamin Nelligan
    # Description : This method will serialize the data to be sent through tcp. Using cPickle/ could use json
    # Last Modified : February 14, 2018 BEN
    # ================================= #
    def __str__(self):
        json_str = 'QR Content: ' + str(self.content)
        try:
            json_str = json.dumps(json_str)
        except (ValueError, TypeError) as e:
            dalsa_qr_log.error('Error while serializing: %s', e)
        return json_str
