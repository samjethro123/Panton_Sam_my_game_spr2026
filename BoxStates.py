
from state_machine import *
from settings import *

import pygame as pg

class BoxIdleState(State):
    def __init__(self, box):
        self.box = box
        self.name = "idle"

    def get_state_name(self):
        return "idle"

    def enter(self):
        self.box.image.fill(YELLOW)
        print('enter box idle state')

    def exit(self):
        print('exit box idle state')

    def update(self):
        # print('updating box idle state...')
        self.box.image.fill(YELLOW)
