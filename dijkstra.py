import core

def initialize(grid: core.Grid):
    start_node = grid.grid[grid.start[1]][grid.start[0]]
    start_node.f = 0
    start_node.explored = False

def get_t(node: core.Node):
    return node.f

def explore_next_node(grid: core.Grid) -> bool:
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

        next_value = next_node.f + 1

        if neighbor.f == None or next_value < neighbor.f:
            neighbor.f = next_value
            neighbor.last = next_node
    
    return False