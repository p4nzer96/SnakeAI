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

mode = "gui"

if __name__ == "__main__":

    if mode == "gui":

        env = SnakeEnv()

        root = tk.Tk()
        w = 1400  # Width
        h = 600  # Height

        screen_width = root.winfo_screenwidth()  # Width of the screen
        screen_height = root.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (w / 2)
        y = (screen_height / 2) - (h / 2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.configure(bg='black')
        root.title("Snake")
        root.resizable(False, False)

        root.tk.call("tk", "scaling", 4.0)
        board = SnakeGui(env.snake.blocks, env.apple.position, env.wall)

        call_step()
        root.mainloop()

    elif mode == "manual":
        pass
