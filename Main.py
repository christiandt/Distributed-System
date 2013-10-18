__author__ = 'Christian D. Tuen'

from Replica import *
from Transmission import *
from Event import *
import re

replicas_num = 3
replicas = [Replica(replicas_num) for i in range(replicas_num)]
network = dict()
transmissionCounter = 1


def increment(replicaID, key, countingEvent):
    replicaID -= 1
    if replicaID < len(replicas):
        replica = replicas[replicaID]
    else:
        return
    if key in replica.keys:
        replica.keys[key] += 1
    else:
        replica.keys[key] = 1
    if countingEvent:
        replica.timeTable[replicaID][replicaID] += 1
        event = Event(replica.timeTable[replicaID][replicaID], replicaID, "increment(%s)" % key)
        replica.log.append(event)


def decrement(replicaID, key, countingEvent):
    replicaID -= 1
    if replicaID < len(replicas):
        replica = replicas[replicaID]
    else:
        return
    if key in replica.keys:
        replica.keys[key] -= 1
    else:
        replica.keys[key] = -1
    if countingEvent:
        replica.timeTable[replicaID][replicaID] += 1
        event = Event(replica.timeTable[replicaID][replicaID], replicaID, "decrement(%s)" % key)
        replica.log.append(event)


def getValue(replicaID, key):
    replicaID -= 1
    if replicaID < len(replicas):
        replica = replicas[replicaID]
    else:
        return
    if key in replica.keys:
        print replica.keys[key]
    else:
        print None


def printState(replicaID):
    replicaID -= 1
    if replicaID < len(replicas):
        replica = replicas[replicaID]
    else:
        return
    print "Log: ", [event.operation for event in replica.log]
    print "TimeTable:"
    for line in replica.timeTable:
        print line


def hasrec(timeTable, event, replicaID):
    return timeTable[replicaID][event.replicaID] >= event.time


def sendLog(sourceReplicaID, destReplicaID):
    sourceReplicaID -= 1
    destReplicaID -= 1
    global transmissionCounter
    if sourceReplicaID < len(replicas):
        replica = replicas[sourceReplicaID]
    else:
        return
    log = []
    for event in replica.log:
        if not hasrec(replica.timeTable, event, destReplicaID): log.append(event)
    transmission = Transmission(sourceReplicaID, destReplicaID, replica.timeTable, log)
    transmissionNumber = transmissionCounter
    network[transmissionNumber] = transmission
    transmissionCounter += 1
    print transmissionNumber


def receiveLog(transmissionNumber):
    if transmissionNumber in network:
        transmission = network[transmissionNumber]
    else:
        return
    receiver = replicas[transmission.destination]
    receivedTable = transmission.timeTable
    localTable = receiver.timeTable
    receivedLog = transmission.log
    for event in receivedLog:
        if not hasrec(localTable, event, transmission.destination):
            receiver.log.append(event)
            executeEvent(transmission.destination, event)
    for i in range(len(localTable)):
        localTable[transmission.destination][i] = max(localTable[transmission.destination][i], receivedTable[transmission.source][i])
        localTable[i] = [max(received, local) for received, local in zip(receivedTable[i], localTable[i])]
    #Garbage-collect:
    for event in receiver.log:
        replicas_with_event = 0
        for i in range(len(replicas)):
            if hasrec(receiver.timeTable, event, i): replicas_with_event += 1
        if replicas_with_event >= replicas_num: receiver.log.remove(event)


def executeEvent(replicaID, event):
    array_input = re.split("[()]", event.operation)
    if len(array_input) == 3:
        process = array_input[0]
        key = array_input[1]
        if process == "increment": increment(replicaID+1, key, False)
        elif process == "decrement": decrement(replicaID+1, key, False)


def demo():
    print '> increment(1, "X")'
    increment(1, "X", True)
    print '> getValue(1, "X")'
    getValue(1, "X")
    print '> getValue(2, "X")'
    getValue(2, "X")
    print '> printState(1)'
    printState(1)
    print '> sendLog(1, 2)'
    sendLog(1, 2)
    print '> increment(1, "Y")'
    increment(1, "Y", True)
    print '> printState(2)'
    printState(2)
    print '> receiveLog(1)'
    receiveLog(1)
    print '> printState(2)'
    printState(2)
    print '> getValue(2, "X")'
    getValue(2, "X")

def replicaTest():
    print 'increment(1, "X")'
    increment(1, "X", True)
    print 'increment(3, "X")'
    increment(3, "X", True)
    print 'sendLog(1,2)'
    sendLog(1, 2)
    print 'receiveLog(1)'
    receiveLog(1)
    print 'increment(1, "Y")'
    increment(1, "Y", True)
    print 'sendLog(1,3)'
    sendLog(1, 3)
    print 'receiveLog(2)'
    receiveLog(2)
    print 'sendLog(3,2)'
    sendLog(3, 2)
    print 'sendLog(3,2)'
    sendLog(3, 2)
    print 'receiveLog(3)'
    receiveLog(3)
    print 'receiveLog(4)'
    receiveLog(4)
    print 'printState(1)'
    printState(1)
    print 'printState(2)'
    printState(2)
    print 'printState(3)'
    printState(3)

demo()