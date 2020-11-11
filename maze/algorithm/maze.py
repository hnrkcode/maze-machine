import random

try:
    from maze.utils import settings
except ModuleNotFoundError:
    from utils import settings


class HuntAndKillMaze:
    def __init__(self, start, grid_pos, grid_size, cell_size):
        self.w, self.h = int(grid_size[0] / cell_size), int(grid_size[0] / cell_size)
        self.grid = self.generate_grid(grid_size, cell_size)

    def kill_mode(self, grid, pos, grid_pos, grid_size, cell_size):
        adjacents = self.get_adjacent(grid, pos)

        try:
            direction = random.choice(list(adjacents.keys()))
        except IndexError:
            direction = "stop"

        if direction == "up":
            grid[pos]["up"] = False
            grid[pos]["visited"] = True
            pos = adjacents[direction]
            grid[pos]["down"] = False
            grid[pos]["visited"] = True
        elif direction == "right":
            grid[pos]["right"] = False
            grid[pos]["visited"] = True
            pos = adjacents[direction]
            grid[pos]["left"] = False
            grid[pos]["visited"] = True
        elif direction == "down":
            grid[pos]["down"] = False
            grid[pos]["visited"] = True
            pos = adjacents[direction]
            grid[pos]["up"] = False
            grid[pos]["visited"] = True
        elif direction == "left":
            grid[pos]["left"] = False
            grid[pos]["visited"] = True
            pos = adjacents[direction]
            grid[pos]["right"] = False
            grid[pos]["visited"] = True
        else:
            pos = self.hunt_mode(grid)

            if pos == False:
                return grid, pos

            grid[pos]["visited"] = True
            adjacents = self.get_adjacent(grid, pos, True)
            direction = random.choice(list(adjacents.keys()))
            grid[pos][direction] = False
            grid[adjacents[direction]][self.inverse(direction)] = False

        return grid, pos

    def hunt_mode(self, grid):

        for key, value in grid.items():
            adjacents = self.get_adjacent(grid, key, True)
            if not value["visited"] and adjacents:
                return key

        return False

    def inverse(self, direction):
        if direction == "up":
            return "down"
        if direction == "down":
            return "up"
        if direction == "left":
            return "right"
        if direction == "right":
            return "left"

    def get_adjacent(self, grid, pos, visited=False):

        x, y = pos

        adjacents = {}

        try:
            if y > 0 and grid[(x, y - 1)]["visited"] == visited:
                adjacents["up"] = (x, y - 1)
        except KeyError:
            pass

        try:
            if x < self.w - 1 and grid[(x + 1, y)]["visited"] == visited:
                adjacents["right"] = (x + 1, y)
        except KeyError:
            pass

        try:
            if y < self.h - 1 and grid[(x, y + 1)]["visited"] == visited:
                adjacents["down"] = (x, y + 1)
        except KeyError:
            pass

        try:
            if x > 0 and grid[(x - 1, y)]["visited"] == visited:
                adjacents["left"] = (x - 1, y)
        except KeyError:
            pass

        return adjacents

    def generate_grid(self, grid_size, cell_size):
        """Create all cells in the grid."""

        cells = {}
        grid_pos = self.calc_grid_pos(grid_size)
        w, h = grid_size
        x, y = 0, 0
        dx, dy = self.calc_dx(grid_pos, grid_size, cell_size), grid_pos[1]

        for _ in range(int(h / cell_size)):
            for _ in range(int(w / cell_size)):
                cells[(x, y)] = {
                    "up": True,
                    "right": True,
                    "down": True,
                    "left": True,
                    "visited": False,
                    "walls": self.calc_lines((dx, dy), (cell_size, cell_size)),
                }

                x, dx = (x + 1), (dx + cell_size)

            x, y = 0, (y + 1)
            dx, dy = self.calc_dx(grid_pos, grid_size, cell_size), (dy + cell_size)

        return cells

    def calc_grid_pos(self, grid_size):
        """Position grid in the center of the window."""

        x = int(settings.WIDTH / 2 - grid_size[0] / 2)
        y = int(settings.HEIGHT / 2 - grid_size[1] / 2)

        return (x, y)

    def calc_dx(self, pos, size, cell):
        """Keeps the grid horizontally centered on the screen."""

        x = pos[0]
        w = size[0]
        dx = x + int((w - cell * int(w / cell)) / 2)

        return dx

    def calc_lines(self, pos, size):
        x, y = pos
        w, h = size

        up = ((x, y), (x + w, y))
        right = ((x + w, y), (x + w, y + h))
        down = ((x, y + h), (x + w, y + h))
        left = ((x, y), (x, y + h))

        return [up, right, down, left]
