import pygame
import numpy as np
pygame.init()

win = pygame.display.set_mode((400, 400))  # Creates our screen object


class Node:
    def __init__(self, parent=None, position=None):
        self.g = 0
        self.f = 0
        self.h = 0
        self.parent = parent
        self.position = position

    def __eq__(self, other):
        return self.position == other.position

    def show(self, color):
        pygame.draw.rect(win, color, (self.position[1] * 20 + 2, self.position[0] * 20 + 2, 18, 18), 0)
        pygame.display.update()


def return_node(opened):
    f = np.inf
    temp = opened[0]
    for obj in opened:
        if obj.f < f:
            f = obj.f
            temp = obj
    return temp


def neighbours(node, nodes):
    neighbour = []
    for i in [(-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, -1), (-1, 1), (1, -1)]:
        obj = Node(node, (node.position[0]+i[0], node.position[1]+i[1]))
        x, y = obj.position
        if 19 >= x >= 0 and 19 >= y >= 0:
            if not nodes[x, y]:
                neighbour.append(obj)
    return neighbour


def get_h(a, b):
    x, y = a.position
    x1, y1 = b.position
    # return (x1-x)**2 + (y1-y)**2  # Euclidean
    return max(abs(x1-x), (y1-y))  # Diagonal 1
    '''d_max = max(abs(x1-x), (y1-y))
    d_min = min(abs(x1-x), (y1-y))
    return 14*d_min + 10*(d_max-d_min)  # Diagonal 2'''


def a_star(nodes, beg, end):
    beg_node = Node(None, beg)
    end_node = Node(None, end)
    opened = [beg_node]
    closed = []

    while opened:
        current_node = return_node(opened)
        a = current_node.position
        # print(current_node.position)
        # if current_node == end_node:
        if current_node.position == end_node.position:
            path = list()
            while current_node:
                # path.append(current_node.position)
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1]
        else:
            current_node = opened.pop(opened.index(current_node))
            b = current_node.position
            closed.append(current_node)
            for neighbor in neighbours(current_node, nodes):
                c = neighbor.position
                if neighbor not in closed:
                    x, y = neighbor.position
                    x1, y1 = current_node.position
                    if (x-x1, y-y1) in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        temp = current_node.g + 1
                    else:
                        temp = current_node.g + 1
                    if neighbor in opened:
                        if neighbor.g > temp:
                            neighbor.g = temp
                    else:
                        neighbor.g = temp
                        opened.append(neighbor)

                neighbor.h = get_h(neighbor, end_node)
                neighbor.f = neighbor.g + neighbor.h
                h = neighbor.h
                g = neighbor.g
                temp = 0
                pygame.time.delay(10)
                neighbor.show((153, 0, 153))


def draw_grid(w, surface):
    size = w // 20  # Gives us the distance between the lines

    x = 0  # Keeps track of the current x
    y = 0  # Keeps track of the current y
    for l in range(20):  # We will draw one vertical and one horizontal line each loop
        x = x + size
        y = y + size

        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, w))
        pygame.draw.line(surface, (0, 0, 0), (0, y), (w, y))


def redraw_window(surface):
    surface.fill((255, 255, 255))  # Fills the screen with black
    draw_grid(400, surface)  # Will draw our grid lines
    pygame.display.update()  # Updates the screen


def draw_path(p, beg, end):
    for obj in p:
        y, x = obj.position
        if (y, x) == end or (y, x) == beg:
            pygame.draw.rect(win, (0, 250, 0), (x * 20 + 2, y * 20 + 2, 18, 18), 0)
            pygame.display.update()
        else:
            pygame.draw.rect(win, (0, 0, 250), (x*20 + 2, y*20 + 2, 18, 18), 0)
            pygame.display.update()


def main():
    nodes = np.zeros((20, 20))
    redraw_window(win)
    points = []

    flag = True
    while flag:
        for event in pygame.event.get():

            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                x = x//20
                y = y//20
                nodes[y, x] = 1
                pygame.draw.rect(win, (200, 0, 0), (x * 20 + 2, y * 20 + 2, 18, 18), 0)
                pygame.display.update()
            if pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()
                x = x // 20
                y = y // 20
                points.append((y, x))
                pygame.draw.rect(win, (0, 200, 0), (x * 20 + 2, y * 20 + 2, 18, 18), 0)
                pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    flag = False

    p = a_star(nodes, points[0], points[1])
    # p = a_star(nodes, (3, 3), (5, 5))

    flag = True
    while flag:
        pygame.time.delay(50)  # This will delay the game so it doesn't run too quickly
        draw_path(p, points[0], points[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if user hit the red x
                pygame.quit()
                exit()


if __name__ == '__main__':
    main()