#!/usr/bin/env python
# -*- coding:utf-/ -*-
__author__ = '&USER'

import os
import pygame
from boat import Boat
from boatMathModel import Boat_Math_Model

# 画布居中
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# 画布尺寸
screen = pygame.display.set_mode([1500, 973])
screen.fill([255, 255, 255])

# 时钟
clock = pygame.time.Clock()

# 己方船舶模型
boat_self_model = Boat('./pictures/boat.jpg', 0, 750, 750, 4)
boat_self_instance = boat_self_model.get_boat_instance()

# 目标船舶模型
boat_target_model = Boat('./pictures/boat.jpg', 180, 750, 150, 4)
boat_target_instance = boat_target_model.get_boat_instance()

# 两船相对运动模型
boat_math_model = Boat_Math_Model(self_boat=boat_self_model, target_boat=boat_target_model)

running = True
while running:
    # 用时钟对每秒迭代次数进行控制
    clock.tick(6)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 重绘己方船舶与目标船舶
    screen.fill([255, 255, 255])
    screen.blit(boat_self_instance, (boat_self_model.boat_x_location, boat_self_model.boat_y_location))
    screen.blit(boat_target_instance, (boat_target_model.boat_x_location, boat_target_model.boat_y_location))

    # 当前会遇态势
    encounter_situation = boat_math_model.encounter_situation()
    boat_math_model.danger_calculate(encounter_situation)

    # 己方船舶与目标船舶移动
    boat_self_model.move()
    boat_target_model.move()
    boat_self_model.angle_move()
    boat_target_model.angle_move()
    boat_self_instance = boat_self_model.get_boat_instance()
    boat_target_instance = boat_target_model.get_boat_instance()

    pygame.display.update()
pygame.quit()
