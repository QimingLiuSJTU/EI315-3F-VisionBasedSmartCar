import cv2 
import numpy as np
from driver import driver

def get_direction_err(err_array):
    
    err = 0
    ################
    #5个误差的权系数#
    ################
    err_count = [0.5, 0.3, 0.2, 0.1, 0.05]
    for i in range(len(err_array)):
        if err_array[i] != None:
            err += err_count[i] * err_array[i]

    return err

#对控制数据的范围进行控制(-1,1)
def constrain(data):
    if data >= 1:
        data = 1
    if data <= -1:
        data = -1
    return data



d = driver() #实体化类
d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
speed_P = 1
speed_I = 0
speed_D = 0
    
speed_err = 0
last_speed_err = 0
speed_err_sum = 0
speed_err_diff = 0
    
    #转向控制部分的参数
steer_P = 2
steer_I = 0
steer_D = 0
    
direction_err = 0
last_direction_err = 0
direction_err_sum = 0
direction_err_diff = 0
    
    #############################
    #Default speed and direction#
    #############################
    #默认参考速度和参考转向
expected_speed = 0.25
expected_steer = 0

d.setStatus(mode="speed") #设置处于速度模式
        
        #初始化控制量
speed = steer = 0

cap = cv2.VideoCapture(1)
while True:
    if cap.isOpened():
        _, frame = cap.read()
    else:
        continue
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, frame = cv2.threshold(frame, 80, 255, cv2.THRESH_BINARY_INV)
    rows, cols = frame.shape
    src_points = np.float32([[555,185],[85,185],[cols-1,0],[0,0]])
    dst_points = np.float32([[0,0],[cols-1,0],[210,rows-1],[430,rows-1]])

    projective_martix = cv2.getPerspectiveTransform(src_points,dst_points)
    frame = cv2.warpPerspective(frame,projective_martix,(cols,rows))
    
    cv2.imshow("capture", frame)
    cv2.waitKey(1)

    # frame = cv2.Canny(frame, 50, 120)
    '''
    seeds = np.where(frame[479] == 255)[0]
    seedMark = np.zeros(frame.shape)
    seedList = []
    for seed in seeds:
        seedList.append((479,seed))
    connects = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, 0), (1, -1), (1, 1)]

    while(len(seedList)>0):
        currentPoint = seedList.pop(0)
        for i in range(8):
            tmpX = currentPoint[0] + connects[i][0]
            tmpY = currentPoint[1] + connects[i][1]
            if tmpX < 0 or tmpY < 0 or tmpX >= 480 or tmpY >= 640:
                continue
            if frame[tmpX,tmpY] == 255 and seedMark[tmpX,tmpY] == 0:
                seedMark[tmpX,tmpY] = 255
                seedList.append((tmpX,tmpY))
                continue
    '''

    pos = 400
    black_count = 0
    while(black_count == 0):
        color = frame[pos].flatten()
        pos -= 5
        black_count = np.sum(color == 255)
    black_index = np.where(color == 255)
    center = np.sum(black_index) / black_count
    deviation = 350 - center


    direction_err = deviation / 150
    direction_err_sum = direction_err_sum + direction_err
    print(direction_err, direction_err_sum)
    direction_err_diff = direction_err - last_direction_err
    last_direction_err = direction_err
    
    if(deviation > 50):
        expected_speed = 0.2
        steer_P = 0.75
        steer_I = 0
        steer_D = 0
    else:
        expected_speed = 0.25
        steer_P = 1.2
        steer_I = 0
        steer_D = 0

    steer = constrain(expected_steer + steer_P * direction_err + steer_I * direction_err_sum + steer_D * direction_err_diff)
    speed = constrain(expected_speed + speed_P * speed_err + speed_I * speed_err_sum + speed_D * speed_err_diff )

    d.setStatus(motor = speed, servo = steer)



    '''
    deviationList = []
    for i in range(5):
        position = 470 - 40 * i
        color = frame[position].flatten()
        black_count = np.sum(color == 255)
        black_index = np.where(color == 255)
        center = np.sum(black_index) / black_count
        deviation = 320 - center
        deviationList.append(deviation)

    
    print(deviation)

    err_array = deviationList
            
    #转向PID变量更新
    direction_err = get_direction_err(err_array)
    direction_err_sum = 0.1 * direction_err_sum + direction_err
    direction_err_diff = direction_err - last_direction_err
    last_direction_err = direction_err
            
    #速度PID变量更新
    speed_err = get_speed_err()
    speed_err_sum = 0.1 * speed_err_sum + speed_err
    speed_err_diff = speed_err - last_speed_err
    last_speed_err = speed_err
    
            
            #根据PID在expected基础上调整控制量
    steer = constrain(expected_steer + steer_P * direction_err + steer_I * direction_err_sum + steer_D * direction_err_diff)
    speed = constrain(expected_speed + speed_P * speed_err + speed_I * speed_err_sum + speed_D * speed_err_diff )
            
            
            #控制小车啦~~~
    d.setStatus(motor = speed, servo = steer)
    '''

cap.release()

