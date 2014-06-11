import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 5
GAME_HEIGHT = 5

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Princess"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class Gem(GameElement):
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

class orangeGem(Gem):
    IMAGE = "OrangeGem"

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

class greenGem(Gem):
    IMAGE = "GreenGem"
    SOLID = True

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("Green gems are deadly! You are now a boulder."  )
        GAME_BOARD.del_el(PLAYER.x,PLAYER.y)
        deadlyrock = Rock()
        GAME_BOARD.register(deadlyrock)
        GAME_BOARD.set_el(PLAYER.x,PLAYER.y,deadlyrock)


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER

    rock_positions = [
            (2, 1),
            (1, 2),
            (3, 2),
            (2, 3)
        ]
    #how to fill up entire board!
    # rock_positions = []
    # for i in range(GAME_WIDTH):
    #     for j in range(GAME_HEIGHT):
    #         rock_positions.append((i, j))

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    for rock in rocks:
        print rock

    rocks[-1].SOLID = False

    GAME_BOARD.draw_msg("This game is wicked awesome.")

    gem = orangeGem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    deadlygem = greenGem()
    GAME_BOARD.register(deadlygem)
    GAME_BOARD.set_el(0, 1, deadlygem)

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:
            # If there's nothing there _or_ if the existing element is not solid, walk through
            GAME_BOARD.del_el(PLAYER.x,PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
