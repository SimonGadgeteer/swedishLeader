#!/usr/bin/env python
import urllib.request
import os

port = 8080
host = ''

if os.environ.get('SWEDISHLEADER_SERVICE_PORT'):
    port = int(os.environ.get('SWEDISHLEADER_SERVICE_PORT'))

if os.environ.get('SWEDISHLEADER_SERVICE_HOST'):
    host = os.environ.get('SWEDISHLEADER_SERVICE_HOST')



# probably no necessary --> remote kv store in use; import registry
from random import randint


# to do import store
# import config


def registerself():
    try:
        response = urllib.request.urlopen(
            'http://isprot-registry.appspot.com/registry/touriste/1272');
        registerResponse = response.read().decode('UTF-8')
        print("Node registered as " + registerResponse)
    except Exception as e:
        print("Error registering: ", e)


def application(environ, start_response):
    ctype = 'text/plain'
    status = '200 OK'
    response_body = "It works"

    if environ['PATH_INFO'].startswith("/store"):
        return store.application(environ, start_response)
    elif environ['PATH_INFO'].startswith("/leader"):
        return True
        if environ['PATH_INFO'].startswith("/leader/vote"):
            start_response(status, "('Content-Type', ctype)")
            return vote()
    else:
        response_body = 'It Works'

    response_body = response_body.encode('utf-8')
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]


def getNodeList():
    try:
        response = urllib.request.urlopen(
            'http://isprot-registry.appspot.com/registry/touriste')
        registerResponse = response.read().decode('UTF-8')
        listOfAvailableNodes = registerResponse[13:].split(",")
        print(listOfAvailableNodes)
    except Exception as e:
        print("Error registering: ", e)

def vote():
    return randint(0,1)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server(host, port, application)
    registerself()
    getNodeList()

    while True:
        httpd.handle_request()
