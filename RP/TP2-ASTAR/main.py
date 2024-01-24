from rush_hour_puzzle import RushHourPuzzle
from node import Node
from queue import Queue, PriorityQueue
import time
import pygame
from pygame.locals import *
import random

puzzle = RushHourPuzzle("1.csv")
for row in puzzle.board:
    print(" ".join(row))

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 100
GRID_ROWS, GRID_COLS = 6, 6

vehicle_colors = dict(X=(255, 0, 0))


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


for vehicle in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]:
    vehicle_colors[vehicle] = random_color()

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Rush Hour Puzzle")


title_font = pygame.font.SysFont("Arial", 42)


def draw(puzzle_):
    screen.fill((255, 255, 255))
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                1,
            )
    for vehicle in puzzle_.vehicles:
        x_position = vehicle["x"]
        y_position = vehicle["y"]
        width, height = (
            (GRID_SIZE * vehicle["length"], GRID_SIZE)
            if vehicle["orientation"] == "H"
            else (GRID_SIZE, GRID_SIZE * vehicle["length"])
        )
        color = vehicle_colors.get(vehicle["id"], (255, 255, 255))
        if width > height:
            pygame.draw.rect(
                screen,
                color,
                (x_position * GRID_SIZE, y_position * GRID_SIZE, width, height),
            )
        else:
            pygame.draw.rect(
                screen,
                color,
                (x_position * GRID_SIZE, y_position * GRID_SIZE, GRID_SIZE, height),
            )


solved = False


@staticmethod
def BFS(initial_state):
    initial_node = Node(initial_state)
    if initial_node.state.is_goal():
        return initial_node, 0
    open = Queue()
    open.put(initial_node)
    closed = list()
    step = 0
    while True:
        global solved
        time.sleep(0.03)
        print(f"step : {step} ")
        if open.empty():
            return None, step
        current = open.get()
        draw(current.state)

        closed.append(current)
        step += 1
        for action, successor in current.state.successorFunction():
            child = Node(successor, current, action)
            if child.state.board not in [
                node.state.board for node in closed
            ] and child.state.board not in [
                node.state.board for node in list(open.queue)
            ]:
                if child.state.is_goal():
                    solved = True
                    print("Goal reached")
                    draw(child.state)
                    draw_text(
                        "Steps : " + str(step), title_font, (255, 255, 255), 60, 50
                    )
                    return child, step
                open.put(child)
        screen.blit(screen, (0, 0))

        pygame.display.update()


@staticmethod
def a_star(initial_state, h):
    global solved
    open = PriorityQueue()
    closed = list()
    initial_node = Node(initial_state)
    initial_node.set_f(h)

    if initial_node.state.is_goal():
        return initial_node, 0

    open.put(initial_node)
    step = 0
    while True:
        time.sleep(0.01)
        print(f"step : {step}")
        current = open.get()
        draw(current.state)
        draw_text("step : " + str(step), title_font, (0, 0, 0), 60, 50)

        if current.state.is_goal():
            solved = True
            print("reached goal")
            draw(current.state)
            draw_text("step : " + str(step), title_font, (0, 0, 0), 60, 50)
            return current, step

        closed.append(current)
        step += 1

        for action, successor in current.state.successorFunction():
            child = Node(successor, current, action)
            child.set_f(h)

            if (child.state.board not in [node.state.board for node in closed]) and (
                child.state.board not in [node.state.board for node in list(open.queue)]
            ):
                open.put(child)
            else:
                if (
                    child.state.board in [node.state.board for node in list(open.queue)]
                ) and child.f >= current.f:
                    child = current  # remove this condition
                else:
                    if (
                        child.state.board in [node.state.board for node in closed]
                    ) and child.f < current.f:
                        if child in closed:
                            closed.remove(child)
                            open.put(child)
        screen.blit(screen, (0, 0))

        pygame.display.update()


def draw_text(text, font, text_col, x, y):
    image = font.render(text, True, text_col)
    screen.blit(image, (x, y))


isStarting = False
running = True
solved = False
while running:
    if not solved:
        screen.fill((255, 255, 255))
    if not isStarting:
        if not solved:
            solution = a_star(puzzle, 3)

    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

    pygame.display.update()


pygame.quit()
