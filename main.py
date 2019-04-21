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
from state import State

# 画布居中
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# 画布尺寸
screen = pygame.display.set_mode([1500, 973])
screen.fill([255, 255, 255])

# 船舶对于态势演示模型
state_model = State()

# 双方船舶追越模型
boat_self_model = Boat('./pictures/boat.jpg', 0, 600, 900, 9)
boat_target_model = Boat('./pictures/boat.jpg', 0, 600, 350, 2)

# 追越
state_model.boat_state(boat_self_model, boat_target_model, screen)

# 双方船舶对遇模型
boat_self_model = Boat('./pictures/boat.jpg', 0, 600, 750, 5)
boat_target_model = Boat('./pictures/boat.jpg', 180, 600, 150, 5)

# 对遇
state_model.boat_state(boat_self_model, boat_target_model, screen)

# 双方船舶左弦交叉模型
boat_self_model = Boat('./pictures/boat.jpg', 0, 900, 650, 5)
boat_target_model = Boat('./pictures/boat.jpg', 225, 700, 150, 5)

# 右弦交叉
state_model.boat_state(boat_self_model, boat_target_model, screen)

# 双方船舶左弦交叉模型
boat_self_model = Boat('./pictures/boat.jpg', 0, 600, 750, 5)
boat_target_model = Boat('./pictures/boat.jpg', 135, 800, 150, 5)

# 左弦交叉
state_model.boat_state(boat_self_model, boat_target_model, screen)

pygame.quit()
