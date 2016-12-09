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
    listValue = list(value)
    hosts = leader.getNodeList()
    print(str(hosts))

    nr = 0
    for host in hosts:
        length = int(round(len(listValue) / len(hosts)))

        if nr != (len(hosts) - 1):
            shardValue = listValue[nr*length : (nr*length + length)]
        else:
            shardValue = listValue[nr*length : len(listValue)]

        shardValue = str(nr) + ''.join(shardValue)
        nr = nr + 1

        if host.strip() != localhost + ':' + str(localport):
            url = 'http://' + host.strip() + '/sync/' + key + '=' + shardValue
            threading.Thread(target=urlopen, args=(url,)).start()
        else:
            values[key] = shardValue

    return "I'll store "+key+" with the value "+value

def syncValue(key, value):
    values[key] = value


def getValue():
    return

def getValues():
    return str(values)

def notifyLeader(leader, key, value):
    return

def syncAll(key, value, localhost, localport):
    # Do nothing, no leader needed on shardStore
    return

def geturl(url):
    return