__author__ = 'Christian D. Tuen'

from Replica import *
from Transmission import *
from Event import *
import re
import sys

replicas_num = 3    #The number of replicas that should be created
replicas = [Replica(replicas_num) for i in range(replicas_num)]
network = dict()
transmissionCounter = 1


def increment(replicaID, key, countingEvent):
    """
    Increments the value of a specific key

    :param replicaID: The ID of the replica that should increment
    :param key: The key that should be incremented
    :param countingEvent: Is this an event that increments the local clock,
        and gets added to the log?
    """
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
    """
    Decrements the value of a specific key

    :param replicaID: The ID of the replica that should decrement
    :param key: The key that should be decremented
    :param countingEvent: Is this an event that increments the local clock,
        and gets added to the log?
    """
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
    """
    Prints the numeric value of a specific key on in a specific replica

    :param replicaID: The ID of the replica
    :param key: The key who's value should be printed
    """
    replicaID -= 1
    if replicaID < len(replicas):
        replica = replicas[replicaID]
    else:
        return
    if key in replica.keys:
        print replica.keys[key]
    else:
        print "null"


def printState(replicaID):
    """
    Prints the log and timetable of the given replica

    :param replicaID: The ID of the replica
    """
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
    """
    Checks whether or not the replica has a given event.

    :param timeTable: The TimeTable
    :param event: The event
    :param replicaID: The replicas ID
    :return: Boolean value
    """
    return timeTable[replicaID][event.replicaID] >= event.time


def sendLog(sourceReplicaID, destReplicaID):
    """
    Creates a transmission-object containing the source ID, destination ID,
    timetable and log.

    :param sourceReplicaID: The ID of the transmitting replica
    :param destReplicaID: The ID of the receiving replica
    """
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
    """
    Receives any specific previously sent messages, identified by the transmission
    number

    :param transmissionNumber: The transmission number received from sendLog
    """
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
    """
    Executed the given event without it counting as an activity in the local clock

    :param replicaID: The Replica that will execute the event
    :param event: The event to be executed
    """
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


def garbageTest():
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


def user_input():
    """
    A simple, command based, user interface
    """
    try:
        array_input = re.split("[()]", raw_input())
    except TypeError:
        print "Illegal Input"
    else:
        if len(array_input) == 3:
            process = array_input[0]
            key = array_input[1]
            if "," in key:
                array_input = [x.strip().strip('""') for x in key.split(',')]
                if len(array_input) == 2:
                    value1 = int(array_input[0])
                    value2 = str(array_input[1])
                    if process == "Increment": increment(value1, value2, True)
                    elif process == "Decrement": decrement(value1, value2, True)
                    elif process == "getValue": getValue(value1, value2)
                    elif process == "SendLog": sendLog(value1, int(value2))
                    else: print "Illegal Input"
                else:
                    print "Illegal Input"
            else:
                if process == "Demo": demo()
                elif process == "GarbageDemo": garbageTest()
                elif process == "End": sys.exit()
                elif process == "PrintState": printState(int(key))
                elif process == "ReceiveLog": receiveLog(int(key))
                else: print "Illegal Input"
        else:
            print "Illegal Input"


while True:
    user_input()