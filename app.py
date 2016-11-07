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
            response = urllib.request.urlopen('http://isprot-registry.appspot.com/registry/touriste6/' + hostname)
            registerResponse = response.read().decode('UTF-8')

        print("Node registered as " + hostname)
    except Exception as e:
        print("Error registering: ", e)


def application(environ, start_response):
    global isLeader
    global leaderhost
    global host
    global port

    ctype = 'text/plain'
    status = '200 OK'
    response_body = "It works"

    print('Called : ' + environ['PATH_INFO'])

    if environ['PATH_INFO'].startswith("/store/"):
        params = environ['PATH_INFO'][7:]
        params = params.split('=')
        if isLeader == False:
            store.notifyLeader(leaderhost, params[0], params[1])
        else:
            store.syncAll(params[0], params[1], host, port)
        #return store.application(environ, start_response)
        response_body = store.storeValues(params[0], params[1], True)
    elif environ['PATH_INFO'].startswith("/store"):
        response_body =  str(store.getValues())
    elif environ['PATH_INFO'].startswith("/sync/"):
        params = environ['PATH_INFO'][6:]
        params = params.split('=')
        store.storeValues(params[0], params[1], False)

        if isLeader == True:
            print('I Am leader')
            store.syncAll(params[0], params[1], host, port)

    elif environ['PATH_INFO'].startswith("/leader"):
        if environ['PATH_INFO'].startswith("/leader/vote"):
            response_body = str(leader.vote())
            print(response_body)
            if response_body == '0':
                isLeader = False
            else:
                isLeader = True
        else:
            response_body = leader.election(host, port)
    elif environ['PATH_INFO'].startswith("/newleader/"):
        leaderhost = environ['PATH_INFO'][11:]
        isLeader = False
        print('Registered Leader Host:' + leaderhost)
    elif environ['PATH_INFO'].startswith("/getleader"):
        response_body = leaderhost

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
