

/* This example shows how to display a moving rainbow pattern on
 * an APA102-based LED strip. */

/* By default, the APA102 uses pinMode and digitalWrite to write
 * to the LEDs, which works on all Arduino-compatible boards but
 * might be slow.  If you have a board supported by the FastGPIO
 * library and want faster LED updates, then install the
 * FastGPIO library and uncomment the next two lines: */
// #include <FastGPIO.h>
// #define APA102_USE_FAST_GPIO
#include <FastGPIO.h>
#define APA102_USE_FAST_GPIO
#include <APA102.h>

// Define which pins to use.
const uint8_t dataPin = 8;
const uint8_t clockPin = 12;

// Create an object for writing to the LED strip.
APA102<dataPin, clockPin> ledStrip;

// Set the number of LEDs to control.
const uint16_t ledCount = 100;
const uint16_t brightness = 20; // 0 - 31

// Create a buffer for holding the colors (3 bytes per color).
rgb_color leds[ledCount];

const uint16_t num_cycles_per_second = 10;

void setup()
{
  for(uint16_t i = 0; i < ledCount; i++) {
    leds[i].red = 255;
    leds[i].green = 255;
    leds[i].blue = 255;
  }
}

void loop()
{
  
  
  ledStrip.write(leds, ledCount, brightness);
  delay(10);
  ledStrip.write(leds, ledCount, 0);
  delay(1000 / num_cycles_per_second);
//ledStrip.startFrame();
//ledStrip.sendColor(255, 255, 255, 20);
//ledStrip.sendColor(255, 255, 255, 20);
//ledStrip.sendColor(255, 255, 255, 20);
//ledStrip.sendColor(255, 255, 255, 20);
////delay(1);
//ledStrip.endFrame(ledCount);
//ledStrip.startFrame();
//ledStrip.sendColor(0, 0, 0, 0);
//ledStrip.sendColor(0, 0, 0, 0);
//ledStrip.sendColor(0, 0, 0, 0);
//ledStrip.sendColor(0, 0, 0, 0);
//ledStrip.endFrame(ledCount);
//delay(1000 / num_cycles_per_second);
//delay(100);
  
  
  
}
