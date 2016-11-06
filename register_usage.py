import requests, json

def registerUsage():
    url = "http://160.85.4.89:4567/data"
    data = {'_class': 'Storage', 'account': 'gruppeasdf', 'unit': 'pair', 'usage':1}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)