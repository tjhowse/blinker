# Code

This directory contains the code for generating the morse code
sequences and the microcontroller

## Generation

Run `generate_morse.py "<message>"` to write the byte sequence for that text to `sequence.h`. This is included into the C program that runs on the attiny10.

## Compiling

This depends on the attiny10core detailed here: https://github.com/technoblogy/attiny10core

## Flashing

I used a USBasp. I used zadig to install the libusbK v3.1.0.0 driver. I had to flash the newer 2011 firmware to the USBasp and install the low-speed flashing jumper connection. There are a million different disagreeing guides for doing this, but this is what worked for me. By default the arduino IDE hides the detailed output from avrdude, and it misinterprets the return code. This means your code is successfully flashed to the uc but the IDE reports otherwise. In the preferences menu you can enable full output from compilation and upload.