import random

try:
    from maze.utils import settings
except ModuleNotFoundError:
    from utils import settings


class HuntAndKillMaze:
    def __init__(self, start, grid_pos, grid_size, cell_size):
        """Initialize the grid."""

        self.grid = self._generate_grid(grid_size, cell_size)

    def kill_mode(self, grid, pos, grid_pos, grid_size, cell_size):
        """Open passages to unvisited neighbors, until the current cell has no unvisited neighbors."""

        adjacents = self._get_adjacent(grid, grid_size, cell_size, pos)
        direction = self._get_direction(adjacents)

        if direction in ["up", "right", "down", "left"]:
            grid[pos][direction] = False
            grid[pos]["visited"] = True
            pos = adjacents[direction]
            grid[pos][self._inverse(direction)] = False
            grid[pos]["visited"] = True
        else:
            pos = self._hunt_mode(grid, grid_size, cell_size)

            if pos:
                grid[pos]["visited"] = True
                adjacents = self._get_adjacent(grid, grid_size, cell_size, pos, True)
                direction = self._get_direction(adjacents)
                grid[pos][direction] = False
                grid[adjacents[direction]][self._inverse(direction)] = False

        return grid, pos

    def _hunt_mode(self, grid, grid_size, cell_size):
        """Scan the grid for an unvisited cell that is adjacent to a visited cell."""

        for key, value in grid.items():
            adjacents = self._get_adjacent(grid, grid_size, cell_size, key, True)
            if not value["visited"] and adjacents:
                return key

        return False

    def _get_direction(self, adjacents):
        """Return random direction."""

        try:
            direction = random.choice(list(adjacents))
        except IndexError:
            direction = None

        return direction

    def _inverse(self, direction):
        """Return the inverse direction."""

        if direction == "up":
            direction = "down"
        elif direction == "down":
            direction = "up"
        elif direction == "left":
            direction = "right"
        elif direction == "right":
            direction = "left"

        return direction

    def _get_adjacent(self, grid, grid_size, cell_size, pos, visited=False):
        """Return dictionary with adjacent cells."""

        adjacents = {}
        w, h = int(grid_size[0] / cell_size), int(grid_size[1] / cell_size)
        x, y = pos

        if y > 0 and grid[(x, y - 1)]["visited"] == visited:
            adjacents["up"] = (x, y - 1)

        if x < w - 1 and grid[(x + 1, y)]["visited"] == visited:
            adjacents["right"] = (x + 1, y)

        if y < h - 1 and grid[(x, y + 1)]["visited"] == visited:
            adjacents["down"] = (x, y + 1)

        if x > 0 and grid[(x - 1, y)]["visited"] == visited:
            adjacents["left"] = (x - 1, y)

        return adjacents

    def _generate_grid(self, grid_size, cell_size):
        """Create all cells in the grid."""

        cells = {}
        x, y = 0, 0
        w, h = grid_size
        grid_pos = self._calc_grid_pos(grid_size)
        dx, dy = self._calc_dx(grid_pos, grid_size, cell_size), grid_pos[1]

        for _ in range(int(h / cell_size)):
            for _ in range(int(w / cell_size)):
                cells[(x, y)] = {
                    "up": True,
                    "right": True,
                    "down": True,
                    "left": True,
                    "visited": False,
                    "walls": self._calc_lines((dx, dy), (cell_size, cell_size)),
                }

                x, dx = (x + 1), (dx + cell_size)

            x, y = 0, (y + 1)
            dx, dy = self._calc_dx(grid_pos, grid_size, cell_size), (dy + cell_size)

        return cells

    def _calc_grid_pos(self, grid_size):
        """Position grid in the center of the window."""

        x = int(settings.WIDTH / 2 - grid_size[0] / 2)
        y = int(settings.HEIGHT / 2 - grid_size[1] / 2)

        return (x, y)

    def _calc_dx(self, pos, size, cell):
        """Keeps the grid horizontally centered on the screen."""

        x = pos[0]
        w = size[0]
        dx = x + int((w - cell * int(w / cell)) / 2)

        return dx

    def _calc_lines(self, pos, size):
        """Calculate start and end points of line segments of a cell."""

        x, y = pos
        w, h = size

        # These lines segments creates a square.
        up = ((x, y), (x + w, y))
        right = ((x + w, y), (x + w, y + h))
        down = ((x, y + h), (x + w, y + h))
        left = ((x, y), (x, y + h))

        return [up, right, down, left]
