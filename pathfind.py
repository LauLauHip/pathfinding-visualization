import sys

if sys.argv[1] == '-dijkstra':
    from dijkstra import *
elif sys.argv[1] == '-astar':
    from astar import *

if __name__ == "__main__":
    window = core.Grid(900, 50)

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