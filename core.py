import pygame as pg
from math import floor
from random import randint
import time

pg.init()

TOP    = [ 0,  1]
BOTTOM = [ 0, -1]
RIGHT  = [ 1,  0]
LEFT   = [-1,  0]

class Node():
    EMPTY = 0
    START = 1
    END = 2
    OPEN = 3
    CLOSED = 4
    WALL = 5
    PATH = 6
    COLORS = [[255, 255, 255],
              [255,   0,   0],
              [  0, 255,   0],
              [255, 255,   0],
              [255,   0, 255],
              [  0,   0,   0],
              [  0,   0, 255]]
    UNEXPLORED = False
    EXPLORED = True

    def __init__(self, pos: tuple[int, int], state: int = EMPTY):
        self.pos = pos
        self.state = state
        self.explored: bool = None
        self.g: int = None
        self.h: int = None
        self.f: int = None
        self.last: Node = None

    def get_last_recursive(self):
        nodes = []
        if self.last == None:
            return nodes
        nodes.extend(self.last.get_last_recursive())
        nodes.append(self)
        return nodes
    
    def set_explored(self, explored: bool) -> None:
        self.explored = explored
        self.state = [Node.OPEN, Node.CLOSED][explored]
    
    def get_color(self) -> list[int, int, int]:
        return Node.map_to_color(self.state)

    @classmethod
    def map_to_color(self, state: int) -> list[int, int, int]:
        return Node.COLORS[state]

class Grid():
    def __init__(self, size: int = 300, res: int = 12) -> None:
        self.screen = pg.display.set_mode((size, size))
        self.size = size
        self.running = True
        self.res = res
        self.interval = size / res
        self.line_offset = -.5
        self.line_thickness = 4

        self.grid: list[list[Node]] = self.init_grid()

        self.start = None
        self.end = None

        self.started = False
    
    def get_nodes_of_type(self, t: bool) -> list[Node]:
        return [node for line in self.grid for node in line if node.explored == t]
    
    def init_grid(self) -> list[Node]:
        nodes = []
        for y in range(self.res):
            line = []
            for x in range(self.res):
                line.append(Node((x, y)))
            nodes.append(line)
        return nodes
    
    def abs_to_coord(self, pos) -> tuple[int, int]:
        x, y = pos

        x /= self.size
        y /= self.size

        x *= self.res
        y *= self.res

        return (floor(x), floor(y))
    
    def update(self) -> None:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
            
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    if not self.start == None and not self.end == None:
                        self.started = True

                if e.key == pg.K_n:
                    for y in range(self.res):
                        for x in range(self.res):
                            node = self.grid[y][x]
                            overwriteable = [Node.WALL, Node.EMPTY, Node.OPEN, Node.CLOSED]
                            if node.state in overwriteable:
                                node.state = [Node.EMPTY, Node.WALL][randint(0,100) <= 25]
                
                if e.key == pg.K_ESCAPE:
                    self.started = False

                if e.key == pg.K_s:
                    self.save()
                
                if e.key == pg.K_l:
                    self.load()
            
        if pg.mouse.get_pressed()[0]:
            pos = pg.mouse.get_pos()
            pos = self.abs_to_coord(pos)
            node = self.grid[pos[1]][pos[0]]
            if node.state == Node.EMPTY:
                node.state = Node.WALL
            if self.start == None:
                node.state = Node.START
                self.start = node.pos
            if not node.state == Node.START and self.end == None:
                node.state = Node.END
                self.end = node.pos
        
        if pg.mouse.get_pressed()[2]:
            pos = pg.mouse.get_pos()
            pos = self.abs_to_coord(pos)
            node = self.grid[pos[1]][pos[0]]
            if node.state == Node.WALL:
                node.state = Node.EMPTY

        if self.started:
            self.grid[self.start[1]][self.start[0]].state = Node.START
            self.grid[self.end[1]][self.end[0]].state = Node.END

        self.render()

    def render(self) -> None:
        offset = self.line_offset
        thickness = self.line_thickness
        self.screen.fill(Node.map_to_color(Node.EMPTY))

        for y in range(self.res):
            for x in range(self.res):
                if not self.grid[y][x].state == Node.EMPTY:
                    pg.draw.rect(self.screen, self.grid[y][x].get_color(), pg.Rect(x*self.interval, y*self.interval, self.interval, self.interval))

        for y in range(self.res+1):
            pg.draw.line(self.screen, (50, 50, 50), (0, y*self.interval+offset), (self.size+offset, y*self.interval+offset), thickness)
            for x in range(self.res+1):
                pg.draw.line(self.screen, (50, 50, 50), (x*self.interval+offset, 0), (x*self.interval+offset, self.size+offset), thickness)
        
        pg.display.update()
    
    def load(self) -> None:
        with open('map.txt', 'r') as f:
            for y, line in enumerate(f.readlines()):
                for x, val in enumerate(line[:-1:]):
                    val = int(val)
                    self.grid[y][x].state = val
                    if val == Node.PATH:
                        self.started = True
                    if val == Node.START:
                        self.start = [x, y]
                    if val == Node.END:
                        self.end = [x, y]
        f.close()

    def save(self) -> None:
        with open('map.txt', 'w') as f:
            for line in self.grid:
                for node in line:
                    f.write(str(node.state))
                f.write('\n')
        f.close()

if __name__ == "__main__":
    window = Grid(900, 50)
    window.line_thickness = 2
    while window.running:
        window.update()