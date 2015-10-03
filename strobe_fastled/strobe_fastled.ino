#include "FastLED.h"

// How many leds in your strip?
#define NUM_LEDS 240

// For led chips like Neopixels, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
#define DATA_PIN 8
#define CLOCK_PIN 12
#define COLOR_ORDER BGR
#define CHIPSET APA102

// Define the array of leds
CRGB leds[NUM_LEDS];
const uint16_t num_cycles_per_second = 13;

void setup() { 

  FastLED.addLeds<CHIPSET, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_LEDS);

  for(int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::White;
  }
}

void loop() { 
  // Turn the LED on, then pause
  
//  leds[0] = CRGB::White;
  FastLED.setBrightness(225);
  FastLED.show();
//  delay(1);
  // Now turn the LED off, then pause
//  for(int i = 0; i < NUM_LEDS; i++) {
//    leds[i] = CRGB::Black;
//  }
FastLED.setBrightness(0);
  FastLED.show();
  delay(1000 / num_cycles_per_second);
}
