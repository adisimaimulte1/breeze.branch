from leafbreeze.Components.BetterClasses.booleanEx import *
from leafbreeze.Components.Constants.screenSize import *
from leafbreeze.Components.BetterClasses.mathEx import *

import pygame 
import os

device_relative_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Images')

screenshot_path = os.path.join(device_relative_path, 'Screenshots\\')

default_fps = 150

#KEY BINDS
left_wheel_forward_key = pygame.K_q
right_wheel_forward_key = pygame.K_w

left_wheel_backward_key = pygame.K_a
right_wheel_backward_key = pygame.K_s

turn_0_key = pygame.K_1
turn_45_key = pygame.K_2
turn_90_key = pygame.K_3
turn_135_key = pygame.K_4
turn_180_key = pygame.K_5
turn_225_key = pygame.K_6
turn_270_key = pygame.K_7
turn_315_key = pygame.K_8




#XBOX
xbox_threshold = 0.0001
xbox_left_x = 0
xbox_left_y = 1
xbox_right_x = 2

xbox_disable_button = 2
xbox_direction_button = 3
xbox_zero_button = 1
xbox_head_selection_button = 5
xbox_trail_button = 0
xbox_erase_trail_button = 4
xbox_screenshot_button = 7

xbox_turn_0 = (0, 1)
xbox_turn_45 = (1, 1)
xbox_turn_90 = (1, 0)
xbox_turn_135 = (1, -1)
xbox_turn_180 = (0, -1)
xbox_turn_225 = (-1, -1)
xbox_turn_270 = (-1, 0)
xbox_turn_315 = (-1, 1)

#PS4
ps4_threshold = 0.06
ps4_left_x = 0
ps4_left_y = 1
ps4_right_x = 2

ps4_disable_button = 2
ps4_direction_button = 3
ps4_zero_button = 1
ps4_head_selection_button = 10
ps4_trail_button = 0
ps4_erase_trail_button = 9
ps4_screenshot_button = 5

ps4_turn_0 = 11
ps4_turn_45 = None
ps4_turn_90 = 14
ps4_turn_135 = None
ps4_turn_180 = 12
ps4_turn_225 = None
ps4_turn_270 = 13
ps4_turn_315 = None

#PS5
ps5_threshold = 0.05 #to be tuned
ps5_left_x = 0
ps5_left_y = 1
ps5_right_x = 2

ps5_disable_button = 2
ps5_direction_button = 3
ps5_zero_button = 1
ps5_head_selection_button = 10
ps5_trail_button = 0
ps5_erase_trail_button = 9
ps5_screenshot_button = 10

ps5_turn_0 = (0, 1)
ps5_turn_45 = (1, 1)
ps5_turn_90 = (1, 0)
ps5_turn_135 = (1, -1)
ps5_turn_180 = (0, -1)
ps5_turn_225 = (-1, -1)
ps5_turn_270 = (-1, 0)
ps5_turn_315 = (-1, 1)



def point2Tuple(point: Point):
    return (point.x, point.y)

def tuple2Point(tuple: tuple):
    return Point(tuple[0], tuple[1])

def percent2Alpha(value):
    return value * 2.25

def distance(p1: tuple, p2: tuple):
    return hypot(p2[0] - p1[0], p2[1] - p1[1])

def exists(value):
    return value is not None

def getRelativeFromAbsolutePath(path: str) -> str:
    return os.path.join(device_relative_path, path)


class Constants():
    def __init__(self, 
                 fps = default_fps,
                 screen_size: ScreenSize = ScreenSize()):
        
        self.recalculate = BooleanEx(False)

        self.FPS = fps
        self.screen_size = screen_size

    #resets all the values to default
    def default(self):
        self.reset_buttons_default = False

    
    def updateRobotImgSource(self, 
                             path = None, 
                             name = None, 
                             extension = None):
        
        if path is not None:
            self.ROBOT_IMG_PATH = path
        if name is not None:
            self.ROBOT_IMG_NAME = name
        if extension is not None:
            self.ROBOT_IMG_EX = extension

        self.ROBOT_IMG_SOURCE = os.path.join(device_relative_path, "{0}{1}.{2}".format(self.ROBOT_IMG_PATH, 
                                                    self.ROBOT_IMG_NAME, 
                                                    self.ROBOT_IMG_EX))
          
    def copy(self):
        new = Constants(
            self.FPS,
            self.screen_size,
        )
        return new
    
    def check(self, other):
        if isinstance(other, Constants):
            dif = 0
            
            if not self.FPS == other.FPS:
                self.FPS = other.FPS
                dif += 1
            if not self.screen_size.isLike(other.screen_size):
                self.screen_size = other.screen_size.copy()
                dif += 1

            if not dif == 0:
                self.reset_buttons_default = other.reset_buttons_default
                self.recalculate.set(True)
    
    def checkScreenSize(self, actual_screen_size: tuple):
        if not (self.screen_size.width == actual_screen_size[0] 
                                      and
                self.screen_size.height == actual_screen_size[1]):
            if self.recalculate.compare(True):
                return True

            self.recalculate.set(True)
            return False

        return True
    
    def matchScreenSize(self, image: pygame.Surface, width):
        size_multiplier = self.WIDTH_PERCENT / 100 * width / self.screen_size.MAX_WIDTH

        return pygame.transform.scale(image, 
            (size_multiplier * image.get_width(),
            size_multiplier * image.get_height()))
