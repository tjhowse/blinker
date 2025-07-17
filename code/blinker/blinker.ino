#define ws2812_port B     // Data port
#define ws2812_pin  2     // Data out pin


#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#include "attiny10_ws2812.h"  // Include the ws2812 library
#include "tomthumb_5x3_font.h" // Include the font header

const char message[] = "Hello World!"; // Message to display
// const uint8_t ledOff[] = {128,128, 128}; // RGB values for LED off
// const uint8_t ledOn[] = {0, 0, 0}; // RGB values for LED on
// const uint8_t ledRed[] = {0, 0, 0}; // RGB values for LED red

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

  for (uint8_t i = 0; message[i] != '\0'; i++) {
  // while (1) {
    // uint16_t bitmap = TomThumbBitmaps[message[i] - 34];
    // uint16_t bitmap = TomThumbBitmaps[33][1] + TomThumbBitmaps[33][0] << 8;
    // uint16_t bitmap = (0x57 << 8) + 0xDA;
    uint16_t bitmap = 0XD75C; // B
    for (uint8_t column = 2; column <= 2 && column >= 0; column--) {
      for (uint8_t row = 4; row <= 4 && row >= 0; row--) {
        if ((bitmap >> (15-(column + row*3))) & 0x1) {
          ws2812_sendarray((uint8_t *)&ledOn,3);
        } else {
          // ws2812_sendarray((uint8_t *)&ledOn,3);
          ws2812_sendarray((uint8_t *)&ledOff,3);
        }
      }
    }
    // _delay_ms(50);
    _delay_ms(500);
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
