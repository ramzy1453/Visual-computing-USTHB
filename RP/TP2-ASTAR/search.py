from node import Node
from queue import Queue, PriorityQueue
from rush_hour_puzzle import RushHourPuzzle


class Search:

    """blind_search"""

    @staticmethod
    def BFS(initial_state):
        initial_node = Node(initial_state)
        # Check if the start element is the goal
        if initial_node.state.isGoal():
            return initial_node, 0

        # Create the OPEN FIFO queue and the CLOSED list
        open = Queue()  # A FIFO queue
        open.put(initial_node)
        closed = list()

        step = 0
        while True:
            print(f"*** Step {step} ***")
            # Check if the OPEN queue is empty => goal not found
            if open.empty():
                return None, step
            # Get the first element of the OPEN queue
            current = open.get()
            # Put the current node in the CLOSED list
            closed.append(current)
            print(f"*  Closed {closed.count}   *")
            step += 1
            # Generate the successors of the current node
            for action, successor in current.state.successorFunction():
                child = Node(successor, current, action)
                # Check if the child is not in the OPEN queue and the CLOSED list
                if child.state.board not in [
                    node.state.board for node in closed
                ] and child.state.board not in [
                    node.state.board for node in list(open.queue)
                ]:
                    # Check if the child is the goal
                    if child.state.isGoal():
                        print("Goal reached")
                        return child, step
                    # Put the child in the OPEN queue
                    open.put(child)

    @staticmethod
    def a_star(initial_state, h):
        open = PriorityQueue()
        closed = list()
        initial_node = Node(initial_state)
        initial_node.set_f(h)
        if initial_node.state.isGoal():
            return initial_node, 0
        open.put(initial_node)
        step = 0
        while True:
            print(f"step {step}")
            current = open.get()
            if current.state.isGoal():
                return current, step
            closed.append(current)
            step += 1
            for action, successor in current.state.successorFunction():
                child = Node(successor, current, action)
                child.set_f(h)

                if (
                    child.state.board not in [node.state.board for node in closed]
                ) and (
                    child.state.board
                    not in [node.state.board for node in list(open.queue)]
                ):
                    open.put(child)
                else:
                    if (
                        child.state.board
                        in [node.state.board for node in list(open.queue)]
                    ) and child.f >= current.f:
                        child = current
                    else:
                        if (
                            child.state.board in [node.state.board for node in closed]
                        ) and child.f < current.f:
                            if child in closed:
                                closed.remove(child)
                                open.put(child)


initial_state = RushHourPuzzle("1.csv")
RushHourPuzzle.pretty_print(initial_state.board)
goal_node, step = Search.a_star(initial_state, 4)  # Change to the A* search method
if goal_node is not None:
    print(f"Path cost: {goal_node.g}")
    print(f"Number of steps: {step}")
    print("Moves: {}".format(" ".join(map(str, goal_node.getSolution()))))
else:
    print("No solution found!")
