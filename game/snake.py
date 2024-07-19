import time

import pygame
from pygame.locals import *


class SnakeBody():
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg")
        self.x = 100
        self.y = 100
        self.direction ="right"

    def draw(self):
        self.parent_screen.fill((58, 59, 36))
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()

    def move_left(self):
        if self.direction != "right":
            self.direction ="left"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"

    def move_up(self):
        if self.direction != "down":
            self.direction ="up"

    def move_down(self):
        if self.direction != "up":
            self.direction ="down"

    def move(self):
        if self.direction == "right":
            self.x += 10
            self.draw()
        if self.direction == "left":
            self.x -= 10
            self.draw()
        if self.direction == "down":
            self.y += 10
            self.draw()
        if self.direction == "up":
            self.y -= 10
            self.draw()

class Game():
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 500))
        self.surface.fill((58, 59, 36))
        self.snake = SnakeBody(self.surface)
        self.snake.draw()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_LEFT:
                        self.snake.move_left()

                elif event.type == QUIT:
                    running = False

            self.snake.move()
            time.sleep(0.2)

game = Game()
game.run()
