from leafbreeze.Components.BetterClasses.mathEx import *
from leafbreeze.Components.Constants.constants import *
from leafbreeze.Components.Menu.buttons import *
from leafbreeze.Components.Menu.menus import *
from leafbreeze.Components.Menu.enums import *
from leafbreeze.Components.controls import *
import pygame

# file combining all the logic for the menu


class Menu(AbsMenu):
    def __init__(self, 
                 name: MenuType, 
                 constants: Constants, 
                 background: pygame.Surface | None, 
                 always_display: bool = False, 
                 overlap: bool = False):

        super().__init__(name, constants, background, always_display, overlap)

        self.selected = Selected.PLAY # default selection when entering the menu
        self.clicked = False

        self.value = "_"

        self.create()
        self.recalculate()

        self.menus = [self.game, self.main_menu]
        self.main_menu.ENABLED.set(True)

    def createGame(self):
        self.GAME = EmptyButton(name = Selected.GAME,
                                    quadrant_surface = None,
                                    title_surface = None, 
                                    selected_title_surface = None)
        
        self.game = Submenu(MenuType.GAME, self.constants, None)
        self.game.setButtons([self.GAME])
    
    def createMainMenu(self):
        self.PLAY = DynamicButton(name = Selected.PLAY,
                                quadrant_surface = None,
                                title_surface = img_play_button,
                                selected_title_surface = img_selected_play_button)
        
        self.SOUND = BoolButton(name = Selected.SOUND,
                                    constants = self.constants,
                                    value = self.constants.SOUND,
                                    quadrant_surface = None,
                                    title_surface = [img_sound_button_closed, img_sound_button_open],
                                    selected_title_surface = [img_selected_sound_button_closed, img_selected_sound_button_open])

        self.PLAY.link(key = (Dpad.UP, Dpad.RIGHT, Dpad.DOWN, Dpad.LEFT),
                              value = (None, None, Selected.SOUND, None),
                              next = Selected.GAME)
        self.SOUND.link(key = (Dpad.UP, Dpad.RIGHT, Dpad.DOWN, Dpad.LEFT),
                              value = (Selected.PLAY, None, None, None))
        
        self.main_menu = Submenu(MenuType.MAIN_MENU, self.constants, None)


    def recalculateMainMenu(self):
        self.PLAY.titleCenter((self.constants.screen_size.half_w, self.constants.screen_size.half_h * 1.2))
        self.SOUND.titleCenter((self.constants.screen_size.half_w, self.constants.screen_size.half_h * 1.6))

        self.main_menu.setButtons([self.PLAY, self.SOUND])



    def createResetMenu(self):
        ...
    
    def recalculateResetMenu(self):
        ...
    
    def createPauseMenu(self):
        ...
    
    def recalculatePauseMenu(self):
        ...




    # called everytime when reentering the menu
    def reset(self):
        self.selected = Selected.PLAY_BUTTON
        self.enable()

    def create(self):
        self.createGame()
        self.createMainMenu()
        self.createResetMenu()
        self.createPauseMenu()

    def recalculate(self):
        self.recalculateMainMenu()
        self.recalculateResetMenu()
        self.recalculatePauseMenu()

    def __resetButtonsDefault(self):
        if not self.constants.reset_buttons_default:
            return None
        
        for menu in self.menus:
            menu.resetButtonsDefault()
        
        self.constants.reset_buttons_default = False

    def check(self):
        for menu in self.menus:
            menu.check()
    
    def update(self):
        return None



    def enable(self):
        
        for menu in self.menus: # first check in overlapping is allowed
            if self.selected in menu.name.value and (menu.always_display or menu.overlap):
                return 0

        for menu in self.menus: # else shut down every other menu, keep the selected one
            menu.resetToggles()

            if self.selected in menu.name.value:
                menu.ENABLED.set(True)
                
            else: menu.ENABLED.set(False)

    def addControls(self, controls: Controls):
        self.controls = controls

    def addKey(self, key):
        self.value = key

    def onScreen(self, screen: pygame.Surface):
        self.__resetButtonsDefault()

        if self.controls.using_joystick.compare():
            self.clicked = self.controls.joystick_detector[self.controls.keybinds.zero_button].rising
            self.default = self.controls.joystick_detector[self.controls.keybinds.erase_trail_button].rising
            key = self.__updatePressedDpad()
        else:
            self.clicked = False
            self.default = False
            key = None

        moved = False

        for menu in self.menus: # loop through each menu
            menu.update(self.selected, self.clicked, default = self.default, value = self.value)
            toggles = menu.getToggles()

            for item in toggles: # enable all the menus the toggle buttons say you to do
                for each in self.menus:
                    if item[0] is each.name:
                        each.ENABLED.set(item[1])
                

            next = menu.updateSelections(key) # gets the next button to move to
            if next is not None and not moved: # you can move only once / loop, because otherwise things go boom
                
                if key is not None:
                    inverse = Controls.Keybinds.inverse(key)
                    for each in self.menus: # check in all the menus, in all the buttons
                        for button in each.buttons: # the desired next button, to see if has to remember the move
                            if button.remember_links[inverse][0] and button.name is next: 
                                try: 
                                    if not button.on()[1]:
                                        raise("wise words here")
                                except: button.remember_links[inverse][1] = self.selected

                self.selected = next
                self.enable() # update menus
                moved = True

            menu.onScreen(screen)


    def __updatePressedDpad(self):
        if self.controls.keybinds.state is JoyType.PS4:
                if self.controls.joystick_detector[self.controls.keybinds.turn_0].rising:
                    return Dpad.UP
                elif self.controls.joystick_detector[self.controls.keybinds.turn_90].rising:
                    return Dpad.RIGHT
                elif self.controls.joystick_detector[self.controls.keybinds.turn_180].rising:
                    return Dpad.DOWN
                elif self.controls.joystick_detector[self.controls.keybinds.turn_270].rising:
                    return Dpad.LEFT

        else: return self.controls.keybinds.updateDpad(self.controls.joystick.get_hat(0))
