#pragma once
// #include <Adafruit_GFX.h>

/**
** The original 3x5 font is licensed under the 3-clause BSD license:
**
** Copyright 1999 Brian J. Swetland
** Copyright 1999 Vassilii Khachaturov
** Portions (of vt100.c/vt100.h) copyright Dan Marks
**
** All rights reserved.
**
** Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions
** are met:
** 1. Redistributions of source code must retain the above copyright
**    notice, this list of conditions, and the following disclaimer.
** 2. Redistributions in binary form must reproduce the above copyright
**    notice, this list of conditions, and the following disclaimer in the
**    documentation and/or other materials provided with the distribution.
** 3. The name of the authors may not be used to endorse or promote products
**    derived from this software without specific prior written permission.
**
** THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
** IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
** OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
** IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
** INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
** NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
** THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
**
** Modifications to Tom Thumb for improved readability are from Robey Pointer,
** see:
** http://robey.lag.net/2010/01/23/tiny-monospace-font.html
**
** The original author does not have any objection to relicensing of Robey
** Pointer's modifications (in this file) in a more permissive license.  See
** the discussion at the above blog, and also here:
** http://opengameart.org/forumtopic/how-to-submit-art-using-the-3-clause-bsd-license
**
** Feb 21, 2016: Conversion from Linux BDF --> Adafruit GFX font,
** with the help of this Python script:
** https://gist.github.com/skelliam/322d421f028545f16f6d
** William Skellenger (williamj@skellenger.net)
** Twitter: @skelliam
**
** Jan 09, 2020: Bitmaps now compressed, to fix the bounding box problem,
** because non-compressed the calculated text width were wrong.
** Andreas Merkle (web@blue-andi.de)
*/


const uint8_t TomThumbBitmaps[] PROGMEM = {
    0x00, 0x00,       /* 0x20 space */
    0xE8, 0x00,       /* 0x21 exclam */
    0xB4, 0x00,       /* 0x22 quotedbl */
    0xBE, 0xFA,       /* 0x23 numbersign */
    0x79, 0xE4,       /* 0x24 dollar */
    0x85, 0x42,       /* 0x25 percent */
    0xDB, 0xD6,       /* 0x26 ampersand */
    0xC0, 0x00,       /* 0x27 quotesingle */
    0x6A, 0x40,       /* 0x28 parenleft */
    0x95, 0x80,       /* 0x29 parenright */
    0xAA, 0x80,       /* 0x2A asterisk */
    0x5D, 0x00,       /* 0x2B plus */
    0x60, 0x00,       /* 0x2C comma */
    0xE0, 0x00,       /* 0x2D hyphen */
    0x80, 0x00,       /* 0x2E period */
    0x25, 0x48,       /* 0x2F slash */
    0x76, 0xDC,       /* 0x30 zero */
    0x75, 0x40,       /* 0x31 one */
    0xC5, 0x4E,       /* 0x32 two */
    0xC5, 0x1C,       /* 0x33 three */
    0xB7, 0x92,       /* 0x34 four */
    0xF3, 0x1C,       /* 0x35 five */
    0x73, 0xDE,       /* 0x36 six */
    0xE5, 0x48,       /* 0x37 seven */
    0xF7, 0xDE,       /* 0x38 eight */
    0xF7, 0x9C,       /* 0x39 nine */
    0xA0, 0x00,       /* 0x3A colon */
    0x46, 0x00,       /* 0x3B semicolon */
    0x2A, 0x22,       /* 0x3C less */
    0xE3, 0x80,       /* 0x3D equal */
    0x88, 0xA8,       /* 0x3E greater */
    0xE5, 0x04,       /* 0x3F question */
    0x57, 0xC6,       /* 0x40 at */
    0x57, 0xDA,       /* 0x41 A */
    0xD7, 0x5C,       /* 0x42 B */
    0x72, 0x46,       /* 0x43 C */
    0xD6, 0xDC,       /* 0x44 D */
    0xF3, 0xCE,       /* 0x45 E */
    0xF3, 0xC8,       /* 0x46 F */
    0x73, 0xD6,       /* 0x47 G */
    0xB7, 0xDA,       /* 0x48 H */
    0xE9, 0x2E,       /* 0x49 I */
    0x24, 0xD4,       /* 0x4A J */
    0xB7, 0x5A,       /* 0x4B K */
    0x92, 0x4E,       /* 0x4C L */
    0xBF, 0xDA,       /* 0x4D M */
    0xBF, 0xFA,       /* 0x4E N */
    0x56, 0xD4,       /* 0x4F O */
    0xD7, 0x48,       /* 0x50 P */
    0x56, 0xF6,       /* 0x51 Q */
    0xD7, 0xEA,       /* 0x52 R */
    0x71, 0x1C,       /* 0x53 S */
    0xE9, 0x24,       /* 0x54 T */
    0xB6, 0xD6,       /* 0x55 U */
    0xB6, 0xA4,       /* 0x56 V */
    0xB7, 0xFA,       /* 0x57 W */
    0xB5, 0x5A,       /* 0x58 X */
    0xB5, 0x24,       /* 0x59 Y */
    0xE5, 0x4E,       /* 0x5A Z */
};
