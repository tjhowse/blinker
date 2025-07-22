#!/usr/bin/python3

# This program accepts a string as its first argument.
# It converts the sting from 8-bit ASCII to 6-bit by
# subtracting 32, then discarding the two MSBs.
# It prints the result in one-byte hexadecimal format.
# It compacts the bits together so there is no padding between characters.
# I.E.
# "A.B." becomes:
# 100001 001110 100010 001110
# 10000100 11101000 10001110
# 84E88E
# 0x84, 0xE8, 0x8E


def convert_to_6bit_packed_string(input_string) -> str:
    packed_bits = []
    for char in input_string:
        value = ord(char) - 32
        if value < 0 or value > 63:
            raise ValueError(f"Character '{char}' is out of range for 6-bit encoding.")
        packed_bits = [f"{value:06b}"] + packed_bits
    # Join all the packed bits and convert to hex
    packed_bits_str = ''.join(packed_bits)
    # Pad the packed bits to make sure its length is a multiple of 8
    while len(packed_bits_str) % 8 != 0:
        packed_bits_str += '0'
    # Reverse the order to ensure the bits are packed correctly
    # print(f"Padded packed bits: {packed_bits_str}")
    # packed_bits_str = packed_bits_str[::-1]
    # Split into chunks of 8 bits
    hex_output = []
    while packed_bits_str:
        # Take the last 8 bits
        bits = packed_bits_str[-8:]
        # print(bits)
        packed_bits_str = packed_bits_str[:-8]
        # Convert to integer and then to hex
        hex_output.append(f"0x{int(bits, 2):02x}, ")
    # for i in range(len(packed_bits_str), 0, -8):
    #     byte = packed_bits_str[i:i-8]
    #     hex_output.append(f"0x{int(byte, 2):02x}, ")
    return ''.join(hex_output)[:-2]

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 convert_to_6bit.py <input_string>")
        sys.exit(1)

    input_string = sys.argv[1]
    if len(input_string) > 758:
        print("Error: Input string is too long. Maximum length is 634 characters.")
        sys.exit(1)
    try:
        output = convert_to_6bit_packed_string(input_string.upper())
        print(f"const uint8_t message[] = {{{output}}};")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)