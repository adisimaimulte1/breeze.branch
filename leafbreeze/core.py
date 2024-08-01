from leafbreeze.Components.BetterClasses.booleanEx import *
from leafbreeze.Components.Constants.constants import *

from leafbreeze.Components.handRecognition import *
from leafbreeze.Components.Menu.mainMenu import *
from leafbreeze.Components.background import *
from leafbreeze.Components.targetArea import *
from leafbreeze.Components.ControlAI import *
from leafbreeze.Components.controls import *
from leafbreeze.Components.hand import *
from leafbreeze.Components.leaf import *
from leafbreeze.Components.fade import *

from datetime import datetime
import pygame


# file connecting all features into one big ecosystem of classes
#
# from the Simulator object, all different aspects of the simulator can be accessed and be modified
#
# one big feature is the implementation of dynamic constants. Any of the lower-hierarchized objects,
#   or the user, can modify the simulator constants, and the simulator makes sure that all the objects
#   run the latest constants available with an update system based on change detection
#
# the joystick logic is also run in this class, as well as all the updates, screen drawings and simulator
#   quiting events


class LeafBreeze():
    def __init__(self):
        pygame.display.set_caption("Leaf Breeze")
        
        self.running = BooleanEx(True)
        self.manual_control = BooleanEx(True)

        self.constants = Constants()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.constants.screen_size.get(), flags = pygame.RESIZABLE)

        self.dt = 0
        self.mouse_click = EdgeDetectorEx()

        self.controls = Controls()
        self.menu = Menu(MenuType.UNDEFINED, self.constants, None)
        self.background = Background(self.constants)
        self.leaf = Leaf(self.constants)
        self.hand_recognition = HandRecognition()
        self.hand = Hand(self.constants)

        self.ai = AI(self.constants)
        self.target = TargetArea(self.constants)


    def RUNNING(self):
        return self.running.compare()

    def update(self):
        self.__updateEventManager()
        self.controls.update()

        #reset frame
        self.screen.fill("blue")

        self.hand_recognition.update()
        self.hand.setHandInfo(self.hand_recognition.getHandPosition()[0], 
                              self.hand_recognition.getFingerNumber())
        
        self.background.onScreen(self.screen)
        
        self.hand.onScreen(self.screen)
        self.leaf.onScreen(self.screen, self.clock)
        self.target.onScreen(self.screen)

        self.menu.addControls(self.controls)
        self.menu.onScreen(self.screen)
    
        self.__updateGameLoopCheck()
        self.__updateAiControls()

        pygame.display.update()
        self.dt = self.clock.tick(self.constants.FPS) / 1000


    def __updateGameLoopCheck(self):
        if self.menu.menus[0].ENABLED.compare():
            self.leaf.SHOULD_APPLY_GRAVITY.set(True)
        else: self.leaf.reset()
    
    def __updateAiControls(self):
        if self.menu.menus[0].ENABLED.compare(False):
            return None
        
        if self.target.REACHED.compare():
            prompt = self.ai.generate_simon_stays_task()
            parts = prompt.split(" ")

            self.percent = int(parts[0])
            self.finger = int(parts[1])

            if abs(self.percent - self.ai.last_percent) < 40:
                self.percent = (self.percent + 40 - abs(self.percent - self.ai.last_percent)) % 100
            
            if self.percent > 90:
                self.percent = 90
            if self.percent < 10:
                self.percent = 10
            
            self.x = self.constants.screen_size.width * self.percent / 100

            self.ai.setLast(self.percent, self.finger)
            self.target.addZone(self.x)
            self.leaf.move_to_target_area(self.x)

        if self.hand.check_target_area(self.x):
            self.target.REACHED.set(True)
            self.leaf.adjust_lives(-1)

        if self.leaf.check_target_area(self.x):
            self.target.REACHED.set(True)
            self.leaf.adjust_lives(1)


    def __updateEventManager(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEADDED:
                    self.controls.addJoystick(pygame.joystick.Joystick(event.device_index))
                    
                elif event.type == pygame.JOYDEVICEREMOVED:
                    self.controls.addJoystick(None)

                if event.type == pygame.QUIT:
                    self.running.set(False)
                    self.hand_recognition.exit()
                    print('\n\n')
                    pygame.quit()
        except: pass


            



    