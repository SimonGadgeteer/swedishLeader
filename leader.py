import urllib.request
from random import randint

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
