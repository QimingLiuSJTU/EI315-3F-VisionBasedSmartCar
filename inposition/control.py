import cv2 as cv
import numpy as np
from driver import driver
import time

cap = cv.VideoCapture(0)
ss = 0.07

def sleep(mytime = 1):
    start = time.time()
    end = time.time()
    while (end - start) * 1000 < mytime:
        if cap.isOpened():
            _,frame = cap.read()
        end = time.time()
        

def SeeNothing(d, jud):
    if jud == 0:
        print("Now see nothing, go ahead")
        steer = 0
        speed = 0.05
        d.setStatus(motor = speed, servo = steer-ss)
        sleep(2000)
        speed = 0
        d.setStatus(motor = speed, servo = steer-ss)
        d.setStatus(motor = 0, servo = 0)
        return 0
    else:
        print("Now see nothing, go back")
        steer = 0
        speed = -0.05
        d.setStatus(motor = speed, servo = steer-ss)
        sleep(1000)
        speed = 0
        d.setStatus(motor = speed, servo = steer-ss)
        d.setStatus(motor = 0, servo = 0)
        return 1

def InCarPosition(d):
    print("Now parking in position")
    # 进入车位，正着倒车
    steer = 0
    speed = -0.05
    d.setStatus(motor = speed, servo = steer-ss)
    sleep(5000)
    steer = 0
    speed = 0
    d.setStatus(motor = speed, servo = steer-ss)
    sleep(1000)
    # 出车位
    print("Now get out of car position")
    steer = 0
    speed = 0.05
    d.setStatus(motor = speed, servo = steer-ss)
    sleep(2300)
    # 开始转弯，对准下一个车库
    steer = 0.99
    speed = 0.05
    d.setStatus(motor = speed, servo = steer)
    sleep(5000)
    steer = -0.99
    speed = 0.05
    d.setStatus(motor = speed, servo = steer)
    sleep(5000)
    steer = 0
    speed = 0.05
    d.setStatus(motor = speed, servo = steer-ss)
    sleep(500)
    d.setStatus(motor = 0, servo = 0)
    return 1

def AdTilt(d, Degree = 0):
    print("Now adjust tilt")
    steer = 0.99 * Degree / abs(Degree)
    speed = -0.05
    d.setStatus(motor = speed, servo = steer)
    sleep(abs(Degree) * 2000)
    d.setStatus(motor = 0, servo = 0)
    return 0

def AdShift(d, ShiftDis = 0):
    print("Now adjust distance shift")
    steer = -0.8 * ShiftDis / abs(ShiftDis)
    speed = -0.05
    d.setStatus(motor = speed, servo = steer)
    sleep(2400)
    # sleep(abs(ShiftDis) * 25)

    steer = 0.8 * ShiftDis / abs(ShiftDis)
    speed = -0.05
    d.setStatus(motor = speed, servo = steer)
    sleep(2200)
    #sleep(abs(ShiftDis) * 25)
    d.setStatus(motor = 0, servo = 0)
    return 0

def AllRight(d):
    print("parking position corrected, just go back")
    steer = 0
    speed = -0.05
    d.setStatus(motor = speed, servo = steer-ss)
    sleep(500)
    d.setStatus(motor = 0, servo = 0)
    return 0


def Rejected(d):
    print("adjust failed, park again")
    steer = 0
    speed = 0.05
    d.setStatus(motor = speed, servo = steer)
    sleep(7000)
    d.setStatus(motor = 0, servo = 0)
    return 1