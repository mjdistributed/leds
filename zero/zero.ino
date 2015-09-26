

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
const uint8_t dataPin = 11;
const uint8_t clockPin = 12;

// Create an object for writing to the LED strip.
APA102<dataPin, clockPin> ledStrip;

// Set the number of LEDs to control.
const uint16_t ledCount = 240;

const uint16_t brightness = 10; // 0 - 31

// Create a buffer for holding the colors (3 bytes per color).
rgb_color leds[ledCount];


void setup()
{
  for(int i = 0; i < ledCount; i++){
    leds[i].red = 0;
    leds[i].green = 0;
    leds[i].blue = 0;
  }
  ledStrip.write(leds, ledCount, brightness);
  delay(3000);
}

void loop()
{
  
}
