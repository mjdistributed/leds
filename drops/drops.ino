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

// Maximum number of drops
const uint16_t MAX_DROPS = 5;

// Create a buffer for holding the colors (3 bytes per color).
rgb_color leds[ledCount];

// Set the brightness to use (the maximum is 31).
const uint16_t brightness = 20;
const uint16_t max_hue = 359;
const uint8_t rate_of_change = 1;

// new_brightness = current_brightness * fade_factor
const float fade_factor = 0.8;

// on average will add a new drop every x iterations
uint16_t avg_iters_till_add_drop = 20;

struct drop {
  uint16_t start_index;
  int16_t age; // age of -1 signifies invalid
  rgb_color color;
};

drop drops[MAX_DROPS];

// current active drops
uint16_t num_drops = 0;

void setup()
{
  for (int i = 0; i < MAX_DROPS; i++) {
    drops[i] = (drop){0,-1};
  }
  // seed with an analog read on an unconnected pin 
  randomSeed(analogRead(0));
  Serial.begin(9600);
}



void loop()
{
  zero_leds();
  if (num_drops < MAX_DROPS) {
    // if can add another drop add a new drop random with given probability
    if (random(avg_iters_till_add_drop) == 0) {
      rgb_color color = get_random_color();
      uint16_t starting_index = get_random_index();
      add_drop(starting_index, color);  
    }
  }
  
  for (int i = 0; i < MAX_DROPS; i++) {
    // if drop is in use, update its leds
    if (drops[i].age > -1) {
      rgb_color curr_color = fade_rgb(drops[i].color, drops[i].age);
      // a drop's width is 2 * age
      for (int j = 0; j <= drops[i].age; j++) {
        int right_index = drops[i].start_index - j;
        int left_index = drops[i].start_index + j;
        if (validate_bounds(right_index)) {
          leds[right_index] = sum_colors(leds[right_index], curr_color);
          
        }
        if (validate_bounds(left_index)) {
          leds[left_index] = sum_colors(leds[left_index], curr_color);
        }
      }
      drops[i].age ++;
      if (is_zero(curr_color)) {
        drops[i].age = -1;
        num_drops --;
      }
    }
  }
  ledStrip.write(leds, ledCount, brightness);
  delay(10);
}

bool validate_bounds(int index) {
  return (index > -1 && index < ledCount);
}

bool is_zero(rgb_color input) {
  return (input.red <= 0 && input.green <= 0 && input.blue <= 0);
}

int get_random_index() {
    return random(ledCount);
}

rgb_color get_random_color() {
    return (rgb_color){random(255), random(255), random(255)};
}

rgb_color fade_rgb(rgb_color input, int age) {
  double factor = pow(fade_factor, age);
  return (rgb_color){input.red * factor, input.green * factor, input.blue * factor};
}

void add_drop(int index, rgb_color color) {
  num_drops++;
  // find open drop and fill it
  for (int i = 0; i < MAX_DROPS; i++) {
    // check if current drop is open
    if (drops[i].age < 0) {
      drops[i].start_index = index;
      drops[i].age = 0;
      leds[index] = color;
      drops[i].color = color;
      return;
    }
  }
}

rgb_color sum_colors(rgb_color one, rgb_color two) {
  rgb_color result;
  result.red = min(one.red + two.red, 255);
  result.green = min(one.green + two.green, 255);
  result.blue = min(one.blue + two.blue, 255);
  return result;
}

void zero_leds() {
  for (int i = 0; i < ledCount; i++) {
    leds[i] = (rgb_color){0, 0, 0};
  }
}

