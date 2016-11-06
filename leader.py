import urllib.request
from random import randint

def getNodeList():
    try:
        response = urllib.request.urlopen(
            'http://isprot-registry.appspot.com/registry/touriste1')
        registerResponse = response.read().decode('UTF-8')

        if registerResponse.startsWith('Participants'):
            return registerResponse[13:].split(",")
        else:
            return False

    except Exception as e:
        print("Error registering: ", e)

def vote():
    return randint(0,1)

def election():
    return 'leader'