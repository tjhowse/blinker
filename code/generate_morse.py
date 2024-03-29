#!/usr/bin/python3

# This is the code for generating the byte string that encodes the 1x1 monochrome 10fps video
# that is displayed on the single LED.

# https://morsecode.world/international/timing.html

# // https://morsecode.world/international/timing.html
# // Aim for 12 WPM, I.E. 1 character per second on average.

import sys
import click

flash_bytes = 1024
program_bytes = 200
sequence_bytes = flash_bytes-program_bytes
wpm = 12
cpm = 12*5 # 5 characters per word, typically.
cps = cpm/60 # characters per second

def method1(string):
    # First stab: Encode the LED on/off state in a bit array that we step through at a rate.
    dit = [1,0]
    dah = [1,1,1,0]
    char_end = [0]*2 # Nominally 3, but since each dit or dah ends with an off period, we can leave one off.
    word_end = [0]*4 # Nominally 7, but we subtract the off period from the char and dit/dah.

    morse = {
        'a': [dit, dah],
        'b': [dah, dit, dit, dit],
        'c': [dah, dit, dah, dit],
        'd': [dah, dit, dit],
        'e': [dit],
        'f': [dit, dit, dah, dit],
        'g': [dah, dah, dit],
        'h': [dit, dit, dit, dit],
        'i': [dit, dit],
        'j': [dit, dah, dah, dah],
        'k': [dah, dit, dah],
        'l': [dit, dah, dit, dit],
        'm': [dah, dah],
        'n': [dah, dit],
        'o': [dah, dah, dah],
        'p': [dit, dah, dah, dit],
        'q': [dah, dah, dit, dah],
        'r': [dit, dah, dit],
        's': [dit, dit, dit],
        't': [dah],
        'u': [dit, dit, dah],
        'v': [dit, dit, dit, dah],
        'w': [dit, dah, dah],
        'x': [dah, dit, dit, dah],
        'y': [dah, dit, dah, dah],
        'z': [dah, dah, dit, dit],
        '1': [dit, dah, dah, dah, dah],
        '2': [dit, dit, dah, dah, dah],
        '3': [dit, dit, dit, dah, dah],
        '4': [dit, dit, dit, dit, dah],
        '5': [dit, dit, dit, dit, dit],
        '6': [dah, dit, dit, dit, dit],
        '7': [dah, dah, dit, dit, dit],
        '8': [dah, dah, dah, dit, dit],
        '9': [dah, dah, dah, dah, dit],
        '0': [dah, dah, dah, dah, dah],
        # Fun story: I'm using copilot to write this, and it started filling out 0-9 by itself
        # so I let it run with it. It then started doing the below which I'm reasonably
        # sure it invented from whole cloth.
        # '.': [dit, dah, dah, dah, dah, dah],
        # ',': [dah, dah, dah, dah, dah, dit],
        # '?': [dit, dit, dah, dah, dit, dit],
        # '\'': [dit, dit, dah, dah, dah, dah],
        # '!': [dit, dit, dah, dah, dah, dah, dah],
        # '/': [dah, dit, dit, dah, dah],
        # '(': [dah, dit, dah, dit, dah],
        # ')': [dah, dit, dah, dit, dah, dah],
        # '&': [dit, dit, dah, dit, dah, dit],
        # ':': [dah, dah, dah, dah, dah, dah, dah],
        # ';': [dah, dah, dah, dah, dah, dah, dit],
        # '=': [dah, dah, dah, dah, dah, dah, dah, dah],
        # '+': [dah, dah, dah, dah, dah, dah, dah, dah, dah],
        # '-': [dah, dah, dah, dah, dah, dah, dah, dah, dah, dah],
        # '_': [dah, dah, dah, dah, dah, dah, dah, dah, dah, dah, dah],
        # '"': [dit, dit, dah, dah, dah, dah, dah, dah, dah, dah, dah],
        # '$': [dah, dit, dah, dah, dah, dah, dah, dah, dah, dit, dah],
        # '@': [dah, dit, dah, dah, dah, dah, dah, dah, dah, dah, dah, dah],
    }
    string = string.lower()
    output = []
    encoded_message = ""
    for char in string:
        if char == ' ' or char not in morse:
            to_add = word_end
            encoded_message += " "
        else:
            to_add = []
            for bit in morse[char]:
                to_add.extend(bit)
            to_add.extend(char_end)
            encoded_message += char
        for bit in to_add:
            output += [bit]


    return output, encoded_message

def bit_list_to_bytes(bit_list):
    output = [0]
    count = 0
    for bit in bit_list:
        output[-1] |= (bit << count)
        count += 1
        if count == 8:
            count = 0
            output.append(0)
    return output

def encode_string_to_c_bytes_array(string):
    bit_list, message = method1(string)
    byte_list = bit_list_to_bytes(bit_list)
    print(f"{len(byte_list)/652*100:.2f}% of flash used.")
    if len(byte_list) > 652:
        raise Exception("Message is probably too long to fit in flash.")
    result = "uint8_t const sequence[] = {"
    for byte in byte_list:
        result += "0x{:02x}, ".format(byte)
        # result += "{:02}, ".format(byte)
    result = result[:-2] + "};"
    return result, message

@click.command()
@click.argument('string', default="")
def main_morse(string):
    if string == "":
        # Read from stdin instead
        string = sys.stdin.read()
    array, message = encode_string_to_c_bytes_array(string)
    with open("blinker/sequence.h", "w") as f:
        f.write("// {}\n".format(message))
        f.write(array)

if __name__ == '__main__':
    main_morse()
    # print(encode_string_to_c_bytes_array("Hello World"))
    # print(encode_string_to_c_bytes_array("ss s"))

