# -*- coding: utf-8 -*-
"""
Created on Tue May 14 19:10:02 2019

@author: Administrator
"""
import numpy as np
import cv2 as cv
import time
from driver import driver
from func import *
from control import *

#从摄像头获取照片
def get_frame(cap):

     while True:
          if cap.isOpened():
               _,frame = cap.read()
               print('---------------')
               #cv.imshow("ss", frame)
               #cv.waitKey(1)
               break
          else:
               continue
     return frame

#决定要倒那个车库，1，2，3，4
state = 1

#一个倒车过程的子状态, 
# 1-检测后方是否有看到数字
# 2-未检测到后方有数字，向后退直到看到数字
# 3-检测到后方有数字，进入角度调整状态
# 4-角度平行之后，进行位置调整状态
# 5-位置调整结束，进入直接后退状态
# 6-后退结束，出车库
# 

sub_state = 1

#实体化类
d = driver() 
d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
d.setStatus(mode = "speed")
#控制量
speed = 0.05
steer = 0
jud = 1
#开启摄像头


while (state < 5):
     print('state', state)
     #检测后方是否有看到数字
     frame = get_frame(cap)
     contours = dip(frame)
     number_judge = len(contours) != 0
     if number_judge:
         num_list = num_recognition(contours, state)
         ret = cal(state, num_list, contours)
         if ret is None:
             number_judge = False
         else:
             coor = ret[0]
             angle = -(ret[1] + 0.1)
             shift = 300 - coor[0]
             print("angle =", angle, ", shift =", shift)

     if not number_judge:
        jud = SeeNothing(d, jud)
        continue
          
     
     if coor[1] < 300:
          if abs(shift) > 20:
               jud = AdShift(d, shift)
               continue
          AllRight(d)
          continue
     else:
          if abs(shift) > 20:
               jud = Rejected(d)
               continue
          else:
               jud = InCarPosition(d)
               state += 1
               continue
cap.release()