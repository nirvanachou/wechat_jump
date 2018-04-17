# -*- coding: utf-8 -*-
import os
import numpy
from PIL import Image
import matplotlib.pyplot as pyplot
from matplotlib.animation import FuncAnimation
import time

Image_update = True

def get_screen_picture():  # 获取屏幕截图
    os.system('adb shell screencap -p /sdcard/screen.png')  # 保存图片在SD卡
    os.system('adb pull /sdcard/screen.png')  # 下载图片到电脑
    return numpy.array(Image.open('screen.png'))


def jump_next(point1, point2):
    # 计算两点之间长度
    x1, y1 = point1
    x2, y2 = point2
    distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
    os.system('adb shell input swipe 320 410 320 410 {}'.format(int(distance*2.1)))  # 1.35


def on_click(event, locate=[]):  # 鼠标选定跳的位置
    global Image_update
    locate.append((event.xdata, event.ydata))
    if len(locate) == 2:
        jump_next(locate.pop(), locate.pop())
    Image_update = True


def update_screen(frame):  # 更新屏幕截图
    global Image_update
    if Image_update:
        time.sleep(1)
        draw_image.set_array(get_screen_picture())
        Image_update = False
    return draw_image,


figure = pyplot.figure()  # 创建空白的图片对象
# 将获取的图片画到坐标轴上
draw_image = pyplot.imshow(get_screen_picture(), animated=True)
figure.canvas.mpl_connect('button_press_event', on_click)  # 绑定鼠标单击事件
new_screen = FuncAnimation(figure, update_screen, interval=50, blit=True)
pyplot.show()
