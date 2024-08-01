from leafbreeze.Components.BetterClasses.booleanEx import *
from leafbreeze.Components.Constants.constants import *

import math

class Leaf():
    def __init__(self, constants: Constants):
        self.constants = constants
        self.leaf_fps = 3
        self.time = 0

        self.SHOULD_APPLY_GRAVITY = BooleanEx(False)
        self.rectangles = None
        self.pose_font = None
        self.images = None
        self.mask = None

        self.pose = None
        self.show_index = 0

        self.images = [img_leaf1, img_leaf2, img_leaf3]
        self.rectangles = [img.get_rect() for img in self.images]
        self.masks = [pygame.mask.from_surface(img) for img in self.images]

        self.gravity = 0.5  # Acceleration due to gravity
        self.velocity_y = 0  # Initial vertical velocity

        self.amplitude = 4  # Amplitude of the wave (distance from the center)
        self.frequency = 0.08  # Frequency of the wave (speed of oscillation)
        self.wave_time = 0  # Time variable for the sine wave

        self.recalculate()

        self.pose = self.original_pose.copy()
        self.time_4_one_frame = int(1000 / self.leaf_fps)

    def recalculate(self):
        # Initial position slightly above the middle of the screen
        self.original_pose = Pose(self.constants.screen_size.width * 0.5,
                                  self.constants.screen_size.height * 0.25)

    def reset(self):
        self.pose = self.original_pose
        self.SHOULD_APPLY_GRAVITY = BooleanEx(False)
    
    def animate(self, clock):
        self.time += clock.get_time()
        self.time = self.time % 1000

        if self.time > 1000:
            return None

        self.show_index = int(self.time / self.time_4_one_frame)
        if self.show_index >= len(self.images):
            self.show_index = len(self.images) - 1
    
    def apply_gravity(self):
        # Update vertical velocity based on gravity
        self.velocity_y += self.gravity

        # Update the leaf's vertical position based on velocity (falling down)
        self.pose.y += self.velocity_y

        # Stop the leaf at the middle of the screen height
        if self.pose.y >= self.constants.screen_size.height * 0.5:
            self.pose.y = self.constants.screen_size.height * 0.5
            self.velocity_y = 0  # Stop vertical movement

        # Update the leaf's position to create a wavy movement
        self.wave_time += self.frequency
        self.pose.x = self.original_pose.x + self.amplitude * math.sin(self.wave_time)
        self.pose.y = self.original_pose.y + self.amplitude * math.sin(self.wave_time)  # Add to the existing y-position for subtle up-down motion

        # Ensure the leaf doesn't go outside the screen horizontally
        if self.pose.x < 0:
            self.pose.x = 0
        elif self.pose.x > self.constants.screen_size.width:
            self.pose.x = self.constants.screen_size.width


    
    def onScreen(self, screen: pygame.Surface, clock):
        self.animate(clock)

        if self.SHOULD_APPLY_GRAVITY.compare():
            self.apply_gravity()

        for each in self.rectangles:
            each.center = self.pose.tuple()

        screen.blit(self.images[self.show_index], self.rectangles[self.show_index])
