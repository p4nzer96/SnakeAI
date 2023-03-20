import json
import tkinter as tk

from agents.agent_h import AgentH
from agents.agent_ts import AgentTS
from consts import DEATH, GOAL
from gui import SnakeGui
from snake_env import SnakeEnv
from stats import Stats


# Every n milliseconds, step function is called
def call_step():
    time = 30
    try:
        if env.last_event == DEATH:  # If last event is DEATH, reset the agent to initial state
            agent.reset()
    except IndexError:
        pass
    agent.step()  # Call the execution of a step of the agent
    stats.update()
    board.move_snake(env)  # Update the GUI with current environment
    root.after(time, call_step)  # Schedule the next execution of this function (recursive)


mode = "auto"  # The snake is controlled via the agent or the keyboard (latter not implemented)
algorithm = "bfs"  # Algorithm used by the agent

if __name__ == "__main__":

    if mode == "auto":
        # Creating the snake environment
        env = SnakeEnv(30, 30)  # Currently only 30x30 resolution is supported  by the gui
        stats = Stats(algorithm, env)
        # Agent selection: hamiltonian vs tree-search based
        if algorithm in ["gbfs", "bfs", "dfs", "bdir"]:
            agent = AgentTS(env, mode=algorithm)

        elif algorithm == "hamiltonian":
            agent = AgentH(env)

        else:
            raise ValueError("Unknown or not-implemented algorithm ")

        root = tk.Tk()
        w = env.dim_y * 20  # Width
        h = env.dim_y * 20  # Height

        screen_width = root.winfo_screenwidth()  # Width of the screen
        screen_height = root.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        x, y = (screen_width / 2) - (w / 2), (screen_height / 2) - (h / 2)

        # Defining the window
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.configure(bg='black')  # Selecting the background color
        root.title("Snake")  # Window title
        root.resizable(False, False)  # Setting the window as not resizable

        # Calling the window
        root.tk.call("tk", "scaling", 4.0)

        # Initializing the gui
        board = SnakeGui(env.snake.blocks, env.apple.position, env.wall)

        call_step()
        root.mainloop()

    elif mode == "manual":
        # TODO: this section allows the user to control the snake via keystrokes (not available in the current
        #  version of the code)
        pass
