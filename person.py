import random


class Person:
    def __init__(self, init, ave, step):
        self.speed = init
        self.ave = ave
        self.step = step

    def changeSpeed(self, now):
        if now < self.ave:
            self.speed += self.step*random.random()
        else:
            self.speed -= self.step*random.random()
