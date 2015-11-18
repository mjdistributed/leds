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

// physical serial buffer size of arduino uno
#define SERIAL_BUFFER_SIZE 64

// Define which pins to use.
const uint8_t dataPin = 8;
const uint8_t clockPin = 12;

// Create an object for writing to the LED strip.
APA102<dataPin, clockPin> ledStrip;

// Set the number of LEDs to control.
const uint16_t ledCount = 64;//240;

uint16_t brightness = 10; // 0 - 31
const byte num_chasers = 1;
const byte chaser_width = 80;

// "back" positions of each chaser
uint16_t on_leds[num_chasers];

// Create a buffer for holding the colors (3 bytes per color).
rgb_color leds[ledCount];
// Create a buffer for holding the colors (3 bytes per color).
rgb_color start_leds[ledCount];

rgb_color rgb;

void setup()
{
  Serial.begin(9600);
  for(int i = 0; i < num_chasers; i++) {
    on_leds[i] = i * ledCount / (num_chasers);
    for(int j = 0; j < chaser_width && on_leds[i] + j < ledCount; j++) {
      start_leds[on_leds[i] + j].red = 255;
      start_leds[on_leds[i] + j].green = 255;
      start_leds[on_leds[i] + j].blue = 255;
    }
  }
  ledStrip.write(start_leds, ledCount, brightness);
}

uint16_t i = 0;
uint16_t buffer_index = 0;
uint16_t MAX_BRIGHTNESS = 20;
uint16_t input[SERIAL_BUFFER_SIZE];

void loop()
{
  
  // fill input buffer
  if (Serial.available() > 0) {
    int just_read = int(Serial.read());
    input[buffer_index++] = just_read;
    Serial.print("input: ");
    Serial.print(just_read);
    Serial.print(", ");
  }
  
  // once filled buffer, notify producer
  if (buffer_index >= SERIAL_BUFFER_SIZE) {
    buffer_index = 0;
    uint16_t start_i = i;
    uint16_t input_index = 0;
    for(i; i < start_i + SERIAL_BUFFER_SIZE && i < ledCount; i++) {
      leds[i].red = input[input_index] * 1.0 / MAX_BRIGHTNESS * start_leds[i].red;
      leds[i].green = input[input_index] * 1.0 / MAX_BRIGHTNESS * start_leds[i].green;
      leds[i].blue = input[input_index] * 1.0 / MAX_BRIGHTNESS * start_leds[i].blue;
      input_index++;
      Serial.print("red: ");
      Serial.print(leds[i].red);
      Serial.print(", ");
    }
    Serial.print("line_end\n");
//    int input = Serial.parseInt();
//    Serial.write("i: ");
//    Serial.write(i);
//    if (i < ledCount) {
//      if (input <= MAX_BRIGHTNESS) {
//        brightness = input;  
//        leds[i].red = input * 1.0 / MAX_BRIGHTNESS * leds[i].red;
//        leds[i].green = input * 1.0 / MAX_BRIGHTNESS * leds[i].green;
//        leds[i].blue = input * 1.0 / MAX_BRIGHTNESS * leds[i].blue;
//        
//        if (i < ledCount - 1) {
////          Serial.write("setting brightness: ");
////          Serial.print(brightness);
//          Serial.write("red: ");
//          Serial.print(leds[i].red);
//          Serial.write("\n");
//        }
//      }
//      else {
////        Serial.write("input: ");
////        Serial.print(input);
////        Serial.write(", max_brightness: ");
////        Serial.print(MAX_BRIGHTNESS);
////        Serial.write(", i: ");
////        Serial.print(i);
//        Serial.write("line_end\n");
//      }
//    }
//    i ++;
    if (i == ledCount) {
//      Serial.write("writing to strip\n");
      ledStrip.write(leds, ledCount, MAX_BRIGHTNESS);
      i = 0;
    }
  }
    
}
