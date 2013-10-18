Distributed-System
==================
A simple implementation of a distributed system and the replicated log problem. A mock network is simulated using the Transmission-class and Network-array.
Run Main.py and start typing one of the following commands:
Increment(replicaID, key)
Decrement(replicaID, key)
getValue(replicaID, key)
PrintState(replicaID)
SendLog(sourceReplicaID, destinationReplicaID)
ReceiveLog(transmissionID)


## Test-input:

    Increment(1, "X")
    getValue(1,"X")
    getValue(2,"X")
    PrintState(1)
    SendLog(1,2)
    Increment(1, "Y")
    PrintState(2)
    ReceiveLog(1)
    PrintState(2)
    getValue(2,"X")