import cv2
import numpy as np


def judge_light_color(obj_bgr):
    #  将图片转成HSV的
    obj_hsv = cv2.cvtColor(obj_bgr, cv2.COLOR_BGR2HSV)
    #  从H通道中提取出颜色的平均值
    H = obj_hsv[:, :, 0]
    H = np.squeeze(np.reshape(H, (1, -1)))

    H_value = np.array([])
    for i in H:
        if i > 0 and i < 124:
            H_value = np.append(H_value, i)
    H_avg = np.average(H_value)
    print(H_avg)
    #  根据这个值来判断是什么颜色， RYG
    if H_avg <= 18 or H_avg >= 100:
        color = "Red"
    elif H_avg >= 18 and H_avg <= 34:
        color = "Yellow"
    elif H_avg >= 35 and H_avg <= 100:
        color = "Green"
    else:
        color = "Unkonwn"

    return color

if __name__ == '__main__':
    trafficLight = cv2.imread('./Image&Video/4.png', cv2.IMREAD_COLOR)
    print(judge_light_color(trafficLight))