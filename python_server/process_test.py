import subprocess

filename = "entire_rainbow.cpp.hex"
# filename = "pulse.cpp.hex"
bashCommand = "/Applications/Arduino.app/Contents/Java/hardware/tools/avr/bin/avrdude -C/Applications/Arduino.app/Contents/Java/hardware/tools/avr/etc/avrdude.conf -v -patmega328p -carduino -P/dev/cu.usbmodemfa131 -b115200 -D -Uflash:w:/Users/matt/src/leds/python_server/hex_files/" + filename + ":i"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)