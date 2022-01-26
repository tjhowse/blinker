#!/usr/bin/python3

# This is the code for generating the byte string that encodes the 1x1 monochrome 10fps video
# that is displayed on the single LED.

# https://morsecode.world/international/timing.html

# // https://morsecode.world/international/timing.html
# // Aim for 12 WPM, I.E. 1 character per second on average.
# // uint8_t const unit = 10; // Clock cycles? Something? Dunno.
# // uint8_t const dit_length = 1*unit;
# // uint8_t const dah_length = 3*unit;
# // uint8_t const intra_character_gap = 1*unit;
# // uint8_t const inter_character_gap = 3*unit;
# // uint8_t const word_gap = 7*unit;

msg = "hello from the howse family travis michelle alex and sam"
msg2 = "paris "*120
# msg = "hello hello"
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

    output = []
    for char in string:
        if char == ' ':
            to_add = word_end
        else:
            to_add = []
            for bit in morse[char]:
                to_add.extend(bit)
            to_add.extend(char_end)
        for bit in to_add:
            output += [bit]


    return output

def bit_list_to_bytes(bit_list):
    output = [0]
    count = 0
    for bit in bit_list:
        output[-1] |= (bit << (7-count))
        count += 1
        if count == 8:
            count = 0
            output.append(0)
    return output



test = method1(msg)
print(msg)
print("bytes: {}".format(len(test)/8))
print(bit_list_to_bytes(test))
test = method1(msg2)
print(len(test))

final = bit_list_to_bytes(test)

print(final)

counter = 0
