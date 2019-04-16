#!/usr/bin/env python
# -*- coding:utf-/ -*-
__author__ = '&USER'
import pygame
import math

# 避碰方向
turn_right = 2
turn_left = 3

# 角度偏转大小
turn_angle = 1.5


class Boat:
    def __init__(self, image, angle, x_location, y_location, speed):
        # 加载小船图像
        self.boat_image = image

        # 图像位置，移动图像的基础
        self.boat_x_location = x_location
        self.boat_y_location = y_location

        # 小船移动速度
        self.speed = speed

        # 移动时的角度
        self.boat_angle = angle
        self.boat_angle_radians = math.radians(self.boat_angle)

        # 小船船头位置，计算dcpa和tcpa
        self.boat_original_instance = pygame.image.load(self.boat_image).convert()
        self.boat_instance = pygame.transform.rotate(self.boat_original_instance, self.boat_angle)
        self.boat_head_x, self.boat_head_y = self.get_boat_head()

    def get_boat_head(self):
        rect = self.boat_instance.get_rect()
        binary_width = rect.width / 2
        binary_height = rect.height / 2
        mid_x = self.boat_x_location + binary_width
        mid_y = self.boat_y_location + binary_height
        if 0 <= self.boat_angle < 90:
            x = mid_x - binary_width * math.fabs(math.sin(self.boat_angle_radians))
            y = mid_y - binary_height * math.fabs(math.cos(self.boat_angle_radians))
        elif 90 <= self.boat_angle < 180:
            x = mid_x - binary_width * math.fabs(math.sin(self.boat_angle_radians))
            y = mid_y + binary_height * math.fabs(math.cos(self.boat_angle_radians))
        elif 180 <= self.boat_angle < 270:
            x = mid_x + binary_width * math.fabs(math.sin(self.boat_angle_radians))
            y = mid_y + binary_height * math.fabs(math.cos(self.boat_angle_radians))
        else:
            x = mid_x + binary_width * math.fabs(math.sin(self.boat_angle_radians))
            y = mid_y - binary_height * math.fabs(math.cos(self.boat_angle_radians))
        return x, y

    def get_boat_instance(self):
        return self.boat_instance

    def move(self):
        self.boat_angle_radians = math.radians(self.boat_angle)
        if 0 <= self.boat_angle < 90:
            self.boat_x_location -= self.speed * math.fabs(math.sin(self.boat_angle_radians))
            self.boat_y_location -= self.speed * math.fabs(math.cos(self.boat_angle_radians))
        elif 90 <= self.boat_angle < 180:
            self.boat_x_location -= self.speed * math.fabs(math.sin(self.boat_angle_radians))
            self.boat_y_location += self.speed * math.fabs(math.cos(self.boat_angle_radians))
        elif 180 <= self.boat_angle < 270:
            self.boat_x_location += self.speed * math.fabs(math.sin(self.boat_angle_radians))
            self.boat_y_location += self.speed * math.fabs(math.cos(self.boat_angle_radians))
        elif 270 <= self.boat_angle <= 360:
            self.boat_x_location += self.speed * math.fabs(math.sin(self.boat_angle_radians))
            self.boat_y_location -= self.speed * math.fabs(math.cos(self.boat_angle_radians))
        # 每次移动之后计算新的头部位置
        self.boat_head_x, self.boat_head_y = self.get_boat_head()

    def angle_move(self, direction):
        flag = 1
        if self.boat_angle == 60 and direction == turn_left or 300 == self.boat_angle and direction == turn_right:
            flag = 0
        if 1 == flag and turn_right == direction:
            if self.boat_angle == 0:
                self.boat_angle = 360
            self.boat_angle = self.boat_angle - turn_angle
        elif 1 == flag and turn_left == direction:
            if self.boat_angle == 360:
                self.boat_angle = 0
            self.boat_angle = self.boat_angle + turn_angle
        self.boat_instance = pygame.transform.rotate(self.boat_original_instance, self.boat_angle)
