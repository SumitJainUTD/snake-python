import random
import time

import pygame
from pygame.locals import *

BLOCK_WIDTH = 40
SCREEN_SIZE = 1000


class Snake():
    def __init__(self, parent_screen, length=5):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg")
        self.x = [BLOCK_WIDTH] * self.length
        self.y = [BLOCK_WIDTH] * self.length
        self.direction = "right"

    def draw(self):
        self.parent_screen.fill((58, 59, 36))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        # pygame.display.update()

    def increase(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"

    def move_up(self):
        if self.direction != "down":
            self.direction = "up"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def move(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "right":
            self.x[0] += BLOCK_WIDTH
        if self.direction == "left":
            self.x[0] -= BLOCK_WIDTH
        if self.direction == "down":
            self.y[0] += BLOCK_WIDTH
        if self.direction == "up":
            self.y[0] -= BLOCK_WIDTH

        if self.x[0] > SCREEN_SIZE:
            self.x[0] = 0

        if self.x[0] < 0:
            self.x[0] = SCREEN_SIZE

        if self.y[0] > SCREEN_SIZE:
            self.y[0] = 0

        if self.y[0] < 0:
            self.y[0] = SCREEN_SIZE

        self.draw()


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple_img = pygame.image.load("resources/apple.jpg")
        self.x = BLOCK_WIDTH * 4
        self.y = BLOCK_WIDTH * 5

    def draw(self):
        self.parent_screen.blit(self.apple_img, (self.x, self.y))

    def move(self):
        self.x = random.randint(0, 24) * BLOCK_WIDTH
        self.y = random.randint(0, 24) * BLOCK_WIDTH


class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game - Sumit")
        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, 150)
        self.surface = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.surface.fill((58, 59, 36))
        self.snake = Snake(self.surface, 5)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.score = 0

        pygame.mixer.init()
        self.play_background_music()

    def eat(self, x1, y1, x2, y2):
        return x1 == x2 and y1 == y2

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"{self.score}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))

    def play(self):
        self.snake.move()
        self.apple.draw()
        self.display_score()

        # time.sleep(0.15)

        if self.eat(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase()
            self.apple.move()
            self.score += 1
            self.play_sound("ding")

        for i in range(3, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                self.play_sound('crash')
                raise "Collision Occurred"

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.score = 0

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game over! score is {self.score}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again:  press Enter. To exit:  press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.update()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
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
                elif event.type == self.SCREEN_UPDATE:
                    try:
                        if not pause:
                            self.play()
                            pygame.display.update()

                    except Exception as e:
                        self.show_game_over()
                        pause = True
                        self.reset()


                    pygame.time.Clock().tick(60)

            # try:
            #     if not pause:
            #         self.play()
            #
            # except Exception as e:
            #     self.show_game_over()
            #     pause = True
            #     self.reset()


game = Game()
game.run()
