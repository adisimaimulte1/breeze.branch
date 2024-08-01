import math
import pygame
from leafbreeze.Components.BetterClasses.booleanEx import *
from leafbreeze.Components.Constants.constants import *

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

        self.levels = [self.constants.screen_size.height * 0.3,
                       self.constants.screen_size.height * 0.5,
                       self.constants.screen_size.height * 0.7,
                       self.constants.screen_size.height * 0.8]  # Four height levels
        self.current_level = 0  # Start at the highest level

        self.total_lives = 15
        self.lives_per_level = self.total_lives / 3
        self.lives = self.total_lives  # Initialize lives to total lives

        self.target_x = None  # Current target X position for the leaf to move towards
        self.target_speeds = [10, 12, 14, 16]  

        self.recalculate()

        self.pose = self.original_pose.copy()
        self.time_4_one_frame = int(1000 / self.leaf_fps)

        self.float_range = 10  # Range of floating above and below the target_y

    def recalculate(self):
        # Initial position slightly above the middle of the screen
        self.original_pose = Pose(self.constants.screen_size.width * 0.5,
                                  self.constants.screen_size.height * 0.25)

    def reset(self):
        self.pose = self.original_pose
        self.SHOULD_APPLY_GRAVITY = BooleanEx(False)
        self.lives = self.total_lives  # Reset lives when resetting

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

        # Apply a floating effect within the float range
        self.wave_time += self.frequency
        float_y = self.float_range * math.sin(self.wave_time)  # Floating effect above and below target_y

        # Ensure the leaf stops at the target_y and floats above it
        if self.pose.y >= self.levels[self.current_level]:
            self.pose.y = self.levels[self.current_level] + float_y
            self.velocity_y = 0  # Stop vertical movement when at or below target_y
        else:
            self.pose.y = self.original_pose.y + float_y  # Allow falling if not yet at target_y

        # Update horizontal movement towards target area if available
        if self.target_x is not None:
            if abs(self.pose.x - self.target_x) > self.target_speeds[self.current_level]:
                if self.pose.x < self.target_x:
                    self.pose.x += self.target_speeds[self.current_level]
                else:
                    self.pose.x -= self.target_speeds[self.current_level]

        # Ensure the leaf doesn't go outside the screen horizontally
        if self.pose.x < 0:
            self.pose.x = 0
        elif self.pose.x > self.constants.screen_size.width:
            self.pose.x = self.constants.screen_size.width

    def adjust_lives(self, delta_lives: int):
        """Adjust lives by a delta amount."""
        self.lives += delta_lives

        if self.lives > self.total_lives:
            self.lives = self.total_lives
        elif self.lives <= 0:
            self.lives = 0
        
        self.current_level = 3 - int(self.lives // self.lives_per_level)

    def check_grab(self):
        """Check if the leaf should be grabbed."""
        if self.current_level == len(self.levels) - 1 and self.pose.y >= self.constants.screen_size.height * 0.7:
            return True  # Leaf is at the lowest level
        return False

    def check_target_area(self, target_x: int):
        """Check if the leaf is over a target area and handle lives."""
        target_area_width = 100  # Width of the target area
        if abs(self.pose.x - target_x) < target_area_width / 2:
            self.adjust_lives(1)  # Increase lives when the leaf reaches the target area
            self.target_x = None  # Clear target after reaching
            return True
        return False

    def move_to_target_area(self, target_x: int):
        """Move the leaf towards a target area."""
        self.target_x = target_x

    def onScreen(self, screen: pygame.Surface, clock):
        self.animate(clock)

        if self.SHOULD_APPLY_GRAVITY.compare():
            self.apply_gravity()

        for each in self.rectangles:
            each.center = self.pose.tuple()

        screen.blit(self.images[self.show_index], self.rectangles[self.show_index])
