from copy import deepcopy
import csv


class RushHourPuzzle:
    def __init__(self, puzzle_file):
        self.set_vehicles(puzzle_file)
        self.set_board()

    def set_vehicles(self, puzzle_file):
        with open(puzzle_file) as file:
            csvreader = csv.reader(file)
            w, h = next(csvreader)
            self.board_width, self.board_height = int(w), int(h)
            self.vehicles = []
            self.walls = []
            for line in csvreader:
                if line[0] == "#":
                    self.walls.append((int(line[1]), int(line[2])))
                else:
                    id, x, y, orientation, length = line
                    vehicle = {
                        "id": id,
                        "x": int(x),
                        "y": int(y),
                        "orientation": orientation,
                        "length": int(length),
                    }
                    self.vehicles.append(vehicle)

    def set_board(self):
        self.board = [
            [" " for _ in range(self.board_width)] for _ in range(self.board_height)
        ]
        for x, y in self.walls:
            self.board[y][x] = "#"
        for vehicle in self.vehicles:
            x, y = vehicle["x"], vehicle["y"]
            if vehicle["orientation"] == "H":
                for i in range(vehicle["length"]):
                    self.board[y][x + i] = vehicle["id"]
            else:
                for i in range(vehicle["length"]):
                    self.board[y + i][x] = vehicle["id"]

    @staticmethod
    def pretty_print(board):
        str_line = "----------------------"
        printedBoard = f"{str_line}\n" + "".join(
            map(lambda line: " | ".join(map(str, line)) + f"\n{str_line}\n", board)
        )
        print(printedBoard)

    def is_goal(self):
        for vehicle in self.vehicles:
            if vehicle["id"] == "X" and vehicle["x"] == self.board_width - 2:
                return True
        return False

    def successorFunction(self):
        succs = list()
        for index, vehicle in enumerate(self.vehicles):
            x_position = vehicle["x"]
            y_position = vehicle["y"]
            if vehicle["orientation"] == "H":
                if x_position > 0 and self.board[y_position][x_position - 1] == " ":
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    successor.vehicles[index]["x"] = x_position - 1
                    successor.set_board()
                    succs.append(("{}:L".format(vehicle["id"]), successor))
                if (
                    x_position + vehicle["length"] < self.board_width
                    and self.board[y_position][x_position + vehicle["length"]] == " "
                ):
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    successor.vehicles[index]["x"] = x_position + 1
                    successor.set_board()
                    succs.append(("{}:R".format(vehicle["id"]), successor))

            else:
                if y_position > 0 and self.board[y_position - 1][x_position] == " ":
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    successor.vehicles[index]["y"] = y_position - 1
                    successor.set_board()
                    succs.append(("{}:U".format(vehicle["id"]), successor))

                if (
                    y_position + vehicle["length"] < self.board_height
                    and self.board[y_position + vehicle["length"]][x_position] == " "
                ):
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    successor.vehicles[index]["y"] = y_position + 1
                    successor.set_board()
                    succs.append(("{}:D".format(vehicle["id"]), successor))
        return succs
