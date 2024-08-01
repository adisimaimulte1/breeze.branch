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
        self.screen = pygame.display.set_mode(self.constants.screen_size.get())

        self.dt = 0
        self.catch_streak = 0
        self.SOUND_DETECTOR = EdgeDetectorEx()

        self.controls = Controls()
        self.menu = Menu(MenuType.UNDEFINED, self.constants, None)
        self.background = Background(self.constants)
        self.leaf = Leaf(self.constants)
        self.hand_recognition = HandRecognition()
        self.hand = Hand(self.constants)
        self.aux_hand = AuxiliaryHand(self.constants)

        self.ai = AI(self.constants)
        self.target = TargetArea(self.constants)

        self.menu.addControls(self.controls)
        self.playMusic()

    def playMusic(self):
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

    def RUNNING(self):
        return self.running.compare()

    def update(self):
        self.__updateEventManager()

        #reset frame
        self.screen.fill("blue")

        self.hand_recognition.update()
        self.hand.setHandInfo(self.hand_recognition.getHandPosition()[0], 
                              self.hand_recognition.getFingerNumber())
        
        self.background.onScreen(self.screen)
        
        self.hand.onScreen(self.screen)
        self.leaf.onScreen(self.screen, self.clock)
        self.target.onScreen(self.screen)
        self.aux_hand.onScreen(self.screen)

        self.menu.onScreen(self.screen)
    
        self.__updateGameLoopCheck()
        self.__updateAiControls()
        self.__updateMusic()

        pygame.display.update()
        self.dt = self.clock.tick(self.constants.FPS) / 1000



    def __updateGameLoopCheck(self):
        if self.menu.menus[0].ENABLED.compare():
            self.leaf.SHOULD_APPLY_GRAVITY.set(True)
        else: self.leaf.reset()
    
    def __updateAiControls(self):
        if self.menu.menus[0].ENABLED.compare(False):
            self.controls.update()
            return None
        
        if self.target.REACHED.compare():
            prompt = self.ai.generate_simon_stays_task()
            parts = prompt.split(" ")

            try:
                self.percent = int(parts[0])
                self.finger = int(parts[1])
            except: pass

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
            self.aux_hand.set_fingers(self.finger)

            funny = self.ai.generate_dialogue(self.finger, self.leaf.lives, self.catch_streak, self.hand.pose.x)
            self.ai.speak(funny)


        if self.hand.check_target_area(self.x) and self.hand.show_index == self.aux_hand.show_index:
            self.target.REACHED.set(True)

            if self.ai.lastPromptWasSimon():
                self.leaf.adjust_lives(-1)
            else: self.leaf.adjust_lives(1)

            self.catch_streak += 1

        if self.leaf.check_target_area(self.x):
            if self.leaf.ON_TARGET.compare(False):
                self.leaf.ON_TARGET.set(True)
                self.leaf.start_time = pygame.time.get_ticks()

            if pygame.time.get_ticks() - self.leaf.start_time > self.leaf.total_time:
                self.target.REACHED.set(True)

                if self.ai.lastPromptWasSimon():
                    self.leaf.adjust_lives(1)
                else: self.leaf.adjust_lives(-1)
                
                self.catch_streak = 0

        else: self.leaf.ON_TARGET.set(False)

        if self.leaf.lives == 0 and abs(self.leaf.pose.x - self.hand.pose.x) > 30 and self.hand.show_index == 0:
            self.leaf.DISABLE.set(True)

            self.menu.reset()
            self.leaf.reset()
            self.target.reset()

            self.menu.check()
            self.controls.update()
            self.playMusic()
            
            self.aux_hand.is_visible = False

    def __updateMusic(self):
        self.SOUND_DETECTOR.set(self.constants.SOUND.get())
        self.SOUND_DETECTOR.update()

        if self.SOUND_DETECTOR.rising:
            pygame.mixer.music.unpause()
        
        elif self.SOUND_DETECTOR.falling:
            pygame.mixer.music.pause()



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


            



    