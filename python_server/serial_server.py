import serial
from rgb_to_hsv import rgbToHsv, scaleHue
ser = serial.Serial('/dev/cu.usbmodemfa131', 9600)

#!/usr/bin/env python
 
import SimpleHTTPServer
import SocketServer
import os
import cgi

def get_rgb_from_hex(hex_color):
	red = int(hex_color[:2], 16)
	green = int(hex_color[2:4], 16)
	blue = int(hex_color[4:], 16)
	# print("r: " + str(red) + "g: " + str(green) + "b: " + str(blue))
	return (red, green, blue)

 
#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

  
	#handle GET command
	def do_GET(self):
		try:
			if self.path == '/blue.html':
				ser.write('200')
			if self.path == '/red.html':
				ser.write('0')
			if '/index.html?hex_color=' in self.path:
				print("here!" + "\n")
				hex_color = self.path[self.path.index('=') + 1:]
				print("hex_color: " + str(hex_color) + "\n")
				SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
				color = get_rgb_from_hex(hex_color)
				print(color)
				hsv = rgbToHsv(color[0], color[1], color[2])
				hue = int(round(scaleHue(hsv[0])))
				print("hue: " + str(hue) + "\n")
				ser.write(str(hue))
				return
			# if self.path.endswith('.html'):
			f = open('./' + self.path) #open requested file
			# else:
			# 	print("didn't initialize f :(\n")

			#send code 200 response
			self.send_response(200)

			#send header first
			self.send_header('Content-type','text-html')
			self.end_headers()

			#send file content to client
			self.wfile.write(f.read())
			f.close()
			return

		except IOError:
		  self.send_error(404, 'file not found')



	    # CITATION: http://stackoverflow.com/questions/4233218/python-basehttprequesthandler-post-variables
	 #    ctype, pdict = cgi.parse_header(self.headers['content-type'])
	 #    if ctype == 'multipart/form-data':
	 #        postvars = cgi.parse_multipart(self.rfile, pdict)
	 #    elif ctype == 'application/x-www-form-urlencoded':
	 #        length = int(self.headers['content-length'])
	 #        postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
	 #    else:
	 #        postvars = {}
		# print("postvars: " + str(postvars))
		# SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)



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


		# form = cgi.FieldStorage(
  #           fp=self.rfile,
  #           headers=self.headers,
  #           environ={'REQUEST_METHOD':'POST',
  #                    'CONTENT_TYPE':self.headers['Content-Type'],
  #                    })
		# for item in form.list:
		# 	print(str(item) + "\n")
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