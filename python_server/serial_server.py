import serial
import glob
import subprocess
import urllib
import SimpleHTTPServer
import SocketServer
import os
import cgi
import socket

from rgb_to_hsv import rgbToHsv, scaleHue
import page_builder as pb
from BaseHTTPServer import HTTPServer


port = '/dev/cu.usbmodemfa131'  # usb port left-bottom (away from screen)
# port = '/dev/cu.usbmodemfd121' # usb port left-top (toward screen)

try:
	ser = serial.Serial(port, 9600)
except:
	print("error connecting to USB port!")


def get_rgb_from_hex(hex_color):
	red = int(hex_color[:2], 16)
	green = int(hex_color[2:4], 16)
	blue = int(hex_color[4:], 16)
	# print("r: " + str(red) + "g: " + str(green) + "b: " + str(blue))
	return (red, green, blue)

def run_process(filename):
	print("############ running process ###########")
	bashCommand = "/Applications/Arduino.app/Contents/Java/hardware/tools/avr/bin/avrdude -C/Applications/Arduino.app/Contents/Java/hardware/tools/avr/etc/avrdude.conf -v -patmega328p -carduino -P" + port + " -b115200 -D -Uflash:w:/Users/matt/src/leds/python_server/" + filename + ":i"

	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	print("############ done running process ###########")
 
def protected_serial_write(data):
	""" Required: data - String """
	try:
		ser.write(data)
	except IOError:
		print("Error writing to serial output")


#Create custom HTTPRequestHandler class
class CustomHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  
	#handle GET command
	def do_GET(self):
		print("doing get...")
		print("path: " + str(self.path))
		try:
			html = ""
			if "." in self.path and not '?' in self.path:
				print("loading static file: " + self.path)
				# load static files as needed
				f = open("." + self.path)
				html = f.read()
				f.close()
			else:
				dynamic_html = ""
				# generate dynamic html result
				if '?brightness' in self.path:
					brightness = int(self.path[self.path.index('=') + 1:])
					print("brightness: " + str(brightness))
					if(brightness < 0 or brightness > 20):
						dynamic_html += """<div class="alert alert-warning" role="alert">
			            	Brightness must be between 0 and 20.</div>"""
					else:
						protected_serial_write(str(brightness) + "\n");
						print("setting brightness to: " + str(brightness))
				if '?hex_color=' in self.path:
					hex_color = self.path[self.path.index('=') + 1:]
					color = get_rgb_from_hex(hex_color)
					protected_serial_write(str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + "\n")
				if '?program=' in self.path:
					filename = self.path[self.path.index('=') + 1:]
					filename = urllib.unquote(filename).decode('utf8') 
					run_process(filename)
				if('?' in self.path):
					self.path = self.path[:self.path.index('?')]
				#### construct returned html
				# add buttons for running programs
				dynamic_html += "<form action='/' method='GET'>\n"
				filenames = glob.glob("hex_files/*.hex")
				for fname in filenames:
					program_name = fname[fname.index('/') + 1 : fname.index('.cpp')]
					dynamic_html = dynamic_html + pb.get_form(fname, program_name)
				html = pb.get_html(dynamic_html)

			#send code 200 response
			self.send_response(200)

			#send header first
			self.send_header('Content-type','text-html')
			self.end_headers()

			#send file content to client
			self.wfile.write(html)
			print("done doing get...")
			return

		except IOError:
		  self.send_error(404, 'file not found')

class HTTPServerV6(HTTPServer):
  address_family = socket.AF_INET6
	  
def run():
  	print('http server is starting...')
 

  	#ip and port of servr <- IP set dynamically
  	#by default http server port is 80
  	server_address = ('', 8080)
  	httpd = HTTPServerV6(server_address, CustomHTTPRequestHandler)
  	# httpd = SocketServer.TCPServer(server_address, CustomHTTPRequestHandler)
  	print('http server is running...')
	try:
  		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	print("closing server")
	httpd.server_close()
  
if __name__ == '__main__':
  run()