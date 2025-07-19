#!/usr/bin/python3

# This program accepts a string as its first argument.
# It converts the sting from 8-bit ASCII to 6-bit by
# subtracting 46, then discarding the last 2 bits.
# It prints the result in one-byte hexadecimal format.
# It compacts the bits together so there is no padding between characters.
# I.E.
# "A.B." becomes:
# 010011 000000 010100 000000
# 010011000000010100000000
# 4C0500

def convert_to_6bit_packed_string(input_string) -> str:
    packed_bits = []
    for char in input_string:
        if char == ' ':
            packed_bits.append('000000')
        else:
            value = ord(char) - 46
            if value < 0 or value > 63:
                raise ValueError(f"Character '{char}' is out of range for 6-bit encoding.")
            packed_bits.append(f"{value:06b}")
    # Join all the packed bits and convert to hex
    packed_bits_str = ''.join(packed_bits)
    # Split into chunks of 8 bits
    hex_output = []
    for i in range(0, len(packed_bits_str), 8):
        byte = packed_bits_str[i:i+8]
        hex_output.append(f"0x{int(byte, 2):02x}, ")
    return ''.join(hex_output)[:-2]

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 convert_to_6bit.py <input_string>")
        sys.exit(1)

    input_string = sys.argv[1]
    try:
        output = convert_to_6bit_packed_string(input_string.upper())
        print(output)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)