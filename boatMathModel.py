#!/usr/bin/env python
# -*- coding:utf-/ -*-
__author__ = '&USER'
import math

# 四种会遇态势
overtaking = 1
right_cross = 2
left_cross = 3
opposite_direction = 4


class Boat_Math_Model:
    def __init__(self, self_boat, target_boat):
        self.main_boat = self_boat
        self.target_boat = target_boat

    # 计算会遇态势
    def encounter_situation(self):
        encounter = 0
        if self.main_boat.boat_angle == self.target_boat.boat_angle:
            encounter = overtaking
        elif math.fabs(self.main_boat.boat_angle - self.target_boat.boat_angle) == 180:
            encounter = opposite_direction
        elif -180 < self.main_boat.boat_angle - self.target_boat.boat_angle < 0:
            encounter = right_cross
        elif -360 < self.main_boat.boat_angle - self.target_boat.boat_angle < -180:
            encounter = left_cross
        elif 0 < self.main_boat.boat_angle - self.target_boat.boat_angle < 180:
            encounter = left_cross
        elif 180 < self.main_boat.boat_angle - self.target_boat.boat_angle < 360:
            encounter = right_cross
        return encounter

    def danger_calculate(self, encounter):
        main_boat_v_x = math.fabs(math.sin(self.main_boat.boat_angle_radians))
        main_boat_v_y = math.fabs(math.cos(self.main_boat.boat_angle_radians))
        target_boat_v_x = math.fabs(math.sin(self.target_boat.boat_angle_radians))
        target_boat_v_y = math.fabs(math.cos(self.target_boat.boat_angle_radians))

        # 两船距离
        delta_x = self.target_boat.boat_head_x - self.main_boat.boat_head_x
        delta_y = self.target_boat.boat_head_y - self.main_boat.boat_head_y
        distance = math.sqrt(pow(delta_y, 2) + pow(delta_x, 2))

        # 交叉时
        if encounter == left_cross or encounter == right_cross:
            print("会遇态势为交叉")
            # 相对速度
            relative_v_x = math.fabs(main_boat_v_x - target_boat_v_x)
            relative_v_y = math.fabs(main_boat_v_y - target_boat_v_y)
            relative_v = math.sqrt(pow(relative_v_x, 2) + pow(relative_v_y, 2))
            # 相对航向
            alpha = 360 - self.target_boat.boat_angle
            if relative_v_y == 0:
                relative_angle = math.radians(180)
            else:
                relative_angle = math.atan(relative_v_x / relative_v_y) + alpha
            # 目标船方位
            target_boat_situation = math.atan(delta_x / delta_y) + alpha
            # DCTA && TCPA
            dcpa = math.fabs(distance * math.sin(relative_angle - target_boat_situation - math.pi))
            tcpa = math.fabs(distance * math.cos(relative_angle - target_boat_situation - math.pi) / relative_v)
            print(str(dcpa) + " " + str(tcpa))
        # 对遇时
         elif encounter==opposite_direction:
