import tkinter as tk
import numpy as np
from gui import SnakeGui
from snake_env import SnakeEnv


def call_step():
    env.step()
    snake_pos = np.multiply(env.snake.blocks, 20) + 8
    apple_pos = np.multiply(env.apple.position, 20) + 8
    board.move_snake(snake_pos, apple_pos)
    root.after(50, call_step)


env = SnakeEnv()

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)
root.tk.call("tk", "scaling", 4.0)
board = SnakeGui(env.snake.blocks, env.apple.position, env.wall)

call_step()
root.mainloop()