/* This example shows how to display a moving rainbow pattern on
 * an APA102-based LED strip. */

/* By default, the APA102 uses pinMode and digitalWrite to write
 * to the LEDs, which works on all Arduino-compatible boards but
 * might be slow.  If you have a board supported by the FastGPIO
 * library and want faster LED updates, then install the
 * FastGPIO library and uncomment the next two lines: */
 #include <FastGPIO.h>
 #define APA102_USE_FAST_GPIO
#include <APA102.h>
#include "mattLED.h"

// Define which pins to use.
const uint8_t dataPin = 8;
const uint8_t clockPin = 12;

// Create an object for writing to the LED strip.
APA102<dataPin, clockPin> ledStrip;

// Set the number of LEDs to control.
const uint16_t ledCount = 200;//240;

uint16_t brightness = 10; // 0 - 31
const byte num_chasers = 1;
const byte chaser_width = 80;

// "back" positions of each chaser
uint16_t on_leds[num_chasers];

// Create a buffer for holding the colors (3 bytes per color).
rgb_color leds[ledCount];

rgb_color rgb;

void setup()
{
  Serial.begin(9600);
  for(int i = 0; i < num_chasers; i++) {
    on_leds[i] = i * ledCount / (num_chasers);
    for(int j = 0; j < chaser_width && on_leds[i] + j < ledCount; j++) {
      leds[on_leds[i] + j].red = 255;
      leds[on_leds[i] + j].green = 255;
      leds[on_leds[i] + j].blue = 255;
    }
  }
  ledStrip.write(leds, ledCount, brightness);
}

uint16_t i = 0;
uint16_t MAX_BRIGHTNESS = 20;

void loop()
{
  if (Serial.available() > 0) {
    int input = Serial.parseInt();
//    Serial.write("i: ");
//    Serial.write(i);
    if (i < ledCount) {
      if (input <= MAX_BRIGHTNESS) {
        brightness = input;  
        leds[i].red = input * 1.0 / MAX_BRIGHTNESS * leds[i].red;
        leds[i].green = input * 1.0 / MAX_BRIGHTNESS * leds[i].green;
        leds[i].blue = input * 1.0 / MAX_BRIGHTNESS * leds[i].blue;
        
        if (i < ledCount - 1) {
//          Serial.write("setting brightness: ");
//          Serial.print(brightness);
          Serial.write("red: ");
          Serial.print(leds[i].red);
          Serial.write("\n");
        }
      }
      else {
//        Serial.write("input: ");
//        Serial.print(input);
//        Serial.write(", max_brightness: ");
//        Serial.print(MAX_BRIGHTNESS);
//        Serial.write(", i: ");
//        Serial.print(i);
        Serial.write("line_end\n");
      }
    }
    i ++;
    if (i == ledCount) {
      Serial.write("writing to strip\n");
      ledStrip.write(leds, ledCount, MAX_BRIGHTNESS);
      i = 0;
    }
  }
    
}
