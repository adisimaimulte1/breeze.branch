from leafbreeze.Components.BetterClasses.booleanEx import *
from leafbreeze.Components.Constants.constants import *

from leafbreeze.Components.controls import *
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


    def recalculate(self):
        resize_screen = self.constants.checkScreenSize(self.screen.get_size())

        if self.constants.recalculate.compare(False):
            return 0
        
        if resize_screen:
            self.screen = pygame.display.set_mode(self.constants.screen_size.get(), pygame.RESIZABLE)
        else: 
            self.constants.screen_size = ScreenSize(self.screen.get_size()[0], self.screen.get_size()[1])

        self.constants.recalculate.set(False)


    def RUNNING(self):
        return self.running.compare()

    def update(self):
        self.recalculate()
        self.__updateEventManager()

        #reset frame
        self.screen.fill("black")

        if self.manual_control.compare():
            self.__updateControls()


        pygame.display.update()
        self.dt = self.clock.tick(self.constants.FPS) / 1000

        self.__updateScreenshoot()
    

    
    def __updateEventManager(self):

        try:
            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEADDED:
                    self.controls.addJoystick(pygame.joystick.Joystick(event.device_index))
                    
                elif event.type == pygame.JOYDEVICEREMOVED:
                    self.controls.addJoystick(None)

                if event.type == pygame.QUIT:
                    self.running.set(False)
                    print('\n\n')
                    pygame.quit()
        except: pass


    def __updateControls(self):
        self.controls.update()

        if self.controls.using_joystick.compare():
            self.__updateJoystick()


    def __updateJoystick(self):
        left_x = round(self.controls.joystick.get_axis(self.controls.keybinds.left_x), 4)
        left_y = round(self.controls.joystick.get_axis(self.controls.keybinds.left_y), 4)
        right_x = round(self.controls.joystick.get_axis(self.controls.keybinds.right_x), 4)

        self.__updateJoystickButtons()

        ...

    def __updateJoystickButtons(self):
        ...

    def __updateScreenshoot(self):
        if exists(self.controls.joystick):
            if self.manual_control.compare(False):
                self.controls.update()
            
            if self.controls.joystick_detector[self.controls.keybinds.screenshot_button].rising:
                #take a screenshot

                screenshot = pygame.Surface(self.constants.screen_size.get())
                screenshot.blit(self.screen, (0, 0))

                date_and_time_info = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                image_name_with_time_format = "{0}.png".format(date_and_time_info)
                individual_data = date_and_time_info.split("-")

                device_screenshot_path = os.path.join(os.path.join(os.path.dirname(__file__), "Screenshots"), image_name_with_time_format)
                pygame.image.save(screenshot, device_screenshot_path)

                print("\n\nyou took a screenshot :o -- check it out:")

                for each in individual_data: # easter egg? :0
                    if each == '42' or each == '69':
                        print("\n\nnice 😎")
                        break

                print(device_screenshot_path)



            



    