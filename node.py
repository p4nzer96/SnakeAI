from collections import defaultdict


class Node:

    def __init__(self, node_x, node_y, parent=None, children=None, depth=None, heuristic=None):
        self.node_id = (node_x, node_y)  # Current node coordinate in the graph
        self.parent = parent  # Node parent
        self.children = [x for x in children] if children else []  # Children of the node

        self.depth = depth  # Current depth of the node
        self.heuristic_value = heuristic  # Heuristic value

    @property
    def coord(self):  # Node coordinate
        return self.node_id

    @property
    def x(self):  # Node x coordinate
        return self.node_id[0]

    @property
    def y(self):  # Node y coordinate
        return self.node_id[1]

    # Adds a parent to the node
    def add_parent(self, parent):
        self.parent = parent

    # Adds one or more children to the node
    def add_children(self, children):
        if isinstance(children, Node):
            self.children.append(children)
            children.add_parent(self)
        elif isinstance(children, list):
            self.children.extend(children)
        else:
            raise TypeError("Unknown type for children node")

    # Removes the parent from the node
    def remove_parent(self):
        self.parent = None

    # Removes a child to the node
    def remove_children(self, child_id):
        self.children = [child for child in self.children if child.node_id != child_id]

    def get_path(self):
        path = [self.coord]
        p_node = self.parent
        while p_node:
            path.append(p_node.coord)
            p_node = p_node.parent
        return path

    # Hash function to represent a single node
    def __hash__(self):
        name = self.node_id
        return hash("{}".format(name))

    # Two nodes are considered equal if they share the same id (coordinate)
    def __eq__(self, other):
        return self.node_id == other.node_id

    def __str__(self):
        return "{}".format(self.node_id)

    def __repr__(self):
        return self.__str__()
