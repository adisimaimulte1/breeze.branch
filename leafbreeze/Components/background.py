from leafbreeze.Components.Constants.constants import *

class Background():
    def __init__(self, constants: Constants):
        self.constants = constants

        self.tree_image = img_tree_with_leaves
        self.tree_rectangle = self.tree_image.get_rect()
        self.tree_mask = pygame.mask.from_surface(self.tree_image)

        self.background_image = img_background
        self.background_rectangle = self.background_image.get_rect()
        self.background_mask = pygame.mask.from_surface(self.background_image)

        self.recalculate()

    
    def recalculate(self):
        self.tree_rectangle.center = (400, 400)
        self.background_rectangle.center = self.constants.screen_size.getHalf()
    
    def onScreen(self, screen: pygame.Surface):
        screen.blit(self.background_image, self.background_rectangle)
        screen.blit(self.tree_image, self.tree_rectangle)