import tkinter as tk

import numpy as np
from PIL import Image, ImageTk

from consts import *
from snake_env import SnakeEnv


class SnakeGui(tk.Canvas):
    def __init__(self, snake_pos, apple_pos, wall_pos):
        super().__init__(
            width=840, height=680, background="black", highlightthickness=0)

        self.wall = None
        self.wall_image = None
        self.apple = None
        self.apple_image = None
        self.snake_head = None
        self.snake_head_image = None
        self.snake_body = None
        self.snake_body_image = None

        self.snake_positions = np.multiply(snake_pos, 20) + 8
        self.apple_position = np.multiply(apple_pos, 20) + 8
        self.wall_position = np.multiply(wall_pos, 20) + 8
        self.snake_len = snake_pos.shape[0]

        self.load_assets()
        self.create_objects()

        self.pack()

    # Loading the assets

    def load_assets(self):

        self.snake_head_image = Image.open("./assets/snake_head.png")
        self.snake_head = ImageTk.PhotoImage(self.snake_head_image)

        self.snake_body_image = Image.open("./assets/snake_block.png")
        self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

        self.apple_image = Image.open("./assets/apple.png")
        self.apple = ImageTk.PhotoImage(self.apple_image)

        self.wall_image = Image.open("./assets/wall_block.png")
        self.wall = ImageTk.PhotoImage(self.wall_image)

    # Objects Creation

    def create_objects(self):

        snake_head_pos = self.snake_positions[0]
        snake_tail_pos = self.snake_positions[1:]

        self.create_image(*snake_head_pos, image=self.snake_head, tag="snake_head")

        for x_position, y_position in snake_tail_pos:
            self.create_image(x_position, y_position, image=self.snake_body, tag="snake")

        for x_position, y_position in self.wall_position:
            self.create_image(x_position, y_position, image=self.wall, tag="wall")

        self.create_image(*self.apple_position, image=self.apple, tag="apple")

        self.create_text(100, 10, text="Score: {}".format(self.snake_len - 3), font=10, fill="#fff", tags="score")

    # Move the snake

    def move_snake(self, env: SnakeEnv):

        self.snake_positions = np.multiply(env.snake.blocks, 20) + 8
        self.apple_position = np.multiply(env.apple.position, 20) + 8
        if env.last_event == GOAL:
            self.create_image(env.snake.body[0, -1], env.snake.body[0, -1], image=self.snake_body, tag="snake")
        elif env.last_event == DEATH:
            self.delete("all")
            self.create_objects()

        self.snake_len = env.snake.blocks.shape[0]
        self.itemconfigure("score", text=f"Score: {self.snake_len - 3}", tag="score")

        snake_head_pos = self.snake_positions[0]
        snake_tail_pos = self.snake_positions[1:]

        for segment, position in zip(self.find_withtag("snake_head"), snake_head_pos[None, :]):
            self.coords(segment, tuple(position))

        for segment, position in zip(self.find_withtag("snake"), snake_tail_pos):
            self.coords(segment, tuple(position))

        for segment, position in zip(self.find_withtag("apple"), self.apple_position[None, :]):
            self.coords(segment, tuple(position))
