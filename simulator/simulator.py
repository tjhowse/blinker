#! /usr/bin/env python3

import time
import pygame

# font from https://github.com/adafruit/Adafruit-GFX-Library/blob/master/Fonts/TomThumb.h
# https://robey.lag.net/2010/01/23/tiny-monospace-font.html
# 5 high, 3 wide
CHAR_BITMAPS = {
    'A': [0x57, 0xDA],
    'B': [0xD7, 0x5C],
    'C': [0x72, 0x46],
    'D': [0xD6, 0xDC],
    'E': [0xF3, 0xCE],
    'F': [0xF3, 0xC8],
    'G': [0x73, 0xD6],
    'H': [0xB7, 0xDA],
    'I': [0xE9, 0x2E],
    'J': [0x24, 0xD4],
    'K': [0xB7, 0x5A],
    'L': [0x92, 0x4E],
    'M': [0xBF, 0xDA],
    'N': [0xBF, 0xFA],
    'O': [0x56, 0xD4],
    'P': [0xD7, 0x48],
    'Q': [0x56, 0xF6],
    'R': [0xD7, 0xEA],
    'S': [0x71, 0x1C],
    'T': [0xE9, 0x24],
    'U': [0xB6, 0xD6],
    'V': [0xB6, 0xA4],
    'W': [0xB7, 0xFA],
    'X': [0xB5, 0x5A],
    'Y': [0xB5, 0x24],
    'Z': [0xE5, 0x4E],
}

def draw_char(surface: pygame.Surface, char: str, ix: int, iy: int):
    """
    Draws a character on the given surface at the specified position.
    Each character is represented as a list of bytes, each byte is a column (5 bits high, LSB is top).
    """
    if char not in CHAR_BITMAPS:
        raise ValueError(f"Character '{char}' not found in bitmap definitions.")

    bitmap = CHAR_BITMAPS[char]
    joined = bitmap[1] + (bitmap[0] << 8)
    for y in range(5):
        for x in range(3):
            if (joined >> (15 - (y * 3 + x))) & 1:
                pygame.draw.rect(surface, (255, 255, 255), (ix + x * 8, iy + y * 8, 8, 8))

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
        # print(capital_letters[index])
        draw_char(screen, capital_letters[index], 50, 50)  # Draw current letter at position (50, 50)
        pygame.display.flip()  # Update the display
        time.sleep(1)
        index = (index + 1) % len(capital_letters)  # Move to the next letter

    print(" Exiting the simulator...")
    pygame.quit()

if __name__ == "__main__":
    main()