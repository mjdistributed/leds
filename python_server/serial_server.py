import serial
# import SocketServer
# from BaseHTTPServer import BaseHTTPRequestHandler

ser = serial.Serial('/dev/cu.usbmodemfa131', 9600)

# def some_function():
#     print "some_function got called"

# class MyHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/blue':
#             ser.write(200)
#         if self.path == '/red':
#             ser.write(0)
#         if self.path == '/index.html':
#         	# self.send_response("<a href='red'>red!</a>")
#         	self.wfile.write("hey")
#         	print("hey!")
#         self.send_response(200)

# httpd = SocketServer.TCPServer(("", 8080), MyHandler)
# httpd.serve_forever()


#!/usr/bin/env python
 
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
 
#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):

  
	#handle GET command
	def do_GET(self):
		try:
			if self.path == '/blue.html':
				ser.write('200')
			if self.path == '/red.html':
				ser.write('0')
			if self.path.endswith('.html'):
				print("initialized f!\n")
				f = open('./' + self.path) #open requested file
			else:
				print("didn't initialize f :(\n")

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
	  
def run():
  print('http server is starting...')
 
  #ip and port of servr <- IP set dynamically
  #by default http server port is 80
  server_address = ('', 8080)
  httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
  print('http server is running...')
  httpd.serve_forever()
  
if __name__ == '__main__':
  run()