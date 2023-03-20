import gc
import random

from agents.agent import Agent
from node import Node
from utils import next_pos, coord_dir_conv, comp_dirs


def on_collect(obj):
    print(f"Object {obj} is being garbage collected.")


def explore(node, env):
    # Get node parent
    parent = node.parent

    depth = None

    nodes = []  # List of child nodes
    x_bound, y_bound = env.dim_x - 1, env.dim_y - 1

    # Translates a direction to coords
    for direction in ["up", "down", "right", "left"]:

        # Get child coordinates
        ch_x, ch_y = next_pos.get(direction)(*node.node_id)

        if parent:

            # Assign the depth to the node if available
            depth = parent.depth + 1 if parent.depth else None

            # If child coordinates are the same as parent, discard it
            if (ch_x, ch_y) == parent.coord:
                continue

        # if child coordinates are the same as snake coordinates, discard it
        if [ch_x, ch_y] in env.snake.body.tolist():
            continue

        # If child is inside the boundaries, expand it
        if 1 <= ch_x < x_bound and 1 <= ch_y < y_bound:
            nodes.append(Node(ch_x, ch_y, parent=node, depth=depth))

    return nodes


# Breadth First Search
def bfs(env):
    root = Node(*env.snake_head, depth=0)  # Root node
    goal = Node(*env.apple_pos)  # Goal node

    # Set of visited nodes: avoids to expand a node twice
    visited = set()

    # FIFO queue used to store discovered nodes
    queue = [root]

    # While queue is not empty
    while queue:

        # Dequeue a node from queue
        node = queue.pop(0)

        # Check if node is goal
        if node == goal:
            path = node.get_path()
            path.reverse()

            return path

        # If node has already been expanded, ignore it
        if node in visited:
            continue

        # Add the child to visited set
        visited.add(node)

        # Expand the current node
        children = explore(node, env)

        for child in children:
            # Append the child to the queue
            queue.append(child)

    return None


# Depth First Search
def dfs(env):
    root = Node(*env.snake_head, depth=0)  # Root node
    goal = Node(*env.apple_pos)  # Goal node

    # Set of visited nodes: avoids to expand a node twice
    visited = set()  # It also avoids circular paths

    # LIFO stack used to store discovered nodes
    stack = [root]

    # While stack is not empty
    while stack:

        # Pop the last added node from the stack
        node = stack.pop(0)

        # If the node is the goal, then return the full path
        if node == goal:
            path = node.get_path()
            path.reverse()

            return path

        # If child is in visited discard it
        if node in visited:
            continue

        visited.add(node)

        # Explore the current node
        children = explore(node, env)

        for child in children:
            # Append the child to the queue
            stack.insert(0, child)

    return None


# Greedy Best First Search
def greedy_search(env):
    root = Node(*env.snake_head, depth=0)  # Root node (snake's head)
    goal = Node(*env.apple_pos)  # Goal node (apple)

    # Sort paths by heuristic function
    def heuristic(c_node):
        x_n, y_n = c_node.coord
        x_g, y_g = goal.coord
        return abs(x_n - x_g) + abs(y_n - y_g)

    # Setting heuristic of root node
    root.heuristic_value = heuristic(root)

    # FIFO queue used to store discovered nodes
    queue = [root]  # Adding the root node to the queue

    # A set which holds the node currently visited
    visited = set(Node(*x) for x in env.snake_tail)

    while queue:

        # Pop a node from the queue
        node = queue.pop(0)

        # If the current node is equal to goal, retrieve the full path
        if node == goal:
            path = node.get_path()
            path.reverse()

            return path

        # If the node is already visited, don't expand it
        if node in visited:
            continue

        # If the node is not visited, expand it
        visited.add(node)

        # explore the adjacent nodes
        children = explore(node, env)

        # for every adjacent node
        for child in children:
            # update queue
            queue.append(child)

            # evaluate heuristic
            child.heuristic_value = heuristic(child)

        # Sort the queue according to heuristics (from lowest to highest value)
        queue.sort(key=lambda x: x.heuristic_value, reverse=False)

    return None


# Bidirectional Search
def bidirectional(env):
    root = Node(*env.snake_head, depth=0)  # Root node (goal node for backward path)
    goal = Node(*env.apple_pos)  # Goal node (root node for backward path)

    # Sets of visited nodes (forward and backward)
    visited_forward = set()
    visited_backward = set()

    # FIFO queues used for expand nodes
    queue_forward = [root]  # Queue of the forward path
    queue_backward = [goal]  # Queue of the backward path

    node_f, node_b = [], []

    # While both queues are not empty
    while queue_forward or queue_backward:

        # Deque a node from forward and backward queues

        # If forward queue is not empty, pop an element from it
        if queue_forward:
            node_f = queue_forward.pop(0)

        # If backward queue is not empty, pop an element from it
        if queue_backward:
            node_b = queue_backward.pop(0)

        # If current node is not visited yet (forward path)
        if node_f not in visited_forward:

            # Add the node to visited forward path
            visited_forward.add(node_f)

            # Explore
            children = explore(node_f, env)

            for child in children:
                queue_forward.append(child)

        if node_b not in visited_backward:

            # Add the node to visited backward path
            visited_backward.add(node_b)

            # Explore
            children = explore(node_b, env)

            for child in children:
                queue_backward.append(child)

        # If the forward search finds a node that has been explored in the backward search
        if node_f in visited_backward:
            # Extract the node from the visited backward set
            join_node = [x for x in visited_backward if x == node_f]

            # Compute full forward path
            forward_path = node_f.get_path()
            forward_path.reverse()

            # Compute full backward path
            backward_path = join_node[0].get_path()[1:]
            return forward_path + backward_path

        if node_b in visited_forward:
            # Extract the node from the visited forward set
            join_node = [x for x in visited_forward if x == node_b]

            # Compute full forward path
            forward_path = join_node[0].get_path()
            forward_path.reverse()

            # Compute full backward path
            backward_path = node_b.get_path()[1:]
            return forward_path + backward_path

    return None


class AgentTS(Agent):

    def __init__(self, env, mode="bfs", recover_trial=False):
        super().__init__(env)
        self._comm_queue = None  # Queue of commands
        self.mode = mode  # Algorithm used
        self.recover_capability = recover_trial
        self.time = []

    @property
    def comm_queue(self):
        return self._comm_queue

    @comm_queue.setter
    def comm_queue(self, nodes):

        if nodes is None or all(x in ["up", "down", "right", "left"] for x in nodes):
            self._comm_queue = nodes

        elif all(type(x) == tuple for x in nodes):
            n_dirs = [coord_dir_conv(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]

            if any(x is None for x in n_dirs):
                raise ValueError("Something went wrong in dirs generation")
            else:
                self._comm_queue = n_dirs

        else:
            raise ValueError("Something went wrong in path generation")

    def step(self):

        if not self.comm_queue:

            # Greedy Best First Search
            if self.mode == "gbfs":
                self.comm_queue = greedy_search(self.env)

            # Breadth First Search
            elif self.mode == "bfs":
                self.comm_queue = bfs(self.env)

            # Depth First Search
            elif self.mode == "dfs":
                self.comm_queue = dfs(self.env)

            # Bidirectional Search (BFS implementation)
            elif self.mode == "bdir":
                self.comm_queue = bidirectional(self.env)

            else:
                raise ValueError("Unknown mode")

        # If a command is found
        if self.comm_queue:
            command = self.comm_queue.pop(0)

        # If the queue is still empty (i.e. no solution was found, keep the current direction)
        else:
            if self.recover_capability:
                command = self.recover() if self.recover() else self.env.snake.direction
            else:
                command = self.env.snake.direction

        self.env.step(command)

    # Try to recover the snake from a possible death
    def recover(self):

        head = self.env.snake_head
        body = self.env.snake_body
        walls = self.env.wall_pos

        command_list = ["up", "down", "right", "left"]  # All possible direction of the snake
        current_dir = self.env.snake.direction  # Take the current direction of the snake

        command_list.remove(comp_dirs.get(current_dir))  # Remove the complementary direction from command list
        command_list.remove(current_dir)  # Remove the current direction from the command list

        command = self.env.snake.direction  # First, set the current direction as default command

        # Until the selected direction is brings us to a dead end, try another direction
        while next_pos.get(command)(*head) in body or next_pos.get(command)(*head) in walls:
            if not command_list:  # If command list is empty, return the current direction as command (NOP)
                return self.env.snake.direction
            command = random.choice(command_list)  # Select a random command from the command list
            command_list.remove(command)  # Remove the current command from the command list

        return command

    # Resets the agent to its initial state
    def reset(self):
        self.comm_queue = None  # Queue of commands
        self.time = []
