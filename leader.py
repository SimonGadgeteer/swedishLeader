import urllib2

def getAvailablePatricipants():
	req = urllib2.Request('http://kvstore-python-kvstore.44fs.preview.openshiftapps.com/registry')
	response = urllib2.urlopen(req)
	the_page = response.read()
	print(the_page);