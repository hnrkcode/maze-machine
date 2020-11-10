import random


class Maze:
    def __init__(self, start, grid_pos, grid_size, cell_size):
        self.w, self.h = int(grid_size[0] / cell_size), int(grid_size[0] / cell_size)
        # self.grid = self.kill_mode(start, grid_pos, grid_size, cell_size)
        self.grid = self.generate_grid(start, grid_pos, grid_size, cell_size)

    def visualize_maze(self, grid, pos, grid_pos, grid_size, cell_size):
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

    def kill_mode(self, pos, grid_pos, grid_size, cell_size):
        grid = self.generate_grid(pos, grid_pos, grid_size, cell_size)

        while True:

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
                    break

                grid[pos]["visited"] = True
                adjacents = self.get_adjacent(grid, pos, True)
                direction = random.choice(list(adjacents.keys()))
                grid[pos][direction] = False
                grid[adjacents[direction]][self.inverse(direction)] = False

        return grid

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

    def generate_grid(self, pos, grid_pos, grid_size, cell_size):
        """Create all cells in the grid."""

        cells = {}
        w, h = grid_size
        x, y = 0, 0
        dx, dy = 0 + grid_pos[0], 0 + grid_pos[1]

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
                x += 1
                dx += cell_size
            x = 0
            dx = 0 + grid_pos[0]
            dy += cell_size
            y += 1

        return cells

    def calc_lines(self, pos, size):
        x, y = pos
        w, h = size

        up = ((x, y), (x + w, y))
        right = ((x + w, y), (x + w, y + h))
        down = ((x, y + h), (x + w, y + h))
        left = ((x, y), (x, y + h))

        return [up, right, down, left]