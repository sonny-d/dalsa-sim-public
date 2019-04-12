# reticle-sim - Sprint 4 Demo (2019-04-12)

## Overview
A reticle handler simulation package being developed for 2018-2019 engineering senior design class.

This demo version was put together specifically to demonstrate our progress on a few main points that will be essential going forward:
 - TCP/IP communication
 - Simulating camera's command handling/formatting
 - Logging
 - Overall architecture design

 This build does __not__ yet satisfy our requirements as laid out for the Second Prototype, but is meant to show progress thus far.

### What it can do:
- Provides two separate executable packages which can communicate over TCP/IP
- Demo can send an arbitrary camera command string from devtester to camserver, and camserver will return a response.
- Demo can send an arbitrary hinted QR string from devtester to camserver, and camserver and return a response.
- All interactions from both client and server are logged locally.

### What it can't do/Remaining priorities:
- Simulator can only listen for hint commands OR camera commands, not both simultaneously
    - Task: Improve this to allow simultaneous listening on multiple ports/interfaces.
- Commands do not actually trigger any processing, they are just transmitted and a status is returned, in order to demonstrate functionality.
    - Task: Add functions to parse the commands entered, and return appropriate responses
- devtester package does not compare any results.
    - Task: Add logic to compare expect results with actual returned result
- Needs more robust error handling
    - Task: Improve this

### Notes:
There are some packages that are not used at all in this demo, as well as some code we have yet to integrate.
Notably:
- reticle-sim/Dalsa_Sim/Test/Dalsa_driver
- dalsasim/serve4ever


## Usage
There are two packages included in this repo.
To run from command line, you must have Python 2.7 installed.
Clone or download source code from github.

## Running In the Correct Order
- Server must be manually set to listen for a command
    - This will be changed soon, keeping it simple as we worked to debug things
- Order of execution is crucial:
    1. Start CamSim
        - Start camsim:
            - Navigate into the folder that contains the project folder (ie `cd \Dev\projects\reticle-sim`). Then run:
                ```
                python dalsasim
                ```
        - Enter __listen__ to start camera simulator server ()
        - Server will now wait and listen for socket connection from client...
        - Expects a hint first, then any number of camera commands
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
This second prototype will support the following API. **Currently only supports test-id and qr**
```json
{
  "test-id": "(int) Sequentially generated test ID",
  "qr": "(string) Barcode ID value",
  "attributes": {
    "weather-cond": "(string) good/bad",
    "error-trigger": {
        "no-response": "(boolean) true/false",
        "communication-err": "(boolean) true/false"
    }
  }
}
```

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
