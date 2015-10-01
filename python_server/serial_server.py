import serial
from rgb_to_hsv import rgbToHsv, scaleHue
import glob
import subprocess
import urllib

ser = serial.Serial('/dev/cu.usbmodemfa131', 9600)

#!/usr/bin/env python
 
import SimpleHTTPServer
import SocketServer
import os
import cgi

# creates an html form object that submits "program=<filename>" as parameter
def get_form(filename):
	html_result = """
		<form action="/index.html" method="GET">
			<input name="program" value=\""""  + filename + """\" />
			<input type="submit" value="Submit"/>
		</form>
		"""
	return html_result

def get_rgb_from_hex(hex_color):
	red = int(hex_color[:2], 16)
	green = int(hex_color[2:4], 16)
	blue = int(hex_color[4:], 16)
	# print("r: " + str(red) + "g: " + str(green) + "b: " + str(blue))
	return (red, green, blue)

def run_process(filename):
	print("############ running process ###########")
	bashCommand = "/Applications/Arduino.app/Contents/Java/hardware/tools/avr/bin/avrdude -C/Applications/Arduino.app/Contents/Java/hardware/tools/avr/etc/avrdude.conf -v -patmega328p -carduino -P/dev/cu.usbmodemfa131 -b115200 -D -Uflash:w:/Users/matt/src/leds/python_server/" + filename + ":i"
	# /Applications/Arduino.app/Contents/Java/hardware/tools/avr/bin/avrdude -C/Applications/Arduino.app/Contents/Java/hardware/tools/avr/etc/avrdude.conf -v -patmega328p -carduino -P/dev/cu.usbmodemfa131 -b115200 -D -Uflash:w:/var/folders/k9/f3jfm9l51wj4z6j350w5w_800000gn/T/build1561620600180326105.tmp/pulse.cpp.hex:i 

	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	print("############ done running process ###########")
 
#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  
	#handle GET command
	def do_GET(self):
		print("doing get...")
		print("path: " + str(self.path))
		try:
			if '/index.html?hex_color=' in self.path:
				print("here!" + "\n")
				hex_color = self.path[self.path.index('=') + 1:]
				print("hex_color: " + str(hex_color) + "\n")
				color = get_rgb_from_hex(hex_color)
				print(color)
				ser.write(str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + "\n")
				SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
				return
			if '/index.html?program=' in self.path:
				print("loading program!" + "\n")
				filename = self.path[self.path.index('=') + 1:]
				filename = urllib.unquote(filename).decode('utf8') 
				print("filename: " + filename + "\n")
				run_process(filename)
				# SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
				# return
			if('?' in self.path):
				self.path = self.path[:self.path.index('?')]
			print("path: " + self.path)
			# if self.path.endswith('.html'):
			f = open('./' + self.path) #open requested file
			html = f.read()
			if '/index.html' in self.path:
				filenames = glob.glob("hex_files/*.hex")
				for fname in filenames:
					print("fname: " + fname + "||||")
					html = html + get_form(fname)
				html = html + """"
					</body>
					</html>"""
			

			#send code 200 response
			self.send_response(200)

			#send header first
			self.send_header('Content-type','text-html')
			self.end_headers()

			#send file content to client
			self.wfile.write(html)
			f.close()
			print("done doing get...")
			return

		except IOError:
		  self.send_error(404, 'file not found')



	def do_POST(self):
		ctype, pdict = cgi.parse_header(self.headers['content-type'])
		if ctype == 'multipart/form-data':
			postvars = cgi.parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers['content-length'])
			postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
		else:
			postvars = {}
		print("postvars: " + str(postvars) + "\n")

		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
	  
def run():
  print('http server is starting...')
 
  #ip and port of servr <- IP set dynamically
  #by default http server port is 80
  server_address = ('', 8080)
  httpd = SocketServer.TCPServer(server_address, KodeFunHTTPRequestHandler)
  print('http server is running...')
  httpd.serve_forever()
  
if __name__ == '__main__':
  run()