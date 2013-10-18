__author__ = 'Christian D. Tuen'


class Replica(object):

    def __init__(self, replicas_num):
        self.timeTable = [[0]*replicas_num for i in range(replicas_num)]
        self.clock = 0
        self.log = []
        self.keys = dict()