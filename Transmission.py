__author__ = 'Christian D. Tuen'

import copy


class Transmission(object):

    def __init__(self, source, destination, timeTable, log):
        self.source = int(source)
        self.destination = int(destination)
        self.timeTable = copy.deepcopy(timeTable)
        self.log = copy.deepcopy(log)