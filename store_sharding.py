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

    # threading.Thread(target=register_usage.registerUsage, args=()).start()

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

def getValue(key):
    return values[key]

def getValues(localhost, localport):
    hosts = leader.getNodeList()
    message = ''

    for key, value in values.items():
        nr = int(value[0:1])
        value = value[1:]

        if len(message) > 0:
            message = message + ', '

        for host in hosts:
            if host.strip() != localhost + ':' + str(localport):
                url = 'http://' + host.strip() + '/getvalue/' + key
                response = urlopen(url)

                tmpValue = response.read().decode('UTF-8')
                tmpNr = int(tmpValue[0:1])
                tmpValue = tmpValue[1:]

                if(tmpNr > nr):
                    value = value + tmpValue
                else:
                    value = tmpValue + value

                nr = tmpNr

        message = message + key + '=' + value


    return message

def notifyLeader(leader, key, value):
    return

def syncAll(key, value, localhost, localport):
    # Do nothing, no leader needed on shardStore
    return

def geturl(url):
    return