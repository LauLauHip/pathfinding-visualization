import core

def initialize(grid: core.Grid):
    start_node = grid.grid[grid.start[1]][grid.start[0]]
    end_node = grid.grid[grid.end[1]][grid.end[0]]
    start_node.g = 0
    start_node.h = manhattan_distance(start_node.pos, end_node.pos)
    start_node.f = 0
    start_node.explored = False

def get_t(node: core.Node):
    return node.f

def manhattan_distance(pos1, pos2) -> int:
    dist1 = pos2[0] - pos1[0]
    dist2 = pos2[1] - pos1[1]
    return abs(dist1) + abs(dist2)

def explore_next_node(grid: core.Grid) -> bool:
    end_node = grid.grid[grid.end[1]][grid.end[0]]
    unexplored_nodes = grid.get_nodes_of_type(core.Node.UNEXPLORED)
    if len(unexplored_nodes) <= 0:
        return True

    next_node = sorted(unexplored_nodes, key=get_t)[0]

    next_node.set_explored(True)

    if next_node.pos == tuple(grid.end):
        return True
    
    for pos in (core.TOP, core.RIGHT, core.BOTTOM, core.LEFT):
        x = next_node.pos[0] + pos[0]
        y = next_node.pos[1] + pos[1]
        if x < 0 or x >= grid.res or y < 0 or y >= grid.res:
            continue

        neighbor = grid.grid[y][x]

        if neighbor.state == core.Node.WALL or neighbor.explored == True:
            continue

        neighbor.set_explored(False)

        g = next_node.g + 1
        h = manhattan_distance(neighbor.pos, end_node.pos)
        f = g + h

        if neighbor.f == None or f < neighbor.f:
            neighbor.f = f
            neighbor.g = g
            neighbor.h = h
            neighbor.last = next_node
    
    return False