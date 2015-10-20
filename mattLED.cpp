#include "Arduino.h"
#include "FASTLED.h"




class MattLED {
 public:
   	//pass a reference to a Print object
	MattLED( HardwareSerial &print ) { 
	 printer = &print; //operate on the adress of print
	 printer->begin(9600);
	}
	void brightness_control() {
	  while (printer->available() > 0) {
	    int brightness = Serial.parseInt();
	    if (brightness > max_brightness || brightness < min_brightness) {
	      return;
	    }
	    if (printer->read() == '\n') {
	      LEDS.setBrightness(brightness);
	    }
	  }
	}
 	private:
   		HardwareSerial* printer;
};