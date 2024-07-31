from leafbreeze.Components.Constants.constants import *

class Background():
    def __init__(self, constants: Constants):
        self.constants = constants

        self.rectangle = None
        self.pose_font = None
        self.image = None
        self.mask = None

        self.image = img_tree_with_leaves
        self.rectangle = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.recalculate()

    
    def recalculate(self):
        self.rectangle.center = (400, 400)
    
    def onScreen(self, screen: pygame.Surface):
        screen.blit(self.image, self.rectangle)