#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep, time
import random
import copy


class Particle:
    def __init__(self, location=0, weight=2, dir=0):
        self.location = location
        self.dir = dir
        self.weight = weight


def move_function():
    global dir
    if ts.value() == 1:
        dir = dir * -1
    m.run_to_rel_pos(position_sp=-dir * 79, speed_sp=50)
    sleep(2)
    m.stop(stop_action="hold")
    sleep(2)
    return dir


def sensor_read():
    color1 = cl.value()
    if color1 <= 20:
        color = 1
    else:
        color = 0
    return color


def check(part):
    tmpp = part[0]
    a = 0
    b = 0
    for p in part:
        a = 0
        b = 0
        if p.location == tmpp.location:
            b = 1
        if p.dir == tmpp.dir:
            a = 1
        if a + b != 2:
            print("False")
            return False
    print("True")
    return True


def funcrand(N, part, w):
    samples = [i for i in range(N)]
    r = 0
    temp = 0
    for i in range(N):
        r = random.random()
        temp = 0
        for j in range(len(part)):
            temp += w[j]
            if (temp > r):
                samples[i] = copy.deepcopy(part[j])
                break
    return samples


###############################
##########   MAIN   ###########
###############################
random.seed()

ts = TouchSensor('in4')
cl = ColorSensor('in1')
m = LargeMotor('outA')
cl.mode = 'COL-REFLECT'

MinVal = 0
MaxVal = 17
l = 40
dir = -1
c = 0
k = 0
a = 0
random.seed()

karta = []
kfile = open('map.txt')
for st in kfile:
    karta.append(int(st))
part = []

for st in karta:
    part.append(Particle(a, 0, 1))
    part.append(Particle(a, 0, -1))
    a += 1

per = 0
summ = 0
sens = 0
it = 0
while not check(part):
    per = move_function()
    sens = sensor_read()
    summ = 0.0
    for p in part:
        p.weight = 0.0
        p.location += per * p.dir

        if p.location >= len(karta) or p.location < 0:
            p.weight = 0.0
        elif sens == karta[p.location]:
            p.weight = 1.0
        else:
            p.weight = 0.0
        summ = summ + p.weight
    for p in part:
        if summ == 0:
            Sound.speak('Error')
            exit()
        p.weight = p.weight / summ
    for p in part:
        print(p.location, p.weight)
    N = 2 * len(karta)
    weight = [p.weight for p in part]
    part = funcrand(N, part, weight)
    it += 1

Sound.speak(str(part[0].location))
sleep(2)
if part[0].dir == 1:
    Sound.speak('back')
if part[0].dir == -1:
    Sound.speak('forward')
answer = open('answer.txt', 'w')
answer.write(str(part[0].location))
answer.write(it)
answer.close