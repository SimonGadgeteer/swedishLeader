# swedishLeader
##Trivia
Implementation of the swedish leadership voting algorithm in Python3

A remote kv-store is used for registration of (new) nodes. Every node registers it self upon first creation.
For voting a leader the swedish leadership voting algorith is used. This means, every node will flip a coin and, if passed, will take part in the next voting round until no other nodes are left. The last node is the leader. If every node loses in a round, that round is repeated again.
The leader henceforth is responsible to syncronize the stored key value between the independent nodes.

*This implementation uses a random port number (which will be displayed)*
*exmaple installation: `http://swedish.mybluemix.net`*


##Installation
1. clone the files with `git clone https://github.com/SimonGadgeteer/swedishLeader.git`

2. run the app with `python app.py [port]`

3. your instance of the kv-store is now running


##Usage
###Store a KV
To store a KV in your local instance, use `yourhost:yourport/store/<yourKey>=<yourValue>`

##Storage
This implementation of a KV store uses sharding to distribute all your values equally between all available nodes. To configure this one has to change the `config.json` file (`"shard"` or `"full"`)

###Read all KVs
To get all your KVs, use `yourhost:yourport/store`

###Leader election
To vote for a new leader, use the following command `yourhost:yourport/store/leader`

###Billing
####Config
To change your Cyclopse data, modify the example information in `create_bill.py` and `create_udr.py`

####Usage
To create a bill for your usage, use

1. `yourhost:yourport/udr`
2. `yourhost:yourport/billing`
3. your bill is now created within your Cyclopse account

##API
There is also an api description file available to use. The file is written in the RAML format (api.raml).

##Docker
There is also a Docker image of the swedishLeader available:
`https://hub.docker.com/r/gruppeasdf/swedish_leader/`

The container is already running @ `https://swedish.mybluemix.net/`
