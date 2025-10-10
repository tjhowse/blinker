#define ws2812_port B     // Data port
#define ws2812_pin  2     // Data out pin


#include <util/delay.h>
#include <avr/io.h>
#include <avr/wdt.h>
#include <avr/sleep.h>
#include <avr/interrupt.h>

#include "attiny10_ws2812.h"  // Include the ws2812 library
#include "tomthumb_5x3_font.h" // Include the font header
#include "message.h"

const uint16_t message_len = (sizeof(message)*8)/6;
// Note: These are GRB values.
const cRGB ledOff = {0,0,0};
const cRGB ledOn = {16,16,16};
const cRGB ledGreen = {0,16,0};
const cRGB ledRed = {1,0,0};
const cRGB ledBlue = {0,0,16};


// 2025-09-23 First run white, then green.
// 2025-09-24 Red then blue

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

  // Power saving measures:
  // Disable ADC:
  ADCSRA = 0;
  // Shut down ADC and timer0
  PRR = 0b11;

  // Enable interrupts
  sei();


  while (1) {
    for (uint16_t charIndex = 0; charIndex < message_len; charIndex++) {
      // This henious nonsense looks up the character in the message array.
      // Each character is 6 bits, so we need to read two bytes from the array
      // in case the character straddles a byte boundary.
      uint8_t index = (charIndex*6)/8; // Index of the first byte
      uint8_t shift = (charIndex*6)%8; // Bit shift within the two bytes
      uint8_t c = (((message[index] | message[index+1] << 8) >> shift) & 0x003F) * 2;
      uint16_t bitmap = (TomThumbBitmapsRotated[c] << 8) | TomThumbBitmapsRotated[c + 1];

      for (uint8_t bit = 0; bit < 16; bit++) {
        if ((bitmap >> bit) & 0x1) {
          ws2812_sendarray((uint8_t *)&ledRed, 3);
        } else {
          ws2812_sendarray((uint8_t *)&ledOff, 3);
        }
      }
    //   _delay_ms(400);
      sleep();
    }
  }
}

void sleep() {
  // Tell the watchdog timer to wake us up in 500ms.
  wdt_enable(WDTO_500MS);
  WDTCSR |= (1<<WDIE | 1<<WDE);

  // Go to sleep.
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  sleep_cpu();
}

// This fires when the watchdog timer expires and wakes up the CPU.
ISR(WDT_vect) {
  sleep_disable();
}
