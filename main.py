import tkinter as tk

from agents.agent_h import AgentH
from agents.agent_ts import AgentTS
from gui import SnakeGui
from snake_env import SnakeEnv
from consts import DEATH


def call_step():
    try:
        if env.last_event == DEATH:
            agent.reset()
    except IndexError:
        pass
    agent.step()
    board.move_snake(env)
    root.after(5, call_step)


mode = "gui"
algorithm = "bdir"

if __name__ == "__main__":

    if mode == "gui":

        env = SnakeEnv(30, 30)

        if algorithm != "hamiltonian":
            agent = AgentTS(env, mode=algorithm)
        else:
            agent = AgentH(env)

        root = tk.Tk()
        w = env.dim_y * 20  # Width
        h = env.dim_y * 20  # Height

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
