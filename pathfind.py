import sys

if len(sys.argv) == 1:
    print('Specify which algorithm to use!')
    exit(1)

if sys.argv[1] == '-dijkstra':
    from dijkstra import *
elif sys.argv[1] == '-astar':
    from astar import *
else:
    print(f'1st argument specifies algorithm, {sys.argv[1]} is not a valid option!')

window_size = 900
density = 50
line_width = 2

if len(sys.argv) == 5:
    window_size = int(sys.argv[2])
    density = int(sys.argv[3])
    line_width = int(sys.argv[4])

if __name__ == "__main__":
    window = core.Grid(window_size, density)
    window.line_thickness = line_width

    found = False
    path = None
    index = 0
    initialized = False
    finished = False

    while window.running:
        if window.started:
            
            if not initialized:
                initialize(window)
                t1 = core.time.time()
                initialized = True

            if not found:
                found = explore_next_node(window)
            elif path == None and found:
                path = window.grid[window.end[1]][window.end[0]].get_last_recursive()[::-1]
            elif index < len(path):
                path[index].state = core.Node.PATH
                index += 1
            elif not finished:
                print(f'Path completed in {round(core.time.time() - t1, 3)}s')
                finished = True

        elif initialized == True:
            found = False
            path = None
            index = 0
            initialized = False
            finished = False
            window.grid = window.init_grid()
            window.start = None
            window.end = None
        window.update()