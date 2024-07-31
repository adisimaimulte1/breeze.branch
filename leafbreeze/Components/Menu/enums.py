from enum import Enum, auto
 
# file containing the majority of enums used for the menus

class ButtonType(Enum):
    BOOL = auto()
    INT = auto()
    STRING = auto()
    UNDEFINED = auto()

class Selected(Enum):
    PLAY = auto()
    SOUND = auto()

    RESET = auto()
    HOME = auto()

    RESUME = auto()
    EXIT = auto()

    GAME = auto()


# menus with their respective buttons
class MenuType(Enum):
    MAIN_MENU = [Selected.PLAY, Selected.SOUND]
    RESET_MENU = [Selected.RESET, Selected.HOME]
    PAUSE_MENU = [Selected.RESUME, Selected.EXIT]
    GAME = [Selected.GAME]
    UNDEFINED = auto()

# inputs with their respective display extension
class InputType(Enum):
    DIMENSION = ' cm'
    PERCENT = '%'
    FONT = auto()
    COLOR = auto()
    IMAGE_PATH = auto()