# reticle-sim - Final Report Release (2019-05-01)

## Overview
A reticle handler simulation package developed for 2018-2019 engineering senior design class.

### What it can do:
- Provides two separate executable packages which can communicate over TCP/IP
- Demo can send an arbitrary camera command string from devtester to camserver, and camserver will return a response.
  - Commands enabled: ReadBarcode(), isBarcodeReady(), GetBarcode(), GetVersion(), GetASMLVersion
- Demo can send an hinted QR string from devtester to camsim, and camsim will return a response similarly to Dalsa camera.
- All interactions from both client and server are logged locally.

### What it can't do/Remaining priorities:
- Simulator can only listen for hint commands OR camera commands, not both simultaneously. Listens in logical order: QR hint, then commands (this does *NOT* mirror camera behavior, so fixing it would be priority)
    - Task: Improve this to allow simultaneous listening on multiple ports/interfaces.
- Simulator only accepts a limited set of commands and error types. These are documented below and can be extended later
- devtester package does not compare any results other than QR code. This may or may not be a priority for future development
- Needs more robust error handling


### Notes:
There are some packages that are not used at all in this demo, which are included in-case they might be useful for future development.
Notably:
- reticle-sim/Dalsa_Sim/Test/Dalsa_driver
- dalsasim/serve4ever


## Usage
There are two packages included in this repo.
To run from command line, you must have Python 2.7 installed.
Clone or download source code from github.

## Running In the Correct Order
- Server must be manually set to listen for a command
- Order of execution is crucial:
    1. Start CamSim
        - Start camsim:
            - Navigate into the folder that contains the project folder (ie `cd \Dev\projects\reticle-sim`). Then run:
                ```
                python dalsasim
                ```
        - Enter __listen__ to start camera simulator server
        - Server will now wait and listen for socket connection from client...
        - **Expects a hint first, then any number of camera commands**
    2. Start DevTester
        - In a new terminal window/cmd prompt, Start DevTester:
            - Navigate into the folder that contains the project folder (ie `cd \Dev\projects\reticle-sim`). Then run:
                ```
                python devtester
                ```
        - First, send a hint: enter __sendhint__ command
        - Then, send a command by typing __sendcmd__
            - Can submit command as argument: ex: sendcmd eval getBarcode()
        - Check both windows to determine if the command was sent successfully
    4. Exit
        - Enter __exit__ in each app or use CTRL + C to force quit.

## Hinting API v1
This prototype supports the following API.
```json
{
  "test-id": "(int) Manually entered test ID",
  "qr": "(string) Barcode ID value",
  "weather-cond": "(string) good/bad",
  "no-response": "(boolean) true/false",
  "communication-err": "(boolean) true/false"
}
```


| Hint Key          | Purpose                                             | Acceptable Values     | Default Value |
|-------------------|-----------------------------------------------------|-----------------------|---------------|
| test-id           | ID number for the current test, used in logging     | free: alphanumeric    | 1             |
| qr                | Barcode value to store, for camera to "scan"        | free: alphanumeric    | None          |
| weather-cond      | Hint whether test conditions should be good or bad  | fixed: good OR bad    | good          |
| err-no-response   | Trigger an error causing no response from cam       | fixed: True OR False  | False         |
| err-communication | Trigger an error causing socket to close on cam     | fixed: True OR False  | False         |


## Camera Commands Implemented

| Cam Command       | Purpose                                                                                 | Return |
|-------------------|-----------------------------------------------------------------------------------------|--------|
| ReadBarcode()     | Simulate the start of barcode reading process. Return 0 (always)                        | 0      |
| IsBarcodeReady()  | Check if a barcode value has successfully been "scanned." Return: 1 if True, 0 if False |        |
| GetBarcode()      | Return scanned barcode value (as alphanumeric string), if any. If none, return 0        |        |
| GetVersion()      | Return firmware version of simulated camera                                             | 1801   |
| GetASMLVersion    | Return version simulated solution file script                                           | 1      |


## Credits
### Team Members:
- Evan Gorman
- Ben Nelligan
- Brendan Dunne
- Matt Williges

### FU Faculty Advisor:
- Dr. Adrian Rusu

### ASML Industry Sponsor Representatives:
- Steve Lindeberg
- Rafael Ottmann
- Michael O’Neill
- Kishore Ranjan
