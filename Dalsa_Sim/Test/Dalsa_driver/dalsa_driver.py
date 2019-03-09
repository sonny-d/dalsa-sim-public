import datetime
import time
from Dalsa_Sim.dalsasim.serve4ever import serve_4_ever


class DummyDriver(object):
    """
    A very basic placeholder for the drivers to be tested.
    Restructured for Ben 2.0 by Evan Gorman 2/15/19
    """

    driver_version = "Dummy 0.001"

    def __init__(self, server):
        print("Initializing reticle handler drivers version: " + self.driver_version)
        self.cam_server = server
        self.sip = ""
        print"Driver loaded."

    def ping_sim(self):
        # ping and have Serve4ever on forever looking for ping
        serve_4_ever.connect(5021)

    def file_input(self, file):
         # will take in the file the user inputs locally
        self.file = file
        import(file)


    def gen_file(self, file):
      # will call new class in Dalsa_Sim called file_generator
        self.file = file
        export(file)

    def reboot(self):
        serve_4_ever.close(5021)
        serve_4_ever.close(5023)
        serve_4_ever.close(5024)
        serve_4_ever.connect(5021)
        serve_4_ever.connect(5023)
        serve_4_ever.connect(5024)

    def post_image_process(self):
        # post image processing
        # first barcode valid
        if (Barcode1.Result != 0):
            # second barcode valid
            if (barcode2.Result != 0)
                ReticleID = Barcode1 + Barcode2
                BarcodeReadyFlag = 1
                # second barcode not valid
            else:
                ReticleID = Barcode1
                BarcodeReadyFlag = 1
            endif:
            # first barcode not valid
        else:
            ReticleID = 'N/A'
            BarcodeReadyFlag = 1
        endif:

    def solution_initialize(self):
        # Solution file initialization
        # Set version to current value
        ASMLVersion = 01

        # Set barcode ready flag to 0
        BarcodeReadyFlag = 0

        # Set reticle ID to blank string
        ReticleID = ""

        # Set trigger mode to SW
        TriggerSource(3)

    def ReadBarcode(self):
        BarcodeReadyFlag = 0
        trigger()

    def GetBarcode(self):

        return (ReticleID)

    def GetASMLVersion(self):

        return (ASMLVersion)

    def BarcodeReady(self):

        return (BarcodeReadyFlag)

    def GetImage(self):
        ftp = "ftp://ftp." + machine_id + ":ftp@" + machine_addr + "/usr/asm/atl." + machine_id + "/BC/1D_LDPT_image.bmp"
        WriteImageTools(ftp, 0)


        # old stuff below still using some

    def start(self):
        """
        Begin the reticle handling process.
        :return: RunResult object representing the result of reticle handling process.
        """

        # Non-camera Simulation here
        print("\nDriver: Driver is doing drivers stuff...")
        print("Stage 1: Positioning reticle...")
        time.sleep(3)  # Pause for 3 sec to simulate positioning
        print("Stage 1: Complete")
        # Camera simulation begins here
        print("Stage 2: Scanning reticle QR code...")
        print("Driver: Connecting to Camera Server")
        # Get the IP address from the cam server
        self.sip = self.cam_server.get_ip()
        # Moved below logic to scan_barcode
        # print "Sending commands to the camera:"
        # print "Command 1: Check camera firmware version?"
        # rt = self.cam_server.process_cmd("GetVersion()")
        # print "Command 1: Result: " + rt
        # print "Command 2: Is barcode ready?"
        # rt = self.cam_server.process_cmd("IsBarcodeReady()")
        # print "Command 2: Result: " + rt
        # Scan the reticle barcode
        print("Scanning QR barcode...")
        result = self.scan_barcode()
        # Verify the result
        print("Verifying QR barcode result...")
        test = self.verify_barcode(result)
        return test

    def scan_barcode(self):
        print(\n
        "Sending commands to the camera:")
        print("Command 1: Check camera firmware version.")
        rt = self.cam_server.process_cmd("GetVersion()")
        print("Command 1: Result: " + rt)

        print("Command 2: Check if barcode is ready.")
        rt = self.cam_server.process_cmd("IsBarcodeReady()")
        print("Command 2: Result: " + str(rt))

        # Catch condition if barcode not ready
        if rt is True:
            print("Command 3: Read barcode.")
            self.cam_server.process_cmd("ReadBarcode()")
            # TODO: print a result?

            # print "End test early"
            # return "9999999999"
            # #return RunResult("0", "0", "0", "0")

            print("Command 4: Get Barcode.")
            barcode = self.cam_server.process_cmd("GetBarcode()")
            # TODO: print a result?
            time.sleep(3)
            print(str(barcode))
            # Return the barcode string
            return barcode
        else:
            # TODO: Could be barcode not ready, or some other. Handle both in future.
            print("Barcode not ready, unable to continue.")
            return None  # This should probably return a bad RunResult instead

    def verify_barcode(self, result):
        """
        Simulates the built in error checking of the driver. Will check a couple basic params for now.
        :param result: String of a scanned QR barcode
        :return: RunResult object
        """

        if len(result) > 8:
            status = True
        else:
            status = False
        print("Barcode verify complete")
        return RunResult(result, status, self.driver_version, self.sip)


class RunResult(object):
    """
    call logging server
    """

    def __init__(self, qr, status, driver_version, sip):
        print("")
        self.qr = qr
        self.status = status
        self.driver_version = driver_version
        self.sip = sip
        runtime = str(datetime.datetime.now())
        print(qr + str(status) + runtime + driver_version + sip)