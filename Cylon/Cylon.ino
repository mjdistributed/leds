#include "FastLED.h"
#include "mattLED_fastLED.h"

// How many leds in your strip?
#define NUM_LEDS 240

#define DATA_PIN 8
#define CLOCK_PIN 12
#define COLOR_ORDER BGR
#define CHIPSET APA102

// Define the array of leds
CRGB leds[NUM_LEDS];

void setup() { 
  Serial.begin(9600);
	FastLED.addLeds<CHIPSET, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_LEDS);
	LEDS.setBrightness(84);
}

void fadeall() { 
  for(int i = 0; i < NUM_LEDS; i++) { 
    leds[i].nscale8(250); 
  } 
}

void loop() { 

  brightness_control_fastLED();
  
	static uint8_t hue = 0;
	// First slide the led in one direction
	for(int i = 0; i < NUM_LEDS; i++) {
		// Set the i'th led to red 
		leds[i] = CHSV(hue++, 255, 255);
		// Show the leds
		FastLED.show(); 
		// now that we've shown the leds, reset the i'th led to black
		// leds[i] = CRGB::Black;
		fadeall();
		// Wait a little bit before we loop around and do it again
		delay(5);
	}

	// Now go in the other direction.  
	for(int i = (NUM_LEDS)-1; i >= 0; i--) {
		// Set the i'th led to red 
		leds[i] = CHSV(hue++, 255, 255);
		// Show the leds
		FastLED.show();
		// now that we've shown the leds, reset the i'th led to black
		// leds[i] = CRGB::Black;
		fadeall();
		// Wait a little bit before we loop around and do it again
		delay(5);
	}
}
