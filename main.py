import pygame
import random
import math
from tkinter import messagebox
from tkinter import *


def game_over_screen():
    window = Tk()
    window.withdraw()
    screen = messagebox.askquestion(" GAME OVER ", "Do you want to restart the game?")
    if screen == "yes":
        restart = Snake()
        restart.run()


class Snake:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.FPS = 12
        self.BLACK = (0, 0, 0)
        self.GREEN_HEAD = (0, 255, 0)
        self.GREEN_BODY = (100, 255, 130)
        self.WHITE = (255, 255, 255)
        self.PURPLE = (128, 0, 128)
        self.size = 20
        (self.width, self.height) = (600, 600)
        self.x_snake = self.size*2
        self.y_snake = self.size*2
        self.snake_body = [(self.x_snake, self.y_snake)]
        self.gameOver = False
        self.food_eaten = False
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake game')
        self.running = True
        self.pos_x = math.floor(random.randint(self.size, self.width - self.size * 2) / self.size) * self.size
        self.pos_y = math.floor(random.randint(self.size, self.width - self.size * 2) / self.size) * self.size

    def grid(self):
        limit = int(self.width / self.size)
        lines = [x * self.size for x in range(limit)]
        for point in lines:
            pygame.draw.line(self.screen, self.WHITE, (point, 0), (point, self.width), 1)
            pygame.draw.line(self.screen, self.WHITE, (0, point), (self.width, point), 1)
            # THE BORDER
            pygame.draw.rect(self.screen, self.BLACK, [point, self.width - self.size, self.size, self.size], 0)
            pygame.draw.rect(self.screen, self.BLACK, [self.width - self.size, point, self.size, self.size], 0)
            pygame.draw.rect(self.screen, self.BLACK, [0, point, self.size, self.size], 0)
            pygame.draw.rect(self.screen, self.BLACK, [point, 0, self.size, self.size], 0)

    def food(self):
        food = (self.pos_x, self.pos_y)
        pygame.draw.rect(self.screen, self.PURPLE, [self.pos_x, self.pos_y, self.size, self.size], 0)
        if len(list(filter(lambda x: x == food, self.snake_body))) > 0:
            self.food_eaten = True
            self.pos_x = math.floor(random.randint(self.size * 2, self.width - self.size * 3) / self.size) * self.size
            self.pos_y = math.floor(random.randint(self.size * 2, self.width - self.size * 3) / self.size) * self.size

    def snake(self):
        self.snake_body.insert(0, (self.x_snake, self.y_snake))
        if not self.food_eaten and not self.gameOver:
            self.snake_body.pop()
        self.food_eaten = False
        for i, p in enumerate(self.snake_body):
            if i == 0:
                pygame.draw.rect(self.screen, self.GREEN_HEAD, [p[0], p[1], self.size, self.size], 0)
            else:
                pygame.draw.rect(self.screen, self.GREEN_BODY, [p[0], p[1], self.size, self.size], 0)

    def game_over_check(self, x, y):
        snake_check = self.snake_body[:]
        snake_check.pop(0)
        for pos in snake_check:
            if pos[0] == x and pos[1] == y:
                return True
        if x == 0 or y == 0 or x == (self.width - self.size) or y == (self.width - self.size):
            return True
        else:
            return False

    def run(self):
        snakeY_change = 0
        snakeX_change = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and not self.gameOver:
                    if event.key == pygame.K_DOWN:
                        snakeY_change = snakeX_change = 0
                        snakeY_change += self.size
                    elif event.key == pygame.K_UP:
                        snakeY_change = snakeX_change = 0
                        snakeY_change -= self.size
                    elif event.key == pygame.K_LEFT:
                        snakeY_change = snakeX_change = 0
                        snakeX_change -= self.size
                    elif event.key == pygame.K_RIGHT:
                        snakeY_change = snakeX_change = 0
                        snakeX_change += self.size

            if self.gameOver:
                game_over_screen()
                return
            self.y_snake += snakeY_change
            self.x_snake += snakeX_change
            self.screen.fill(self.BLACK)
            self.grid()
            self.snake()
            self.food()
            if self.game_over_check(self.x_snake, self.y_snake):
                snakeY_change = snakeX_change = 0
                self.gameOver = True
            self.clock.tick(self.FPS)
            pygame.display.flip()


snake = Snake()
snake.run()
