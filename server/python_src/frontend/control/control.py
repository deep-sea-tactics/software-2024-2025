"""
Housed within here is all the control software for the ROV
"""

import pygame
from enum import Enum

class Actions(Enum):
    """
    Ways in which the pilot can interact with the ROV
    """

    # Rotational
    PITCH_UP = 1
    PITCH_DOWN = 2
    YAW_LEFT = 3
    YAW_RIGHT = 4
    ROLL_LEFT = 5
    ROLL_RIGHT = 6

    # Translational
    STRAFE_FORWARD = 7
    STRAFE_BACKWARD = 8
    STRAFE_LEFT = 9
    STRAFE_RIGHT = 10
    STRAFE_RISE = 11
    STRAFE_SINK = 12

def bind(key: int, to: Actions):
    """
    The desired way to create a new action object
    """
    Application.bound[key] = to

class Application():
    """
    The application contains all the keys and whatnot for individual actions
    """
    bound: dict[int, Actions] = {}

    def handle_input(key: int, value: bool):
        retrieved = Application.bound.get(key)

        if retrieved == None:
            return

        print(retrieved)
        print(value)

class ControlScheme:

    def define_all():
        """
        **Place all actions here**.

        Contained within this class is the entire control
        scheme for the ROV. It has all the actions,
        buttons, keys, etc.

        It is valid to bind multiple keys to one action,
        just try not to bind one key to multiple actions
        (unless, of course, in an emergency or for testing)
        """

        bind(pygame.K_w, Actions.STRAFE_FORWARD)
        bind(pygame.K_s, Actions.STRAFE_BACKWARD)
        bind(pygame.K_a, Actions.STRAFE_LEFT)
        bind(pygame.K_d, Actions.STRAFE_RIGHT)

        bind(pygame.K_q, Actions.ROLL_LEFT)
        bind(pygame.K_e, Actions.ROLL_RIGHT)
        
        bind(pygame.K_LEFT, Actions.YAW_LEFT)
        bind(pygame.K_RIGHT, Actions.YAW_RIGHT)
        bind(pygame.K_UP, Actions.PITCH_DOWN)
        bind(pygame.K_DOWN, Actions.PITCH_UP)

        bind(pygame.K_SPACE, Actions.STRAFE_RISE)
        bind(pygame.K_LCTRL, Actions.STRAFE_SINK)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((200, 200))

    application = Application()
    ControlScheme.define_all()

    running = True

    while running:

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                
                case pygame.KEYDOWN:
                    Application.handle_input(event.key, True)
                
                case pygame.KEYUP:
                    Application.handle_input(event.key, False)