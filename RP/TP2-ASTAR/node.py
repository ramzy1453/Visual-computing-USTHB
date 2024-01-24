import math


class Node:
    def __init__(self, rushHourPuzzle, parent=None, action="", c=1, heuristic=1):
        self.state = rushHourPuzzle
        self.parent = parent
        self.action = action
        self.g = 0 if not self.parent else self.parent.g + c
        self.set_f(heuristic)

    def set_f(self, heuristic):
        heuristics = [
            self.first_heuristic(),
            self.second_heuristic(),
            self.third_heuristic(),
        ]
        self.f = self.g + heuristics[heuristic - 1]

    # distance between X and goal
    def first_heuristic(self):
        for vehicle in self.state.vehicles:
            if vehicle["id"] == "X":
                return self.state.board_width - 2 - vehicle["x"]

    def heuristic_ramzy(self):
        for vehicule in self.state.vehicles:
            if vehicule["id"] == "X":
                return math.sqrt(
                    (self.state.board_height - vehicule["y"] - 1) ** 2
                    + (self.state.board_width - 2 - vehicule["x"]) ** 2
                )

    # numbers of vehicle who block the X
    def second_heuristic(self):
        for vehicle in self.state.vehicles:
            if vehicle["id"] == "X":
                unique_vehicles = set(self.state.board[vehicle["y"]][vehicle["x"] :])
                if " " in unique_vehicles:
                    return self.first_heuristic() + len(unique_vehicles) - 2
                return self.first_heuristic() + len(unique_vehicles) - 1

    # calculate the number of vertical and horizontal vehicles that block X
    def third_heuristic(self):
        blocking_vehicles = set()
        for vehicle in self.state.vehicles:
            if vehicle["id"] == "X":
                for other_vehicle in self.state.vehicles:
                    if (
                        vehicle["id"] != other_vehicle["id"]
                        and vehicle["x"] == other_vehicle["x"]
                    ):
                        blocking_vehicles.add(other_vehicle["id"])

        for vehicle in self.state.vehicles:
            if vehicle["id"] == "X":
                for other_vehicle in self.state.vehicles:
                    if (
                        vehicle["id"] != other_vehicle["id"]
                        and vehicle["y"] == other_vehicle["y"]
                    ):
                        blocking_vehicles.add(other_vehicle["id"])

        return len(blocking_vehicles) + self.first_heuristic()

    def getPath(self):
        states = []
        node = self
        while node != None:
            states.append(node.state)
            node = node.parent
        return states[::-1]

    def getSolution(self):
        actions = []
        node = self
        while node != None:
            actions.append(node.action)
            node = node.parent
        return actions[::-1]

    def __lt__(self, other):
        # Define the comparison method for sorting based on the f values
        return self.f < other.f
