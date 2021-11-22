from random import random
from sys import setswitchinterval
from distance import get_distance_wgs84


class Region:
    MAX = 0.0001

    def __init__(self, args):
        self.posH = args[0][0]
        self.posV = args[0][1]
        self.spanH = -args[1][0]+args[0][0]
        self.spanV = args[1][1]-args[0][1]

    def verify(self, args):
        previous = (0, 0)
        for point in args:
            if get_distance_wgs84(previous[1], previous[0], point[1], point[0]) < 15:
                return False
            previous = point
        return True

    def shuffleFix(self):
        self.FIXH = self.MAX*(random()-0.5)
        self.FIXV = self.MAX*(random()-0.5)

    def keepInBound(self, args):
        fixh = self.MAX*random()/2
        fixv = self.MAX*random()/2
        if args[0] < self.posH-self.spanH:
            args[0] = self.posH-self.spanH+fixh
        if args[0] > self.posH:
            args[0] = self.posH-fixh
        if args[1] < self.posV:
            args[1] = self.posV+fixv
        if args[1] > self.posV+self.spanV:
            args[1] = self.posV+self.spanV-fixv
        return(args[0], args[1])

    def getDivision(self, num):
        result = []
        ave = num//4
        switch = {0: (self.posV+self.spanV)/ave, 1: (self.posH -
                                                     self.spanH)/ave, 2: (self.posV)/ave, 3: (self.posH)/ave}
        self.shuffleFix()
        now = [self.posH+self.FIXH, self.posV+self.FIXV]
        now = list(self.keepInBound(now))
        for i in range(num):
            result.append([now[0], now[1]])
            self.shuffleFix()
            if i % ave == 0:
                footstep = switch[i / ave]-now[not i / ave % 2] / ave
            now[0] += (i//ave % 2)*footstep+self.FIXH
            now[1] += (not i//ave % 2)*footstep+self.FIXV
            now = list(self.keepInBound(now))
        if self.verify(result):
            return result
        else:
            return self.getDivision(num)
# 下一步计划区域脱出保护机制
