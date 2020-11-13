import pygame


def bfs(grid, start, end):
    """Breadth first search algorithm."""

    prev = solve(start, grid)

    return reconstruct_path(grid, start, end, prev)


def solve(start, grid):
    """Solves the maze."""

    queue = []
    queue.append(start)

    i = list(grid).index(start)

    visited = [False for _ in range(len(grid))]
    visited[i] = True

    prev = [None for _ in range(len(grid))]

    while len(queue):
        node = queue.pop(0)
        neighbours = get_adjacent(grid, node)

        for neighbour in neighbours:
            i = list(grid).index(neighbour)
            if not visited[i]:
                queue.append(neighbour)
                visited[i] = True
                prev[i] = node

    return prev


def reconstruct_path(grid, start, end, prev):
    """Returns list with points that follow the shortest path."""

    path = []

    at = list(grid).index(end)

    while at != None:
        path.append(list(grid)[at])
        try:
            at = list(grid).index(prev[at])
        except ValueError:
            at = None

    path.reverse()

    if start == path[0]:
        return path

    return []


def get_adjacent(grid, pos):
    """Return dictionary with adjacent cells."""

    x, y = pos[0], pos[1]

    adjacents = []

    for direction in ["up", "right", "down", "left"]:
        if not grid[pos][direction]["wall"]:
            if direction == "up":
                adjacents.append((x, y - 1))
            if direction == "right":
                adjacents.append((x + 1, y))
            if direction == "down":
                adjacents.append((x, y + 1))
            if direction == "left":
                adjacents.append((x - 1, y))

    return adjacents


def draw_path(surface, positions, grid, color):
    """Draw line to show the shortest path from start to finish."""

    points = []

    for pos in positions:
        x, y = grid[pos]["up"]["line"]["start"]
        w = grid[pos]["up"]["line"]["end"][0] - grid[pos]["up"]["line"]["start"][0]
        h = grid[pos]["left"]["line"]["end"][1] - grid[pos]["left"]["line"]["start"][1]

        points.append((x + w // 2, y + h // 2))

    pygame.draw.lines(surface, color, False, points, width=3)