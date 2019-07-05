import cv2 as cv
import math
import numpy as np
from functools import cmp_to_key

cameraMatrix = np.array([[341.1772, 0.0136, 319.2622],
                [0, 341.5543, 243.6391],
                [0, 0, 1]])

distCoeffs = np.array([-0.2898, 0.0634, -0.00029521, -0.00078580, 0])


def cmp(obj1: list, obj2: list) -> int:
    """
    按照横坐标对轮廓排序
    :param obj1: 待排序的轮廓
    :param obj2: 待排序的轮廓
    :return: 比较值
    """
    my_m = cv.moments(obj1)
    cx1 = int(my_m['m10'] / my_m['m00'])
    my_m = cv.moments(obj2)
    cx2 = int(my_m['m10'] / my_m['m00'])
    if cx1 > cx2:
        return 1
    elif cx1 < cx2:
        return -1
    else:
        return 0


def num_recognition(contours: list, num: int) -> list:
    """
    数字识别
    :param contours: 当前图像中找到的轮廓
    :param num: 待寻找的数字
    :return: 当前轮廓代表的数字列表
    """
    '''
    if cv.arcLength(contours[0], True) < 250:
        num_list = list(range(1, len(contours) + 1))
    elif cv.arcLength(contours[-1], True) < 250:
        num_list = list(range(5 - len(contours), 5))
    elif len(contours) == 2:
        num_list = [2, 3]
    else:
        num_list = [num]
    '''
    mine =  10000
    num_list = []
    idx = None
    for i in range(len(contours)):
        my_m = cv.moments(contours[i])
        cx1 = abs(int(my_m['m10'] / my_m['m00']) - 300)
        if cx1 < mine:
            mine = cx1
            idx = i
    for i in range(idx):
        num_list.append(num - idx + i)
    for i in range(idx, len(contours)):
        num_list.append(num - idx + i)
    print(num_list)
    for it in contours:
        my_m = cv.moments(it)
        cx1 = int(my_m['m10'] / my_m['m00'])
        print(cx1)
    return num_list


def dip(img: np.ndarray) -> list:
    """
    处理图像
    :param img: 待处理图像
    :return: 筛选后的轮廓
    """
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (w,h), 1, (w,h))
    frame = cv.undistort(img, cameraMatrix, distCoeffs, None, newcameramtx)
    x, y, w, h = roi
    img = frame[y : y+h, x : x+w]
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, thresh = cv.threshold(gray, 110, 255, cv.THRESH_BINARY_INV)

    rows,cols = thresh.shape
    src_points = np.float32([[85,250],[529,250],[0,rows-1],[cols-1,rows-1]])
    dst_points = np.float32([[0,0],[cols-1,0],[180,rows-1],[434,rows-1]])

    projective_martix = cv.getPerspectiveTransform(src_points,dst_points)
    thresh = cv.warpPerspective(thresh,projective_martix,(cols,rows))


    kernel = np.ones((7, 7), np.uint8)
    thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
    im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    temp = []
    for i in contours:
        if 150 < cv.arcLength(i, True) < 390 and 150 < i.shape[0] < 400:
            area = cv.contourArea(i)
            x, y, w, h = cv.boundingRect(i)
            rect_area = w * h
            extent = float(area) / rect_area
            if 0.2 < extent < 0.6:
                my_m = cv.moments(i)
                cx1 = int(my_m['m10'] / my_m['m00'])
                if 50 < cx1 < 550:
                    temp.append(i)
    temp = sorted(temp, key=cmp_to_key(cmp))
    cv.imshow("ss", thresh)
    cv.waitKey(1)

    return temp


def cal(num: int, num_list: list, contours: list) -> tuple:
    """
    计算车位的位置和车位与车身的角度
    :param num: 车位编号
    :param num_list: 图像中识别的数字列表
    :param contours: 轮廓
    :return: 包含坐标列表和角度的元组
    """
    if num not in num_list:
        return None
    idx = num_list.index(num)
    angle = 0
    m = cv.moments(contours[idx])
    cx = int(m['m10'] / m['m00'])
    cy = int(m['m01'] / m['m00'])
    '''
    for it in range(len(contours) - 1):
        m1 = cv.moments(contours[it])
        m2 = cv.moments(contours[it + 1])
        x1 = int(m1['m10'] / m1['m00'])
        y1 = int(m1['m01'] / m1['m00'])
        x2 = int(m2['m10'] / m2['m00'])
        y2 = int(m2['m01'] / m2['m00'])
        angle += math.atan2(y2 - y1, x2 - x1)
        angle /= 2
    '''
    return (cx, cy), angle
