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

def storeValues(key, value, registerUsage):
    return

def getValues():
    return

def notifyLeader(leader, key, value):
    return

def syncAll(key, value, localhost, localport):
    return

def geturl(url):
    return