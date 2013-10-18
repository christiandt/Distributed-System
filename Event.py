__author__ = 'christue'


class Event(object):

    def __init__(self, time, replicaID, operation):
        self.time = int(time)
        self.replicaID = int(replicaID)
        self.operation = str(operation)