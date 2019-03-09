# reticle-sim - Sprint 3 Demo (2019-03-08)

## Overview
A reticle handler simulation package being developed for 2018-2019 engineering senior design class.

This very limited demo version was put together specifically to demonstrate our progress on a few main points that will be essential going forward:
 - TCP/IP communication
 - Logging
 - Overall architecture design

 This build does __not__ yet satisfy our requirements as laid out for the Second Prototype, but is meant to show progress thus far.

### What it can do:
- Provides two separate executable packages which can communicate over TCP/IP
- Demo can send an arbitrary camera command string from devtester to camserver, and camserver will return a response.
- Demo can send an arbitrary hint command string from devtester to camserver, and camserver and return a response.
- All interactions from both client and server are logged locally.

### What it can't do/Remaining priorities:
- Each transmission of a command or hint is treated separately. Will be automated in near future.
    - Task: Set Dalsa Simulator to listen continuously once started, as real camera does
- Commands do not actually trigger any processing, they are just transmitted and a status is returned, in order to demonstrate functionality.
    - Task: Add functions to parse the commands entered, and return appropriate responses
- Commands are not formatted
    - Task: Along with processing, commands should return exactly as camera does
- devtester package does not compare any results, since commands are not actually being handled yet.
    - Task: Add logic to compare expect results with actual returned result
- Needs more robust error handling
    - Task: Improve this
- Not able to set the hostname to allow tester to reach out to the camserver on a separate host
    - Task: A hostname function needs to be written

### Notes:
There are some packages that are not used at all in this demo, as well as some code we have yet to integrate.
Notably:
- reticle-sim/Dalsa_Sim/Test/Dalsa_driver
- dalsasim/serve4ever
- dalsasim/camsim/barcode

## Usage
There are two packages included in this repo.
To run from command line, must have Python 2.7 installed.
Clone or download source code from github.

## Running In the Correct Order
- Server must be manually set to listen for a command
    - This will be changed soon, keeping it simple as we worked to debug things
- Order of execution is crucial:
    1. Start CamSim
        - Start camsim (see below)
        - Enter __start__ command to begin simulator
        - Enter __listen__ to start camera simulator server ()
        - Server will now wait and listen for socket connection from client...
    2. Start Tester
        - In a new terminal window/cmd prompt, Start DevTester
        - Send a command by typing sendcmd followed by command string.
            - ex: sendcmd getBarcode()
        - Check both windows to determine if the command was sent successfully
    3. Hint Server
        - The same process can be followed to send strings via the hinting interface, which is running through a separate port.
            - On CamSim: Enter __hintlisten__ to listen on hint port
            - On DevTester: Enter __sendhint__ followed by string to send
                - ex: sendhint qr = nklr346mklmdf
    4. Exit
        - Enter __exit__ in each app or use CTRL + C to force quit.

### Camera Simulator (camsim)
Navigate into the folder that contains the project folder (ie `cd \Dev\projects\reticle-sim`). Then run:
```
python camsim
```

### Development Tester (devtester)
Navigate into the folder that contains the project folder (ie `cd \Dev\projects\reticle-sim\Test`). Then run:
```
python devtester
```

## Hinting API v1
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
