// http://www.technoblogy.com/show?1YQY

// uint16_t byte_counter = 0;
uint16_t counter = 0;
// uint8_t bit_counter = 0;

#include <avr/wdt.h>
#include <avr/sleep.h>
#include "sequence.h"

#define LED_OFF PORTB = 0b0100
#define LED_ON PORTB = 0b0000

void setup() {
  // Power saving measures:
  // Disable ADC:
  ADCSRA = 0;
  // Shut down ADC and timer0
  PRR = 0b11;

  // Setup IO:
  DDRB = 0b0100; // PB2 as an output
  LED_OFF;

  // Enable interrupts
  sei();
}

void sleep() {
  // Tell the watchdog timer to wake us up in 120ms.
  wdt_enable(WDTO_120MS);
  WDTCSR |= (1<<WDIE | 1<<WDE);

  // Go to sleep.
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  sleep_cpu();
}

// This looks at the next bit in the sequence and sets the LED accordingly.
void blink() {
  // if (sequence[byte_counter] & (0x01 << bit_counter)) {
  // if (0x01 & (sequence[byte_counter] >> bit_counter)) {
  //   LED_ON;
  // } else {
  //   LED_OFF;
  // }
  // counter = (counter + 1)%(sizeof(sequence)*8);
  PORTB = (0x01 & ~(sequence[(counter & 0xFFF8)>>3] >> (counter & 0x07))) << 2;
  counter = (counter + 1)%(sizeof(sequence)*8);
  // bit_counter++;
  // if (bit_counter == 8) {
  //   bit_counter = 0;
  //   byte_counter = (byte_counter + 1)%sizeof(sequence);
  // }

}

// This fires when the watchdog timer expires and wakes up the CPU.
ISR(WDT_vect) {
  sleep_disable();
}

void loop() {
  blink();
  sleep();
}