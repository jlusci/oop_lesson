import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import time

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8
GAME_MOVES = 5

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

    def interact(self, player):
        GAME_BOARD.del_el(self.x, self.y)
        key = Key()
        GAME_BOARD.register(key)
        GAME_BOARD.set_el(self.x, self.y, key)  

class TallTree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

class ShortTree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True    

    def interact(self,player):
        print player.inventory
        if 'key' in player.inventory:
            GAME_BOARD.draw_msg("Congratulations! You win! Type 'q' to quit.")
            player.MOVES_LEFT = -1 # game over
            star = Star()
            GAME_BOARD.register(star)
            GAME_BOARD.set_el(player.x, player.y-2, star)
        else:
            GAME_BOARD.draw_msg("Find the key to open the chest.")

class Character(GameElement):
    IMAGE = "Princess"
    MOVES_LEFT = GAME_MOVES

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

class Helper(GameElement):
    IMAGE = "Cat"
    SOLID = True

    def interact(self, player):
        GAME_BOARD.draw_msg("Beware of the green gems! You will not survive!")

class Gem(GameElement):
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

class orangeGem(Gem):
    IMAGE = "OrangeGem"

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You earned 5 extra moves!")
        player.MOVES_LEFT += 5

class greenGem(Gem):
    IMAGE = "GreenGem"
    SOLID = True

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("Green gems are deadly! You are now a boulder. Game over, try again!"  )
        GAME_BOARD.del_el(PLAYER.x,PLAYER.y)
        deadlyrock = Rock()
        GAME_BOARD.register(deadlyrock)
        GAME_BOARD.set_el(PLAYER.x,PLAYER.y,deadlyrock)

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False 

    def interact(self, player):
        player.inventory.append("key")
        GAME_BOARD.draw_msg("Use the key to open the chest!")

class Star(GameElement):
    IMAGE = "Star"
    SOLID = True

class Enemy(GameElement):
    IMAGE = "EnemyBug"
    SOLID = True

    def interact(self, player):
        GAME_BOARD.draw_msg("The bug attacked and took away 1 move!")
        player.MOVES_LEFT -= 1
        
####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(6, 6, PLAYER)
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

    # rocks = []
    # for pos in rock_positions:
    #     rock = Rock()
    #     GAME_BOARD.register(rock)
    #     GAME_BOARD.set_el(pos[0], pos[1], rock)
    #     rocks.append(rock)

    # for rock in rocks:
    #     print rock

    # rocks[-1].SOLID = False
    keyrock = Rock()
    GAME_BOARD.register(keyrock)
    GAME_BOARD.set_el(6, 3, keyrock)

    talltree = TallTree()
    GAME_BOARD.register(talltree)
    GAME_BOARD.set_el(4, 1, talltree)

    shorttree = ShortTree()
    GAME_BOARD.register(shorttree)
    GAME_BOARD.set_el(2, 3, shorttree)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(1, 1, chest)

    GAME_BOARD.draw_msg("You have 5 moves to find the key and open the chest. Go!")

    gem1 = orangeGem()
    GAME_BOARD.register(gem1)
    GAME_BOARD.set_el(5, 5, gem1)

    gem2 = orangeGem()
    GAME_BOARD.register(gem2)
    GAME_BOARD.set_el(5, 2, gem2)

    gem3 = orangeGem()
    GAME_BOARD.register(gem3)
    GAME_BOARD.set_el(2, 4, gem3)

    deadlygem = greenGem()
    GAME_BOARD.register(deadlygem)
    GAME_BOARD.set_el(1, 6, deadlygem)

    helper = Helper()
    GAME_BOARD.register(helper)
    GAME_BOARD.set_el(1, 5, helper)

    bug = Enemy()
    GAME_BOARD.register(bug)
    GAME_BOARD.set_el(3, 4, bug)

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
    if KEYBOARD[key.Q]:
        sys.exit()

    if direction:
        # moves_left = GAME_MOVES - PLAYER.MOVES_TAKEN
        if PLAYER.MOVES_LEFT > 0:
            PLAYER.MOVES_LEFT -= 1
            GAME_BOARD.draw_msg("You have %r moves left." % PLAYER.MOVES_LEFT)

            next_location = PLAYER.next_pos(direction)
            next_x = next_location[0]
            next_y = next_location[1]

            if next_x in range(GAME_WIDTH) and next_y in range(GAME_HEIGHT):

                existing_el = GAME_BOARD.get_el(next_x, next_y)

                if existing_el:
                    existing_el.interact(PLAYER)

                if existing_el is None or not existing_el.SOLID:
                    # If there's nothing there _or_ if the existing element is not solid, walk through
                    GAME_BOARD.del_el(PLAYER.x,PLAYER.y)
                    GAME_BOARD.set_el(next_x, next_y, PLAYER)
            else:
                GAME_BOARD.draw_msg("Like we'd like you go off the map!  No go.")

        elif PLAYER.MOVES_LEFT == 0:
            GAME_BOARD.draw_msg("You are out of moves, you lose.")
