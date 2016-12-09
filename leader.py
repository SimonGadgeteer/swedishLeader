import json
config = json.load(open('config.json'))

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
from random import randint

def getNodeList():
    global config

    try:
        response = urlopen(config['hostsRegistry'])
        registerResponse = response.read().decode('UTF-8')

        if registerResponse.startswith('Participants'):
            return set(registerResponse[14:].split(","))
        else:
            return False

    except Exception as e:
        print("Error registering: ", e)
        return False

def vote():
    return randint(0,1)

def election(localhost, port):
    hosts = getNodeList()
    elected = False
    hostlist = hosts

    while elected != True:
        electedHosts = []

        for host in hostlist:
            try:
                if host.strip() != localhost + ':' + str(port):

                    response = urlopen('http://' + host.strip() + '/leader/vote')
                    response = int(response.read().decode('UTF-8'))
                else:
                    response = int(vote())

                if response == 1:
                    electedHosts.append(host)

            except Exception as e:
                print("Error calling vote: ", e, 'http://' + host.strip() + '/leader/vote')

        if len(electedHosts) == 1:
           elected = True
        elif len(electedHosts) != 0:
            hostlist = electedHosts

    for host in hosts:
        if host.strip() != localhost + ':' + str(port):
            response = urlopen('http://' + host.strip() + '/newleader/' + electedHosts[0].strip())

    return electedHosts[0].strip()