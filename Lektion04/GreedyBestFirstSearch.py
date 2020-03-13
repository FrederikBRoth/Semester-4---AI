import sys


class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

    def getstate(self):
        return self.STATE

    def path(self):  # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:  # while current node has parent
            current_node = current_node.PARENT_NODE  # make parent the current node
            path.append(current_node)  # add current node to path
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE[0][0]) + ' - Depth: ' + str(self.DEPTH)


'''
Search the tree for the goal state and return path from initial state to goal state
'''

A = ("A", 6)
B = ("B", 5)
C = ("C", 5)
D = ("D", 2)
E = ("E", 4)
F = ("F", 5)
G = ("G", 4)
H = ("H", 1)
I = ("I", 2)
J = ("J", 1)
K = ("K", 0)
L = ("L", 0)


def BEST_FIRST():
    fringe = []
    initial_node = Node(INITIAL_STATE)
    fringe = INSERT(initial_node, fringe)
    run = 1
    while run == 1:
        node = REMOVE_FIRST(fringe)
        if node.STATE == GOAL_STATE:
            return node.path()
        children = EXPAND(node)
        if children.__len__() == 0:
            return node.path()
        nodeDistance = sys.maxsize
        bestNode = None
        for element in children:
            if element.STATE[0][1] < nodeDistance:
                bestNode = element
                nodeDistance = element.STATE[0][1]
        fringe = INSERT(bestNode, fringe)
        print("fringe: {}".format(fringe))


'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''


def EXPAND(node):
    successors = []
    children = successor_fn(node.STATE[0])
    for child in children:
        s = Node(node)  # create node for each in state list
        s.STATE = child  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + 1
        successors = INSERT(s, successors)
    return successors


'''
Insert node in to the queue (fringe).
'''


def INSERT(node, queue):
    queue.append(node)
    return queue


'''
Insert list of nodes into the fringe
'''


def INSERT_ALL(list, queue):
    for node in list:
        queue.append(node)
    return queue


'''
Removes and returns the first element from fringe
'''


def REMOVE_FIRST(queue):
    removed = queue[0]
    queue.remove(removed)
    return removed


'''
Successor function, mapping the nodes to its successors
'''


def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]  # successor_fn( 'C' ) returns ['F', 'G']


INITIAL_STATE = (A, 0)
GOAL_STATE = (L, 0)
STATE_SPACE = {
    A: [(B, 1), (C, 2), (D, 4)],
    B: [(F, 5), (E, 4)],
    C: [(E, 1)],
    D: [(H, 1), (I, 4), (J, 2)],
    E: [(G, 2), (H, 3)],
    F: [(G, 2)],
    G: [(K, 6)],
    H: [(K, 6)],
    I: [(L, 3)],
    J: [],
    K: [],
    L: []

}

'''
Run tree search and display the nodes in the path to goal node
'''


def run():
    path = BEST_FIRST()
    print('Solution path:')
    for node in path:
        node.display()


if __name__ == '__main__':
    run()
