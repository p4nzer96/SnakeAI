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
    time = 1
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
algorithm = "bfs"  # Algorith used by the agent
debug = True

if __name__ == "__main__":

    if debug is True:
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
    else:
        env = SnakeEnv(30, 30)
        stats = Stats(algorithm, env)
        # Agent selection: hamiltonian vs tree-search based
        if algorithm in ["gbfs", "bfs", "dfs", "bdir"]:
            agent = AgentTS(env, mode=algorithm)

        elif algorithm == "hamiltonian":
            agent = AgentH(env)

        else:
            raise ValueError("Unknown or not-implemented algorithm ")

        deltas = []
        moves_list = []
        status = dict()
        run = 0
        counter = 0
        apples = 1
        while True:
            if env.last_event and env.last_event == DEATH:  # If last event is DEATH, reset the agent to initial
                # state
                status[run] = {"Mode": algorithm, "Moves": moves_list, "Apples": apples, "Time": agent.time}
                agent.reset()
                counter = 0
                apples = 0
                run += 1
                moves_list = []
            elif env.last_event == GOAL:
                moves_list.append(counter)
                counter = 0
                apples += 1
            else:
                counter += 1

            agent.step()  # Call the execution of a step of the agent

            if env.death_count == 200:
                print("Finished -> Algorithm: {}".format(algorithm))
                with open("stats/stats_{}_{}.json".format(algorithm, "60"), 'w') as f:
                    f.write(json.dumps(status, indent=4))
                exit()
