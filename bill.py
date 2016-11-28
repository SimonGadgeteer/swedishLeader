import requests, json

def create():
    url = "http://160.85.4.89:4567/command"
    data = {'_class': 'BillRequest', 'account': "gruppeasdf", 'from': 0, 'to':1514764799}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
