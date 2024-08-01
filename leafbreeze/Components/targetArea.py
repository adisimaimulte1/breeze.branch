from leafbreeze.Components.Constants.constants import *

class TargetArea():
    def __init__(self, constants: Constants):
        self.constants = constants

        self.REACHED = BooleanEx(True)
        self.rectangle_size = (300, 300)
        self.rectangle_center = (0, 0)
    
    def reset(self):
        self.REACHED = BooleanEx(True)
        self.rectangle_size = (300, 300)
        self.rectangle_center = (0, 0)
        
    def __drawBorder(self, screen: pygame.Surface):
        pygame.draw.lines(screen, "white", True, self.__findBorder(), 30)
    
    def __findBorder(self):
        left = self.rectangle_center[0] - self.rectangle_size[0] / 2
        top = self.rectangle_center[1] - self.rectangle_size[1] / 2

        border = pygame.Rect(left, top, self.rectangle_size[0], self.rectangle_size[1])

        topLeft = pygame.math.Vector2(border.topleft) 
        topRight = pygame.math.Vector2(border.topright)
        bottomRight = pygame.math.Vector2(border.bottomright)
        bottonLeft = pygame.math.Vector2(border.bottomleft)

        return [topLeft, topRight, bottomRight, bottonLeft]

    def addZone(self, x: int):
        self.REACHED.set(False)
        self.rectangle_center = (x, 0.85 * self.constants.screen_size.height)
    
    def onScreen(self, screen: pygame.Surface):
        if self.REACHED.compare(False):
            self.__drawBorder(screen)