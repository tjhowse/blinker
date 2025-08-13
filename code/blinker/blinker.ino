#define ws2812_port B     // Data port
#define ws2812_pin  2     // Data out pin


#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#include "attiny10_ws2812.h"  // Include the ws2812 library
#include "tomthumb_5x3_font.h" // Include the font header
#include "message.h"

const uint16_t message_len = (sizeof(message)*8)/6;
// Note: These are GRB values.
const cRGB ledOff = {0,0,0};
const cRGB ledOn = {16,16,16};
const cRGB ledRed = {0,16,0};

int main(void)
{

#ifdef __AVR_ATtiny10__
  CCP=0xD8;   // configuration change protection, write signature
  CLKPSR=0;   // set cpu clock prescaler =1 (8Mhz) (attiny 4/5/9/10)

#else
  CLKPR=_BV(CLKPCE);
  CLKPR=0;      // set clock prescaler to 1 (attiny 25/45/85/24/44/84/13/13A)

#endif
  DDRB|=_BV(ws2812_pin);

  while (1) {
    for (uint16_t charIndex = 0; charIndex < message_len; charIndex++) {
      // This henious nonsense looks up the character in the message array.
      // Each character is 6 bits, so we need to read two bytes from the array
      // in case the character straddles a byte boundary.
      uint8_t index = (charIndex*6)/8; // Index of the first byte
      uint8_t shift = (charIndex*6)%8; // Bit shift within the two bytes
      uint8_t c = (((message[index] | message[index+1] << 8) >> shift) & 0x003F) * 2;
      // uint16_t bitmap = (TomThumbBitmaps[c] << 8) | TomThumbBitmaps[c + 1];
      // c = 34*2; // B
      uint16_t bitmap = (TomThumbBitmapsRotated[c] << 8) | TomThumbBitmapsRotated[c + 1];

      for (uint8_t bit = 0; bit < 16; bit++) {
        if ((bitmap >> bit) & 0x1) {
          ws2812_sendarray((uint8_t *)&ledOn, 3); // Send the "on" color
        } else {
          ws2812_sendarray((uint8_t *)&ledOff, 3); // Send the "off" color
        }
      }
      _delay_ms(400);

      // Old style, reading non-rotated bitmaps.
      // uint16_t bitmap = getBitmapForCharacter('B');
      // for (uint8_t column = 2; column <= 2 && column >= 0; column--) {
      //   for (uint8_t row = 4; row <= 4 && row >= 0; row--) {
      //     if ((bitmap >> (15-(column + row*3))) & 0x1) {
      //       ws2812_sendarray((uint8_t *)&ledOn,3);
      //     } else {
      //       // ws2812_sendarray((uint8_t *)&ledOn,3);
      //       ws2812_sendarray((uint8_t *)&ledOff,3);
      //     }
      //   }
      // }
      // _delay_ms(400);

      // Experiment for scrolling text.
      // for (int8_t slide = -2; slide <= 2; slide++) {
      //   for (uint8_t column = 2; column <= 2 && column >= 0; column--) {
      //     for (uint8_t row = 4; row <= 4 && row >= 0; row--) {
      //       if ((column + slide) < 0 || (column + slide) > 2) {
      //         ws2812_sendarray((uint8_t *)&ledOff,3);
      //         continue; // Skip out of bounds bits
      //       }
      //       if ((bitmap >> (15-((column + slide) + row*3))) & 0x1) {
      //         ws2812_sendarray((uint8_t *)&ledOn,3);
      //       } else {
      //         // ws2812_sendarray((uint8_t *)&ledOn,3);
      //         ws2812_sendarray((uint8_t *)&ledOff,3);
      //       }
      //     }
      //   }
      //   _delay_ms(100);
      // }
      // for (uint8_t j = 0; j < 15; j++) {
      //   ws2812_sendarray((uint8_t *)&ledOff,3);
      // }
      // _delay_ms(100);
    }
  }

  // uint8_t pos=0;
  // uint8_t direction=1;
  // uint8_t i;

  // while(1)
  //   {

  //   for (i=0; i<pos; i++)
  //     ws2812_sendarray((uint8_t *)&ledRed,3);     // Repeatedly send "red" to the led string.
  //                             // No more than 1-2 s should pass between calls
  //                             // to avoid issuing a reset condition.
  //   for (i=0; i<(30-pos); i++)
  //     ws2812_sendarray((uint8_t *)&ledOn,3);     // white


  //   _delay_ms(50);                    // Issue reset and wait for 50 ms.

  //   pos+=direction;
  //   if ((pos==16)||(pos==0)) direction=-direction;
  //   }
}
