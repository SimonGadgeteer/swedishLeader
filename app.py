#!/usr/bin/env python
import sys
import urllib.request
import socket
# probably no necessary --> remote kv store in use; import registry
import leader, store, create_udr, create_bill
from random import randint

port = 8080
host = socket.gethostname()
isLeader = True
leaderhost = ''


if len(sys.argv) > 2:
    host = sys.argv[1]
    port = int(sys.argv[2])


# import config


def registerself(host, port):
    try:
        doRegister = True
        hostname = host + ':' + str(port)
        hosts = leader.getNodeList()

        if hosts:
            for host in hosts:
                if host.strip() == hostname:
                    doRegister = False

        if doRegister:
            response = urllib.request.urlopen('http://isprot-registry.appspot.com/registry/touriste5/' + hostname)
            registerResponse = response.read().decode('UTF-8')

        print("Node registered as " + hostname)
    except Exception as e:
        print("Error registering: ", e)


def application(environ, start_response):
    global leaderhost
    ctype = 'text/plain'
    status = '200 OK'
    response_body = "It works"

    if environ['PATH_INFO'].startswith("/store/"):
        params = environ['PATH_INFO'][7:]
        params = params.split('=')
        #return store.application(environ, start_response)
        response_body = store.storeValues(params[0], params[1])
    elif environ['PATH_INFO'].startswith("/store"):
        return store.getValues()
    elif environ['PATH_INFO'].startswith("/leader"):
        if environ['PATH_INFO'].startswith("/leader/vote"):
            response_body = str(leader.vote())
            if response_body == '0':
                isLeader = False
            else:
                isLeader = True
        else:
            response_body = leader.election(host, port)
    elif environ['PATH_INFO'].startswith("/newleader/"):
        leaderhost = environ['PATH_INFO'][11:]
        print('Registered Leader Host:' + leaderhost)
    elif environ['PATH_INFO'].startswith("/getleader"):
        response_body = leaderhost

    else:
        response_body = 'It Works'

    print('Called : ' + environ['PATH_INFO'])

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
