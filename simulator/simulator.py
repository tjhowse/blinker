#! /usr/bin/env python3

import time
import pygame

# font from https://github.com/adafruit/Adafruit-GFX-Library/blob/master/Fonts/TomThumb.h

# A map of characters to their 5x4 bitmap representations.
# Each character is represented as a 20-bit integer, where each bit corresponds to a pixel
# CHAR_BITMAPS = {
#     'A': 0b00011000001100000110,
#     'B': 0b00011100001100000110,
#     'C': 0b00011000001100000010,
#     'D': 0b00011100001100000110,
#     'E': 0b00011100001100000000,
#     'F': 0b00011100001100000000,
#     'G': 0b00011000001100000110,
#     # Add more characters as needed
# }

CHAR_BITMAPS = {
    ' ': bytearray([0x00]),
    '!': bytearray([0xE8]),
    '"': bytearray([0xB4]),
    '#': bytearray([0xBE, 0xFA]),
    '$': bytearray([0x79, 0xE4]),
    '%': bytearray([0x85, 0x42]),
    '&': bytearray([0xDB, 0xD6]),
    "'": bytearray([0xC0]),
    '(': bytearray([0x6A, 0x40]),
    ')': bytearray([0x95, 0x80]),
    '*': bytearray([0xAA, 0x80]),
    '+': bytearray([0x5D, 0x00]),
    ',': bytearray([0x60]),
    '-': bytearray([0xE0]),
    '.': bytearray([0x80]),
    '/': bytearray([0x25, 0x48]),
    '0': bytearray([0x76, 0xDC]),
    '1': bytearray([0x75, 0x40]),
    '2': bytearray([0xC5, 0x4E]),
    '3': bytearray([0xC5, 0x1C]),
    '4': bytearray([0xB7, 0x92]),
    '5': bytearray([0xF3, 0x1C]),
    '6': bytearray([0x73, 0xDE]),
    '7': bytearray([0xE5, 0x48]),
    '8': bytearray([0xF7, 0xDE]),
    '9': bytearray([0xF7, 0x9C]),
    ':': bytearray([0xA0]),
    ';': bytearray([0x46]),
    '<': bytearray([0x2A, 0x22]),
    '=': bytearray([0xE3, 0x80]),
    '>': bytearray([0x88, 0xA8]),
    '?': bytearray([0xE5, 0x04]),
    '@': bytearray([0x57, 0xC6]),
    'A': bytearray([0x57, 0xDA]),
    'B': bytearray([0xD7, 0x5C]),
    'C': bytearray([0x72, 0x46]),
    'D': bytearray([0xD6, 0xDC]),
    'E': bytearray([0xF3, 0xCE]),
    'F': bytearray([0xF3, 0xC8]),
    'G': bytearray([0x73, 0xD6]),
    'H': bytearray([0xB7, 0xDA]),
    'I': bytearray([0xE9, 0x2E]),
    'J': bytearray([0x24, 0xD4]),
    'K': bytearray([0xB7, 0x5A]),
    'L': bytearray([0x92, 0x4E]),
    'M': bytearray([0xBF, 0xDA]),
    'N': bytearray([0xBF, 0xFA]),
    'O': bytearray([0x56, 0xD4]),
    'P': bytearray([0xD7, 0x48]),
    'Q': bytearray([0x56, 0xF6]),
    'R': bytearray([0xD7, 0xEA]),
    'S': bytearray([0x71, 0x1C]),
    'T': bytearray([0xE9, 0x24]),
    'U': bytearray([0xB6, 0xD6]),
    'V': bytearray([0xB6, 0xA4]),
    'W': bytearray([0xB7, 0xFA]),
    'X': bytearray([0xB5, 0x5A]),
    'Y': bytearray([0xB5, 0x24]),
    'Z': bytearray([0xE5, 0x4E]),
    '[': bytearray([0xF2, 0x4E]),
    '\\': bytearray([0x88, 0x80]),
    ']': bytearray([0xE4, 0x9E]),
    '^': bytearray([0x54]),
    '_': bytearray([0xE0]),
    '`': bytearray([0x90]),
    'a': bytearray([0xCE, 0xF0]),
    'b': bytearray([0x9A, 0xDC]),
    'c': bytearray([0x72, 0x30]),
    'd': bytearray([0x2E, 0xD6]),
    'e': bytearray([0x77, 0x30]),
    'f': bytearray([0x2B, 0xA4]),
    'g': bytearray([0x77, 0x94]),
    'h': bytearray([0x9A, 0xDA]),
    'i': bytearray([0xB8]),
    'j': bytearray([0x20, 0x9A, 0x80]),
    'k': bytearray([0x97, 0x6A]),
    'l': bytearray([0xC9, 0x2E]),
    'm': bytearray([0xFF, 0xD0]),
    'n': bytearray([0xD6, 0xD0]),
    'o': bytearray([0x56, 0xA0]),
    'p': bytearray([0xD6, 0xE8]),
    'q': bytearray([0x76, 0xB2]),
    'r': bytearray([0x72, 0x40]),
    's': bytearray([0x79, 0xE0]),
    't': bytearray([0x5D, 0x26]),
    'u': bytearray([0xB6, 0xB0]),
    'v': bytearray([0xB7, 0xA0]),
    'w': bytearray([0xBF, 0xF0]),
    'x': bytearray([0xA9, 0x50]),
    'y': bytearray([0xB5, 0x94]),
    'z': bytearray([0xEF, 0x70]),
    '{': bytearray([0x6A, 0x26]),
    '|': bytearray([0xD8]),
    '}': bytearray([0xC8, 0xAC]),
    '~': bytearray([0x78]),
}

def draw_char(surface: pygame.Surface, char: str, x: int, y: int):
    """
    Draws a character on the given surface at the specified position.
    Each character is represented as a 5-row, variable-width bitmap.
    """
    if char not in CHAR_BITMAPS:
        raise ValueError(f"Character '{char}' not found in bitmap definitions.")

    bitmap = CHAR_BITMAPS[char]


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Character Bitmap Simulator")
    capital_letters= list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    index = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        screen.fill((0, 0, 0))  # Clear the screen
        print(capital_letters[index])
        draw_char(screen, capital_letters[index], 50, 50)  # Draw current letter at position (50, 50)
        pygame.display.flip()  # Update the display
        time.sleep(0.5)
        index = (index + 1) % len(capital_letters)  # Move to the next letter

    print(" Exiting the simulator...")
    pygame.quit()

if __name__ == "__main__":
    main()