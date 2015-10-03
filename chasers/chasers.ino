

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

// Define which pins to use.
const uint8_t dataPin = 8;
const uint8_t clockPin = 12;

// Create an object for writing to the LED strip.
APA102<dataPin, clockPin> ledStrip;

// Set the number of LEDs to control.
const uint16_t ledCount = 240;

const uint16_t brightness = 10; // 0 - 31
const byte num_chasers = 1;
const byte chaser_width = 80;

// "back" positions of each chaser
uint16_t on_leds[num_chasers];

// Create a buffer for holding the colors (3 bytes per color).
rgb_color leds[ledCount];


void setup()
{
  for(int i = 0; i < num_chasers; i++) {
    on_leds[i] = i * ledCount / (num_chasers);
    for(int j = 0; j < chaser_width && on_leds[i] + j < ledCount; j++) {
      leds[on_leds[i] + j].red = 255;
      leds[on_leds[i] + j].green = 255;
      leds[on_leds[i] + j].blue = 255;
    }
  }
  ledStrip.write(leds, ledCount, brightness);
//  delay(3000);
}

void loop()
{
  for(int i = 0; i < num_chasers; i++) {
    leds[on_leds[i]].red = 0;
    leds[on_leds[i]].green = 0;
    leds[on_leds[i]].blue = 0;
    on_leds[i] += 1;
    if(on_leds[i] >= ledCount) {
      on_leds[i] = 0;
    }
    byte to_write_pos;
    // if front of chaser is off end of strip
    if(!(on_leds[i] + chaser_width - 1 >= ledCount)) {
      to_write_pos = on_leds[i] + chaser_width - 1;
    }
    else {
      to_write_pos = (on_leds[i] + chaser_width - 1) - ledCount;
    }
    leds[to_write_pos].red = 255;
    leds[to_write_pos].green = 255;
    leds[to_write_pos].blue = 255;
  }
  ledStrip.write(leds, ledCount, brightness);
  delay(20);
}
