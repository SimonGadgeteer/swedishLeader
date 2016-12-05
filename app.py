#!/usr/bin/env python
import sys
import socket
import os

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

# probably no necessary --> remote kv store in use; import registry
import leader, store, store_sharding, udr, bill
from random import randint

valueStore = store_sharding

port = int(os.environ.get('VCAP_APP_PORT', '5050'))
host = os.environ.get('VCAP_APP_HOST', 'localhost')
isLeader = False
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
            response = urlopen('http://isprot-registry.appspot.com/registry/touriste11/' + hostname)
            registerResponse = response.read().decode('UTF-8')
        print(socket.gethostname())
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

        response_body = valueStore.storeValues(params[0], params[1], True)

        if isLeader == False:
            valueStore.notifyLeader(leaderhost, params[0], params[1])
        else:
            valueStore.syncAll(params[0], params[1], host, port)
        #return store.application(environ, start_response)

    elif environ['PATH_INFO'].startswith("/store"):
        response_body =  str(valueStore.getValues())
    elif environ['PATH_INFO'].startswith("/sync/"):
        params = environ['PATH_INFO'][6:]
        params = params.split('=')
        valueStore.storeValues(params[0], params[1], False)

        if isLeader == True:
            print('I Am leader')
            valueStore.syncAll(params[0], params[1], host, port)

    elif environ['PATH_INFO'].startswith("/leader"):
        if environ['PATH_INFO'].startswith("/leader/vote"):
            response_body = str(leader.vote())
            print(response_body)

        else:
            response_body = leader.election(host, port)
            leaderhost = response_body

            if leaderhost == host.strip() + ':' + str(port):
                isLeader = True
            else:
                isLeader = False

    elif environ['PATH_INFO'].startswith("/newleader/"):
        leaderhost = environ['PATH_INFO'][11:]
        isLeader = False
        if leaderhost == host.strip() + ':' + str(port):
            isLeader = True
        print('Registered Leader Host:' + leaderhost)
    elif environ['PATH_INFO'].startswith("/getleader"):
        response_body = leaderhost
    elif environ['PATH_INFO'].startswith("/udr"):
        createUDR()
    elif environ['PATH_INFO'].startswith("/billing"):
        createBill()

    else:
        response_body = 'It Works'



    response_body = response_body.encode('utf-8')
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]


def createUDR():
    udr.create()

def createBill():
    bill.create()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('', port, application)
    registerself(host, port)
    httpd.serve_forever()
