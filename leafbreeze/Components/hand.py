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

    def hit(self, leaf: Leaf) -> bool:
        """Perform a hit if the hand is under the leaf and can hit."""
        if self.can_hit and self.is_under_leaf(leaf):
            self.can_hit = False  # Disable further hits until reset
            return True
        return False

    def is_under_leaf(self, leaf: Leaf) -> bool:
        """Check if the hand is positioned under the leaf."""
        leaf_x, leaf_y = leaf.pose.tuple()
        hand_x, hand_y = self.pose.tuple()
        
        # Define the hit region: hand is considered under the leaf if its y is close to the leaf's y
        return (abs(hand_x - leaf_x) < 50) and (hand_y > leaf_y and hand_y < leaf_y + 50)
    
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
