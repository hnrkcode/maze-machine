import os
import random
import pygame
from pygame.locals import *

FPS = 60
SCREEN_SIZE = WIDTH, HEIGHT = 1280, 720
CELL_SIZE = 100
GRID_SIZE = (900, 500)
GRID_POS = (int(WIDTH / 2 - GRID_SIZE[0] / 2), int(HEIGHT / 2 - GRID_SIZE[1] / 2))


def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    fps_text = Text(
        f"FPS: {int(clock.get_fps())}",
        35,
        (GRID_POS[0], GRID_POS[1] - 50),
        (255, 255, 255),
    )
    fps_group = pygame.sprite.RenderUpdates(fps_text)

    start_text = Text(
        "Press ENTER to start",
        25,
        (GRID_POS[0], GRID_POS[1] - 70),
        (255, 255, 255),
    )
    text_group = pygame.sprite.RenderUpdates(start_text)

    start = False
    maze = Maze(start, GRID_POS, GRID_SIZE, CELL_SIZE)

    while True:

        clock.tick(FPS)

        screen.fill((0, 0, 0))

        for event in pygame.event.get():

            # Exit the program.
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            if event.type == KEYDOWN and event.key == K_RETURN:
                start = (0, 0)

        if start:
            maze.grid, start = maze.visualize_maze(
                maze.grid, start, GRID_POS, GRID_SIZE, CELL_SIZE
            )

        # Draw all existing cell walls.
        for cell in maze.grid.values():
            if cell["up"]:
                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    cell["walls"][0][0],
                    cell["walls"][0][1],
                    width=1,
                )
            if cell["right"]:
                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    cell["walls"][1][0],
                    cell["walls"][1][1],
                    width=1,
                )
            if cell["down"]:
                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    cell["walls"][2][0],
                    cell["walls"][2][1],
                    width=1,
                )
            if cell["left"]:
                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    cell["walls"][3][0],
                    cell["walls"][3][1],
                    width=1,
                )

        fps_group.draw(screen)
        fps_group.update(f"FPS: {int(clock.get_fps())}")

        text_group.draw(screen)

        pygame.display.update()


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

        for row in range(int(h / cell_size)):
            for col in range(int(w / cell_size)):
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


class Text(pygame.sprite.DirtySprite):
    def __init__(
        self,
        text,
        size,
        pos,
        color,
    ):
        super().__init__()
        self.color = color
        self.text = text
        self.fontsize = size
        self._font = pygame.font.Font(None, size)
        self.image = self._font.render(text, 1, color)
        self.rect = pos

    def set_position(self, pos):
        self.rect = pos

    def update(self, text):
        self.image = self._font.render(text, 1, self.color)


if __name__ == "__main__":
    main()