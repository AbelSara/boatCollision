#!/usr/bin/env python
# -*- coding:utf-/ -*-
__author__ = '&USER'

import os
import pygame
import math
import numpy as np
from dataDeal import DataDeal
from boat import Boat
from boatMathModel import Boat_Math_Model
from model import Model

# 背景
background = pygame.image.load('./pictures/sea.jpg')

# 有避碰危险时的方向处理
speed_up = 1
turn_right = 2
turn_left = 3
speed_down = 4
select_option = 0

# 四种会遇态势
overtaking = 1
right_cross = 2
left_cross = 3
opposite_direction = 4

# 是否复航
resume = 0

# 数据处理
dataDeal_model = DataDeal()

# 避碰危险度模型
collision_model = Model()

# 画布居中
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# 画布尺寸
screen = pygame.display.set_mode([1500, 973])
screen.fill([255, 255, 255])

# 时钟
clock = pygame.time.Clock()

# 己方船舶模型
boat_self_model = Boat('./pictures/boat.jpg', 0, 800, 750, 4)
boat_self_instance = boat_self_model.get_boat_instance()

# 目标船舶模型
boat_target_model = Boat('./pictures/boat.jpg', 180, 750, 150, 4)
boat_target_instance = boat_target_model.get_boat_instance()

# 两船相对运动模型
boat_math_model = Boat_Math_Model(self_boat=boat_self_model, target_boat=boat_target_model)

# 躲避状态
safe_condition = 0
danger_condition = 1
now_condition = safe_condition

# 安全会遇距离
safe_distance = math.sqrt(math.pow(25, 2) + math.pow(60, 2)) * 2

# 神经网络传入参数
original_data = [[0.0 for i in range(5)] for i in range(1)]
original_data = np.array(original_data)
original_data[0][4] = safe_distance / 200
finish = 0

# 己方船舶与对遇船舶运动轨迹
self_list = []
target_list = []

# 船舶开始航行
running = True
while running:
    # 用时钟对每秒迭代次数进行控制
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 重绘己方船舶与目标船舶
    screen.fill([255, 255, 255])
    # screen.blit(background, (0, 0))
    screen.blit(boat_self_instance, (boat_self_model.boat_x_location, boat_self_model.boat_y_location))
    screen.blit(boat_target_instance, (boat_target_model.boat_x_location, boat_target_model.boat_y_location))
    for i in range(len(self_list)):
        pygame.draw.circle(screen, [255, 0, 0], self_list[i], 2, 1)
    for i in range(len(target_list)):
        pygame.draw.circle(screen, [0, 0, 255], target_list[i], 2, 1)
    self_list.append((int(boat_self_model.boat_head_x), int(boat_self_model.boat_head_y)))
    target_list.append((int(boat_target_model.boat_head_x), int(boat_target_model.boat_head_y)))
    # 当前会遇态势 DCPA TCPA
    encounter_situation = boat_math_model.encounter_situation()
    boat_math_model.danger_calculate(encounter_situation)

    original_data[0][0] = boat_target_model.boat_angle
    original_data[0][1] = boat_target_model.speed * 10
    original_data[0][2] = boat_math_model.get_relative_distance() / 150
    original_data[0][3] = math.fabs(boat_target_model.boat_angle - boat_self_model.boat_angle)

    # 危险度计算，仅在安全情况下计算危险度
    if now_condition == safe_condition and finish == 0 and resume == 0:
        available_data = dataDeal_model.get_instance_data(original_data)
        risk = collision_model.collision_prediction(available_data)

    # 危险度大于0时判断有避碰危险
    if risk > 0 and finish == 0 and resume == 0:
        now_condition = danger_condition
        resume = 1

    # 对遇情况的方向选择
    if now_condition == danger_condition and encounter_situation == opposite_direction:
        if boat_self_model.boat_head_x > boat_target_model.boat_head_x:
            select_option = right_cross
        else:
            select_option = left_cross
        if math.fabs(boat_self_model.boat_x_location - boat_target_model.boat_x_location) > 150:
            resume = 0

    # 己方船舶与目标船舶移动
    boat_self_model.move()
    boat_target_model.move()
    if resume == 1 and now_condition == danger_condition:
        boat_self_model.angle_move(select_option)
        now_condition = boat_math_model.get_risk_index(safe_distance)
        if now_condition == 0 and select_option == turn_left:
            select_option = turn_right
        elif now_condition == 0 and select_option == turn_right:
            select_option = turn_left
    elif resume == 1 and now_condition == safe_condition:
        boat_self_model.angle_move(select_option)
        print(boat_self_model.boat_angle)
        if boat_self_model.boat_angle == 0 or boat_self_model.boat_angle == 360:
            finish = 1
            resume = 0
            select_option = 0

    boat_self_instance = boat_self_model.get_boat_instance()
    boat_target_instance = boat_target_model.get_boat_instance()

    pygame.display.update()
pygame.quit()
