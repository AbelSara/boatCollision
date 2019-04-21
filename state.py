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

# 有避碰危险时的方向处理
speed_up = 1
turn_right = 2
turn_left = 3
speed_down = 4

# 四种会遇态势
overtaking = 1
right_cross = 2
left_cross = 3
opposite_direction = 4


class State:
    def boat_state(self, boat_main_model, boat_target_model, screen):
        # 船舶图形
        boat_self_instance = boat_main_model.get_boat_instance()
        boat_target_instance = boat_target_model.get_boat_instance()

        # 是否复航
        resume = 0

        # 选择态势
        select_option = 0

        # 数据处理
        dataDeal_model = DataDeal()

        # 避碰危险度模型
        collision_model = Model()

        # pygame时钟
        clock = pygame.time.Clock()

        # 两船相对运动模型
        boat_math_model = Boat_Math_Model(self_boat=boat_main_model, target_boat=boat_target_model)
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

        # 会遇态势
        encounter_situation = 0

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
            screen.blit(boat_self_instance, (boat_main_model.boat_x_location, boat_main_model.boat_y_location))
            screen.blit(boat_target_instance, (boat_target_model.boat_x_location, boat_target_model.boat_y_location))
            for i in range(len(self_list)):
                pygame.draw.circle(screen, [255, 0, 0], self_list[i], 2, 1)
            for i in range(len(target_list)):
                pygame.draw.circle(screen, [0, 0, 255], target_list[i], 2, 1)
            self_list.append((int(boat_main_model.boat_head_x), int(boat_main_model.boat_head_y)))
            target_list.append((int(boat_target_model.boat_head_x), int(boat_target_model.boat_head_y)))
            # 当前会遇态势 DCPA TCPA
            if 0 == encounter_situation:
                encounter_situation = boat_math_model.encounter_situation()
            boat_math_model.danger_calculate(encounter_situation)

            original_data[0][0] = boat_target_model.boat_angle
            original_data[0][1] = boat_target_model.speed * 10
            original_data[0][2] = boat_math_model.get_relative_distance() / 150
            original_data[0][3] = math.fabs(boat_target_model.boat_angle - boat_main_model.boat_angle)

            # 危险度计算，仅在安全情况下计算危险度
            if now_condition == safe_condition and finish == 0 and resume == 0:
                available_data = dataDeal_model.get_instance_data(original_data)
                risk = collision_model.collision_prediction(available_data)

            # 危险度大于0时判断有避碰危险
            if risk > 0 and finish == 0 and resume == 0:
                now_condition = danger_condition
                resume = 1

            # 对遇情况的方向选择
            # 对遇
            if now_condition == danger_condition and encounter_situation == opposite_direction:
                if boat_main_model.boat_head_x > boat_target_model.boat_head_x:
                    select_option = right_cross
                else:
                    select_option = left_cross
                if math.fabs(
                        boat_main_model.boat_x_location - boat_target_model.boat_x_location) > 150 and boat_main_model.boat_angle == boat_main_model.boat_original_angle:
                    resume = 0
            # 右弦交叉
            elif now_condition == danger_condition and encounter_situation == right_cross:
                select_option = right_cross
                # if 可以安全通过
                if math.fabs(boat_main_model.boat_x_location - boat_target_model.boat_x_location) > 150 and math.fabs(
                        boat_main_model.boat_y_location - boat_target_model.boat_y_location) > 50 and boat_main_model.boat_angle == boat_main_model.boat_original_angle:
                    resume = 0
            # 左弦
            elif now_condition == danger_condition and encounter_situation == left_cross:
                select_option = right_cross
                # if 可以安全通过
                if math.fabs(boat_main_model.boat_x_location - boat_target_model.boat_x_location) > 150 and math.fabs(
                        boat_main_model.boat_y_location - boat_target_model.boat_y_location) > 50 and boat_main_model.boat_angle == boat_main_model.boat_original_angle:
                    resume = 0
            # 追越
            elif now_condition == danger_condition and encounter_situation == overtaking:
                select_option = right_cross
                if math.fabs(
                        boat_main_model.boat_x_location - boat_target_model.boat_x_location) > 150 and boat_main_model.boat_angle == boat_main_model.boat_original_angle:
                    resume = 0

            # 己方船舶与目标船舶移动
            boat_main_model.move()
            boat_target_model.move()
            print(str(resume) + ' ' + str(now_condition))
            if encounter_situation == left_cross:
                if resume == 1 and now_condition == danger_condition:
                    boat_target_model.angle_move(select_option)
                    now_condition = boat_math_model.get_risk_index(safe_distance, encounter_situation)
                    if now_condition == 0:
                        select_option = turn_left
                elif resume == 1 and now_condition == safe_condition:
                    # select_option = turn_right
                    print(select_option)
                    boat_target_model.angle_move(select_option)
                    if boat_target_model.boat_angle == boat_target_model.boat_original_angle or boat_target_model.boat_angle == 360 + boat_target_model.boat_original_angle:
                        finish = 1
                        resume = 0
                        select_option = 0
                        encounter_situation = 0
            else:
                if resume == 1 and now_condition == danger_condition:
                    boat_main_model.angle_move(select_option)
                    now_condition = boat_math_model.get_risk_index(safe_distance, encounter_situation)
                    if now_condition == 0 and select_option == turn_left:
                        select_option = turn_right
                    elif now_condition == 0 and select_option == turn_right:
                        select_option = turn_left
                elif resume == 1 and now_condition == safe_condition:
                    boat_main_model.angle_move(select_option)
                    if boat_main_model.boat_angle == boat_main_model.boat_original_angle or boat_main_model.boat_angle == 360 + boat_main_model.boat_original_angle:
                        finish = 1
                        resume = 0
                        select_option = 0
                        encounter_situation = 0

            boat_self_instance = boat_main_model.get_boat_instance()
            boat_target_instance = boat_target_model.get_boat_instance()

            pygame.display.update()

            if boat_main_model.state_finish() == 1:
                break
