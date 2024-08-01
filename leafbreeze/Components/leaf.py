from leafbreeze.Components.BetterClasses.booleanEx import *
from leafbreeze.Components.Constants.constants import *

import math
import pygame

class Leaf:
    def __init__(self, constants: Constants):
        self.constants = constants
        self.leaf_fps = 3
        self.time = 0

        self.SHOULD_APPLY_GRAVITY = BooleanEx(False)
        self.ON_TARGET = BooleanEx(False)

        self.start_time = 0
        self.total_time = 1500

        self.images = [img_leaf1, 
                       img_leaf2, 
                       img_leaf3]
        
        self.rectangles = [img.get_rect() for img in self.images]
        self.masks = [pygame.mask.from_surface(img) for img in self.images]
        self.DISABLE = BooleanEx(False)

        self.gravity = 0.5
        self.velocity_y = 0
        self.amplitude = 4
        self.frequency = 0.08
        self.wave_time = 0

        screen_height = self.constants.screen_size.height
        self.levels = [screen_height * 0.3, screen_height * 0.5, screen_height * 0.7, screen_height * 0.8]
        self.current_level = 0

        self.max_lives = 10
        self.total_lives = 9
        self.lives_per_level = self.total_lives // 3
        self.lives = self.total_lives

        self.target_x = None
        self.target_speeds = [10, 12, 14, 16]

        self.float_range = 10
        self.start_pose = Pose(self.constants.screen_size.width * 0.5, screen_height * 0.25)
        self.pose = self.start_pose
        self.time_4_one_frame = int(1000 / self.leaf_fps)

    def reset(self):
        self.pose = self.start_pose
        self.SHOULD_APPLY_GRAVITY = BooleanEx(False)
        self.ON_TARGET = BooleanEx(False)
        self.DISABLE = BooleanEx(False)
        self.lives = self.total_lives


    def animate(self, clock):
        self.time = (self.time + clock.get_time()) % 1000
        self.show_index = min(int(self.time / self.time_4_one_frame), len(self.images) - 1)

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.pose.y += self.velocity_y

        self.wave_time += self.frequency
        float_y = self.float_range * math.sin(self.wave_time)

        if self.pose.y >= self.levels[self.current_level]:
            self.pose.y = self.levels[self.current_level] + float_y
            self.velocity_y = 0
        else:
            self.pose.y = self.pose.y + float_y

        if self.target_x is not None:
            if abs(self.pose.x - self.target_x) > self.target_speeds[self.current_level]:
                direction = 1 if self.pose.x < self.target_x else -1
                self.pose.x += direction * self.target_speeds[self.current_level]

        self.pose.x = max(0, min(self.pose.x, self.constants.screen_size.width))

    def adjust_lives(self, delta_lives: int):
        self.lives = max(0, min(self.lives + delta_lives, self.max_lives))

        if self.total_lives < self.lives:
            self.current_level = 0
        else: self.current_level = (self.total_lives - self.lives) // self.lives_per_level

        if self.total_lives == self.max_lives:
            self.reset()

    def check_target_area(self, target_x: int):
        if abs(self.pose.x - target_x) < 50:
            return True
        return False

    def move_to_target_area(self, target_x: int):
        self.target_x = target_x

    def onScreen(self, screen: pygame.Surface, clock):
        if self.DISABLE.compare():
            return None

        self.animate(clock)

        if self.SHOULD_APPLY_GRAVITY.compare():
            self.apply_gravity()

        for rect in self.rectangles:
            rect.center = self.pose.tuple()

        screen.blit(self.images[self.show_index], self.rectangles[self.show_index])
