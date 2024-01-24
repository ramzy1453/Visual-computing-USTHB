from math import inf
import pygame
import time

MAX, MIN = +1, -1
width, height = 800, 600


class Play:
    @staticmethod
    def minimax(node, depth, player=MAX):
        pass

    @staticmethod
    def minimaxAlphaBetaPruning(screen, node, depth, alpha=-inf, beta=+inf, player=MAX):
        pass


class Node:
    def __init__(self, parent=None, side=None, depth=0, value=None) -> None:
        self.parent = parent
        self.value = value
        self.path = None
        self.leftChild = None

        if self.parent == None:
            self.position = (width // 2, 10)
        else:
            if side == "L":
                self.position = (
                    self.parent.position[0] // 2,
                    self.parent.position[1] + 20,
                )
            else:
                self.position = (
                    width // 2 + self.parent.position[0] // 2,
                    self.parent.position[1] + 20,
                )

    def display(self, color, player):
        if player:
            pass
        else:
            pass


class Tree:
    def __init__(self) -> None:
        self.root_node = Node(parent=None)

    def createEmptyTree(self, node, depth, values):
        leftNode = Node(node, "L", depth + 1, -2)
        rightNode = Node(node, "R", depth + 1, 2)

    def drawTree(self, node, depth, player):
        pass


def main():
    pygame.init()

    global screen
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("MiniMax Algorithm")

    tree = Tree()
    values = [10, 5, 7, 11, 12, 8, 9, 8, 5, 12, 11, 12, 9, 8, 7, 10]
    depth = 4

    running = True
    draw = True

    while running:
        screen.fill((192, 192, 192))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if draw == True:
            tree.createEmptyTree(tree.root_node, depth, values)
            tree.drawTree(tree.root_node, depth, player=MAX)
            pygame.display.update()
            time.sleep(1.5)
            draw = 1.5


if __name__ == "__main__":
    main()
