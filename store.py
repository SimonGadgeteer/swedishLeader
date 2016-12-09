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

def storeValues(key, value, localhost, localport):
    print("I'll store "+key+" with the value "+value)
    values[key] = value

    # threading.Thread(target=register_usage.registerUsage, args=()).start()

    print("the store now looks like this: "+str(values))

    return "I'll store "+key+" with the value "+value

def syncValue(key, value):
    values[key] = value

def getValues():
    return str(values)

def getValue(key):
    return values[key]

def notifyLeader(leader, key, value):
    url = 'http://' + leader + '/sync/' + key + '=' + value
    threading.Thread(target=geturl, args=(url,)).start()

def syncAll(key, value, localhost, localport):
    hosts = leader.getNodeList()
    for host in hosts:
        if host.strip() != localhost + ':' + str(localport):
            urlopen('http://' + host.strip() + '/sync/' + key + '=' + value)

def geturl(url):
    urlHandler = urlopen(url)