import register_usage
import urllib.request
import leader

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
    response = urllib.request.urlopen('http://' + leader + '/sync/' + key + '=' + value)

def syncAll(key, value, localhost, localport):
    hosts = leader.getNodeList()
    for host in hosts:
        if host.strip() != localhost + ':' + str(localport):
            urllib.request.urlopen('http://' + host.strip() + '/sync/' + key + '=' + value)