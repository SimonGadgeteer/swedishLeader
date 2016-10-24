#!/usr/bin/env python2

port = 8080
host = ''

import urllib2
#probably no necessary --> remote kv store in use; import registry 
import leader
#to do import store
#import config


def registerself():
	try:
		register = urllib2.Request('http://kvstore-python-kvstore.44fs.preview.openshiftapps.com/registry/'+ selfnodeName)
		response = urllib2.urlopen(register)
		registerResponse = response.read()
		print("Node registered as "+registerResponse)
	except Exception as e:
		print("Error registering: ",e)

def application(environ, start_response):
		ctype = "text/plain"
		status = "200 OK"


		if environ['PATH_INFO'].startswith("/store"):
			return store.application(environ, start_response)
		else:
			return leader.application(environ, start_response)

if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	httpd = make_server(host, port, application)
	while True:
			print("waiting")
			httpd.handle_request()