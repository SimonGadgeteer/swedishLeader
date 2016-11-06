# swedishLeader
Implementation of the swedish leadership voting algorithm in Python3

A remote kv-store is used for registration of (new) nodes. Every node registers it self upon first creation.
For voting a leader the swedish leadership voting algorith is used. This means, every node will flip a coin and, if passed, will take part in the next voting round until no other nodes are left. The last node is the leader. If every node loses in a round, that round is repeated again.
The leader henceforth is responsible to syncronize the stored key value between the independent nodes.