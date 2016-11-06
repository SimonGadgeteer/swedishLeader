port = 8080
host = ''

import urllib.request

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
    ctype = "text/plain"
    status = "200 OK"

    if environ['PATH_INFO'].startswith("/store"):
        return store.application(environ, start_response)
    elif environ['PATH_INFO'].startswith("/leader"):
        return True
        if environ['PATH_INFO'].startswith("/leader/vote"):
            start_response(status, "('Content-Type', ctype)")
            return vote()
    else:
        start_response("400", "('Content-Type', ctype)")


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
# while True:
#    print("waiting")
#    httpd.handle_request()
