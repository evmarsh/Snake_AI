from Controller import Controller
from Snake import Snake
from World import World
import pygame

class PlayerController(Controller):
    def __init__(self, s):
        self.snake = s
        self.world = None

    def move(self):
        self.snake.move()

    def processInput(self, event):
        if (event == None):
            return
        direction = pygame.math.Vector2()
        direction.xy = 1, 0
        if (event.key == pygame.K_UP):
            direction.xy = 0, -1
        elif (event.key == pygame.K_DOWN):
            direction.xy = 0, 1
        elif (event.key == pygame.K_LEFT):
            direction.xy = -1, 0
        elif (event.key == pygame.K_RIGHT):
            direction.xy = 1, 0

        self.snake.change_direction(direction)

    def giveWorldView(self, w: World):
        self.world = w
