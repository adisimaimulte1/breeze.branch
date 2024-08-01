from leafbreeze.Components.BetterClasses.booleanEx import *
from leafbreeze.Components.Constants.constants import *

import math

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

    def recalculate(self):
        # Initial position slightly above the middle of the screen
        self.original_pose = Pose(self.constants.screen_size.half_w,
                                  self.constants.screen_size.height * 0.9)
        self.position_multiplier = self.constants.screen_size.width / (higher_margin - lower_margin)

    def setHandInfo(self, x: int, fingers: int):
        self.pose.x = self.constants.screen_size.width - x * self.position_multiplier

        if self.pose.x < limit:
            self.pose.x = limit
        if self.pose.x > self.constants.screen_size.width - limit:
            self.pose.x = self.constants.screen_size.width - limit
        
        self.show_index = fingers
    
    def onScreen(self, screen: pygame.Surface):
        for each in self.rectangles:
            each.center = self.pose.tuple()

        screen.blit(self.images[self.show_index], self.rectangles[self.show_index])