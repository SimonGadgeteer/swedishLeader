#!/usr/bin/env python
import sys
import urllib.request
# probably no necessary --> remote kv store in use; import registry
import leader, store, create_udr, create_bill
from random import randint

port = 8080
host = ''
isLeader = True

if len(sys.argv) > 2:
    host = sys.argv[1]
    port = int(sys.argv[2])


# import config


def registerself(host, port):
    try:
        doRegister = True
        hostname = host + ':' + str(port)
        hosts = leader.getNodeList()

        for host in hosts:
            if host.strip() == hostname:
                doRegister = False

        if doRegister:
            response = urllib.request.urlopen('http://isprot-registry.appspot.com/registry/touriste1/' + hostname)
            registerResponse = response.read().decode('UTF-8')

        print("Node registered as " + hostname)
    except Exception as e:
        print("Error registering: ", e)


def application(environ, start_response):
    ctype = 'text/plain'
    status = '200 OK'
    response_body = "It works"

    if environ['PATH_INFO'].startswith("/store"):
        #return store.application(environ, start_response)
        return store.getValues()
    elif environ['PATH_INFO'].startswith("/store/"):
        return store.storeValues()
    elif environ['PATH_INFO'].startswith("/leader"):
        if environ['PATH_INFO'].startswith("/leader/vote"):
            response_body = str(leader.vote())
            if response_body == '0':
                isLeader = False
            else:
                isLeader = True
        else:
            response_body = leader.election(host, port)
    else:
        response_body = 'It Works'

    response_body = response_body.encode('utf-8')
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]


def generateUDR():
    create_udr.generate()

def createBill():
    create_bill.generate()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server(host, port, application)
    registerself(host, port)

    while True:
        httpd.handle_request()
