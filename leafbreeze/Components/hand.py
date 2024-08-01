from leafbreeze.Components.BetterClasses.booleanEx import *
from leafbreeze.Components.Constants.constants import *
from leafbreeze.Components.leaf import *

import pygame

lower_margin = 20
higher_margin = 700
limit = 150

class Hand():
    def __init__(self, constants: Constants):
        self.constants = constants

        self.rectangles = None
        self.pose_font = None
        self.images = None
        self.mask = None

        self.pose = None
        self.show_index = 0
        self.position_multiplier = 0

        self.images = [img_hand_zero_fingers, 
                       img_hand_one_finger,
                       img_hand_two_fingers,
                       img_hand_three_fingers,
                       img_hand_four_fingers,
                       img_hand_five_fingers
        ]

        self.rectangles = [img.get_rect() for img in self.images]
        self.masks = [pygame.mask.from_surface(img) for img in self.images]

        self.recalculate()

        self.pose = self.original_pose.copy()
        self.can_hit = True  # Flag to control hitting

    def recalculate(self):
        # Initial position slightly above the middle of the screen
        self.original_pose = Pose(self.constants.screen_size.half_w,
                                  self.constants.screen_size.height * 0.9)
        self.position_multiplier = self.constants.screen_size.width / (higher_margin - lower_margin)

    def setHandInfo(self, x: int, fingers: int):
        if abs(self.pose.x - (self.constants.screen_size.width - x * self.position_multiplier)) > 15:
            self.pose.x = self.constants.screen_size.width - x * self.position_multiplier

        if self.pose.x < limit:
            self.pose.x = limit
        if self.pose.x > self.constants.screen_size.width - limit:
            self.pose.x = self.constants.screen_size.width - limit
        
        self.show_index = fingers

    def check_target_area(self, target_x: int):
        """Check if the leaf is over a target area and handle lives."""
        target_area_width = 100  # Width of the target area
        if abs(self.pose.x - target_x) < target_area_width / 2:
            return True
        return False

    def reset_hit(self):
        """Reset the hit flag to allow hitting again."""
        self.can_hit = True

    def onScreen(self, screen: pygame.Surface):
        for each in self.rectangles:
            each.center = self.pose.tuple()

        screen.blit(self.images[self.show_index], self.rectangles[self.show_index])



class AuxiliaryHand():
    def __init__(self, constants: Constants):
        self.constants = constants
        self.original_images = [img_hand_zero_fingers,
                                img_hand_one_finger,
                                img_hand_two_fingers,
                                img_hand_three_fingers,
                                img_hand_four_fingers,
                                img_hand_five_fingers]

        # Rotate all images upside down (180 degrees)
        self.images = [pygame.transform.rotate(img, 180) for img in self.original_images]
        

        self.rectangles = [img.get_rect() for img in self.images]
        self.masks = [pygame.mask.from_surface(img) for img in self.images]

        self.show_index = 0  # Index of the number of fingers to display
        self.pose = Pose(self.constants.screen_size.width * 0.9, 0)  # Start position (e.g., bottom-left corner)
        self.target_pose = Pose(self.constants.screen_size.width * 0.9, self.constants.screen_size.width * 0.06)  # Target position to move towards

        self.speed = 5  # Speed at which the hand moves to the target position
        self.is_visible = False  # Initially hidden

    def set_fingers(self, fingers: int):
        """Set the number of fingers to display and make the hand visible."""
        self.show_index = fingers
        self.is_visible = True

    def update_position(self):
        """Move the hand towards its target position."""
        if not self.is_visible:
            return
        
        dx = self.target_pose.x - self.pose.x
        dy = self.target_pose.y - self.pose.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > self.speed:
            # Normalize direction and move towards target
            self.pose.x += (dx / distance) * self.speed
            self.pose.y += (dy / distance) * self.speed
        else:
            # If close enough, snap to target position
            self.pose.x = self.target_pose.x
            self.pose.y = self.target_pose.y

    def hide(self):
        """Hide the auxiliary hand by moving it off-screen."""
        self.is_visible = False
        self.pose = Pose(self.constants.screen_size.width * 0.9, 0)  # Move back to starting position

    def onScreen(self, screen: pygame.Surface):
        """Render the auxiliary hand on the screen."""
        if not self.is_visible:
            return

        self.update_position()

        for each in self.rectangles:
            each.center = self.pose.tuple()

        screen.blit(self.images[self.show_index], self.rectangles[self.show_index])
