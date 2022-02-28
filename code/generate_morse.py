#!/usr/bin/python3

# This is the code for generating the byte string that encodes the 1x1 monochrome 10fps video
# that is displayed on the single LED.

# https://morsecode.world/international/timing.html

# // https://morsecode.world/international/timing.html
# // Aim for 12 WPM, I.E. 1 character per second on average.

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
        'z': [dah, dah, dit, dit]
    }
    string = string.lower()
    output = []
    encoded_message = ""
    for char in string:
        if char == ' ':
            to_add = word_end
        elif char not in morse:
            continue
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
    if len(byte_list) > 652:
        raise Exception("Message is probably too long to fit in flash.")
    result = "uint8_t const sequence[] = {"
    for byte in byte_list:
        result += "0x{:02x}, ".format(byte)
        # result += "{:02}, ".format(byte)
    result = result[:-2] + "};"
    return result, message

@click.command()
@click.argument('string')
def main_morse(string):
    with open("blinker/sequence.h", "w") as f:
        array, message = encode_string_to_c_bytes_array(string)
        f.write("// {}\n".format(message))
        f.write(array)

if __name__ == '__main__':
    main_morse()
    # print(encode_string_to_c_bytes_array("Hello World"))
    # print(encode_string_to_c_bytes_array("ss s"))

