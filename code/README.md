# Code

This directory contains the code for generating the morse code
sequences and the microcontroller

## Generation

Run `generate_morse.py "<message>"` to write the byte sequence for that text to `sequence.h`. This is included into the C program that runs on the attiny10.

## Compiling

This depends on the attiny10core detailed here: https://github.com/technoblogy/attiny10core

## Arduino IDE

I have a few versions of the arduino IDE installed. It looks like only 1.8.13 works currently. The newer one might be convinced to work, but needs the attiny10core package installed, probably.

## Flashing

I used a USBasp. I used zadig to install the libusbK v3.1.0.0 driver. I had to flash the newer 2011 firmware to the USBasp and install the low-speed flashing jumper connection. There are a million different disagreeing guides for doing this, but this is what worked for me. By default the arduino IDE hides the detailed output from avrdude, and it misinterprets the return code. This means your code is successfully flashed to the uc but the IDE reports otherwise. In the preferences menu you can enable full output from compilation and upload.

Later on, when flashing the first of the v1.1 boards, the USBasp was not working properly. I started Zadig and it did not show up in the device list. I had to enable "List all devices" in the options menu, Pick USBasp, then select "libusbK (v3.0.7.0)", and reinstall the driver. I have absolutely no idea why libusbK v3.1.0.0 wasn't showing in the list. Also I seem to have have multiple versions of zadig on this PC. They both only show v3.0.7.0.