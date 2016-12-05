import register_usage
import leader
import threading

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

values = {}

def storeValues(key, value, registerUsage, localhost, localport):
    listValue = list(value)
    hosts = leader.getNodeList()

    nr = 0
    for host in hosts:
        length = int(round(len(listValue) / len(hosts)))

        if nr != (len(hosts) - 1):
            shardValue = listValue[nr*length : (nr*length + length)]
        else:
            shardValue = listValue[nr*length : len(listValue)]

        nr = nr + 1

        if host.strip() != localhost + ':' + str(localport):
            urlopen('http://' + host.strip() + '/sync/' + key + '=' + str(shardValue).strip('[]'))

        print(shardValue + " : "+host)

    return "I'll store "+key+" with the value "+value



def getValues():
    return

def notifyLeader(leader, key, value):
    return

def syncAll(key, value, localhost, localport):
    return

def geturl(url):
    return