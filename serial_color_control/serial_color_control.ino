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

// Create a buffer for holding the colors (3 bytes per color).
rgb_color leds[ledCount];

// Set the brightness to use (the maximum is 31).
const uint16_t brightness = 20;
const uint16_t max_hue = 359;
const uint8_t rate_of_change = 1;

uint16_t hue;
//uint8_t rate_of_change = 1;


void setup()
{
  Serial.begin(9600);
}

// Converts a color from HSV to RGB.
// h is hue, as a number between 0 and 360.
// s is the saturation, as a number between 0 and 255.
// v is the value, as a number between 0 and 255.
rgb_color hsvToRgb(uint16_t h, uint8_t s, uint8_t v)
{
    uint8_t f = (h % 60) * 255 / 60;
    uint8_t p = (255 - s) * (uint16_t)v / 255;
    uint8_t q = (255 - f * (uint16_t)s / 255) * (uint16_t)v / 255;
    uint8_t t = (255 - (255 - f) * (uint16_t)s / 255) * (uint16_t)v / 255;
    uint8_t r = 0, g = 0, b = 0;
    byte constant = 20; // bigger constant -> longer wavelength
    byte wavelength = h/60 % constant; // wavelength
    switch(wavelength){  
        case 0: r = v; g = t; b = p; break;
        case 1: r = q; g = v; b = p; break;
        case 2: r = p; g = v; b = t; break;
        case 3: r = p; g = q; b = v; break;
        case 4: r = t; g = p; b = v; break;
        case 5: r = v; g = p; b = q; break;
    }
    return (rgb_color){r, g, b};
}

void loop()
{
  /*  check if data has been sent from the computer: */
  if (Serial.available()) {
    hue = Serial.parseInt();
    if(hue >= 0 && hue < 360) {
      rgb_color rgb = hsvToRgb(hue, 255, 255);
      for(uint16_t i = 0; i < ledCount; i++) {
        leds[i] = rgb;
      }
      ledStrip.write(leds, ledCount, brightness);
    }
    Serial.println(hue);
  }
}
