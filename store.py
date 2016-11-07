import register_usage
import urllib.request
import leader
import threading

values = {}

def storeValues(key, value, registerUsage):
    print("I'll store "+key+" with the value "+value)
    values[key] = value
    if registerUsage == True:
        register_usage.registerUsage()
    print("the store now looks like this: "+str(values))

    return "I'll store "+key+" with the value "+value

def getValues():
    return str(values)

def notifyLeader(leader, key, value):
    url = 'http://' + leader + '/sync/' + key + '=' + value
    threading.Thread(target=geturl, args=(url,)).start()

def syncAll(key, value, localhost, localport):
    hosts = leader.getNodeList()
    for host in hosts:
        if host.strip() != localhost + ':' + str(localport):
            urllib.request.urlopen('http://' + host.strip() + '/sync/' + key + '=' + value)

def geturl(url):
    urlHandler = urllib.request.urlopen(url)