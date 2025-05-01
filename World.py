from nt import scandir
import pygame.math
import random
import math
import pygame
from typing import Optional  # Import Optional
class World:
    def __init__(self, s, a, controller, width, height):
        self.snake = s
        self.apple = a
        self.controller = controller
        self.width = width
        self.height = height
        self.score = 0
        self.total_deaths = 0
        self.maxScore = 0

        self.placeApple()

    def updateController(self, controller):
        self.controller = controller

    # Returns world size
    def getWorldSize(self):
        return pygame.math.Vector2(self.width, self.height)
    
    # Returns snake position as vector2
    def getSnakePos(self):
        return self.snake.body[0].xy
    
    # Returns apple position as vector2
    def getApplePos(self):
        return self.apple.pos
    
    # Tells controller to move agent
    def doMovement(self):
        self.controller.move()

    # Tells controller to handle input if needed
    def doInput(self, event: Optional[pygame.event] = None):
        self.controller.processInput(event)

    # Places apple in random location where snake isn't
    def placeApple(self):
        randX = 0
        randY = 0

        notDone = True
        while (notDone):
            randX = random.randint(0, int(math.floor(self.width / self.snake.get_size())) - 1) * self.snake.get_size()
            randY = random.randint(0, int(math.floor(self.height / self.snake.get_size())) - 1) * self.snake.get_size()

            notDone = False

            for i in range(self.snake.length()):
                if (randX == self.snake.x(i) and randY == self.snake.y(i)):
                    notDone = True

        self.apple.setPosition(pygame.math.Vector2(randX, randY))

    # Handles all collisions
    def doCollisions(self):
        if (self.snake.x(0) == self.apple.x() and self.snake.y(0) == self.apple.y()):
            self.placeApple()
            self.snake.grow()
            self.score += 1
            self.maxScore = max(self.score, self.maxScore)
        elif (self.snake.length() > 1):
            if (self.snake.colliding_self()):
                self.snake.reset()
                print(f"Score: {self.score}")
                self.score = 0
                self.total_deaths += 1
                print(f"Deaths: {self.total_deaths}")
        if (self.snake.colliding_wall()):
            self.snake.reset()
            print(f"Score: {self.score}")
            self.score = 0
            self.total_deaths += 1
            print(f"Deaths: {self.total_deaths}")

    # Draw snake and apple
    def draw(self, surface):
        self.snake.draw(surface)
        self.apple.draw(surface)

    def getDeaths(self):
        return self.total_deaths