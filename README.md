# EI315-3F-VisionBasedSmartCar
 利用小车前后的RGB摄像头实现自动巡线和倒车入库功能。

## Description
  本项目利用树莓派以及前后摄像头控制小车进行巡线和倒车入库任务。巡线要求小车沿着白色地板上的黑色轨迹线行进，倒车任务要求小车依次倒车进入并列的1~4号车位。我们主要使用python-opencv进行图像处理，下位机控制代码driver.py进行电机控制。涉及到透视校正、桶形畸变校正、边缘提取、模板匹配等图像处理方法。<br>

## File Functions
**DemoVideo.mp4**: 演示视频<br>
**report.pdf**: 详细介绍了各功能的实现方法<br>
**followcurise/driver.py**: 电机控制依赖程序，每次运行程序前需要在terminal里使用 **./picarserver**启动下位机控制<br>
**followcurise/followcurise.py**: 巡线控制代码<br>
**inposition/camera_calibration**: 文件夹内是后置摄像头桶形畸变校正的相关文件，用MATLAB的畸变校正工具箱实现<br>
**inposition/driver.py**: 电机控制依赖程序，每次运行程序前需要在terminal里使用 **./picarserver**启动下位机控制<br>
**inposition/control.py**: 动作函数子文件<br>
**inposition/func.py**: 图像处理子文件<br>
**inposition/main.py**: 倒车入库主文件，其中调用了上方三个依赖文件<br>

## Project participant
赵寅杰、刘启明、严威豪 上海交通大学自动化系
