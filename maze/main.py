import os
import random

import pygame
from pygame.locals import *

try:
    from maze.algorithm.maze import HuntAndKillMaze as Maze
    from maze.algorithm.path import bfs, draw_path
    from maze.utils import settings
    from maze.utils.text import Text
except ModuleNotFoundError:
    from algorithm.maze import HuntAndKillMaze as Maze
    from utils import settings
    from utils.text import Text


def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.font.init()
    screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    clock = pygame.time.Clock()

    cell_size = settings.CELL_SIZE
    grid_size = list(settings.GRID_SIZE)
    h_key_held = False
    w_key_held = False
    start = False
    path = []

    start_text = Text(
        text="Press ENTER to start", size=settings.LARGE_TEXT, color=settings.TEXT_COLOR
    )
    start_text.center_pos(settings.WIDTH)

    reset_text = Text(
        text="Press R to reset", size=settings.LARGE_TEXT, color=settings.TEXT_COLOR
    )
    reset_text.center_pos(settings.WIDTH)

    texts = {
        "cell_size": Text(
            text=f"Cell: {cell_size}x{cell_size}",
            size=settings.MEDIUM_TEXT,
            color=settings.TEXT_COLOR,
        ),
        "grid_size": Text(
            text=f"Grid: {grid_size[0]}x{grid_size[1]}",
            size=settings.MEDIUM_TEXT,
            color=settings.TEXT_COLOR,
        ),
    }
    text_layout(texts, (20, (settings.HEIGHT - grid_size[1]) / 2), 20)

    text_group = pygame.sprite.RenderUpdates(start_text)
    size_group = pygame.sprite.RenderUpdates(texts.values())

    maze = Maze(start, settings.GRID_POS, grid_size, cell_size)

    while True:

        clock.tick(settings.FPS)
        screen.fill(settings.BG_COLOR)

        for event in pygame.event.get():

            # Exit the program.
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                return

            # Change cell size with scrolling.
            if event.type == MOUSEWHEEL and not h_key_held and not w_key_held:
                if grid_size[0] / cell_size > 1 and grid_size[1] / cell_size > 1:
                    if event.y > 0 and cell_size < settings.HIGHEST_CELL_SIZE:
                        cell_size += 1
                    if event.y < 0 and cell_size > settings.LOWEST_CELL_SIZE:
                        cell_size -= 1

                start, maze, grid_size, path = reset(
                    text_group, start_text, maze, cell_size, grid_size
                )
                texts["cell_size"].update_text(f"Cell: {cell_size}x{cell_size}")

            # Change grid width.
            if event.type == MOUSEWHEEL and w_key_held:
                if event.y > 0 and grid_size[0] < settings.GRID_WIDTH:
                    grid_size[0] += cell_size
                if event.y < 0 and (grid_size[0] - cell_size) > cell_size:
                    grid_size[0] -= cell_size

                start, maze, grid_size, path = reset(
                    text_group, start_text, maze, cell_size, grid_size
                )
                texts["grid_size"].update_text(f"Grid: {grid_size[0]}x{grid_size[1]}")

            # Change grid height.
            if event.type == MOUSEWHEEL and h_key_held:
                if event.y > 0 and grid_size[1] < settings.GRID_HEIGHT:
                    grid_size[1] += cell_size
                if event.y < 0 and (grid_size[1] - cell_size) > cell_size:
                    grid_size[1] -= cell_size

                start, maze, grid_size, path = reset(
                    text_group, start_text, maze, cell_size, grid_size
                )
                texts["grid_size"].update_text(f"Grid: {grid_size[0]}x{grid_size[1]}")

            if event.type == KEYDOWN:

                # Start the algorithm.
                if event.key == K_RETURN:
                    start = (0, 0)
                    text_group.empty()
                    text_group.add(reset_text)

                # Reset everything.
                if event.key == K_r:
                    cell_size = settings.CELL_SIZE
                    start, maze, grid_size, path = reset(
                        text_group, start_text, maze, cell_size, settings.GRID_SIZE
                    )
                    texts["cell_size"].update_text(f"Cell: {cell_size}x{cell_size}")
                    texts["grid_size"].update_text(
                        f"Grid: {grid_size[0]}x{grid_size[1]}"
                    )

                # Find the shortest path from start to finish.
                if event.key == K_s:
                    start_point = list(maze.grid)[0]
                    end_point = list(maze.grid)[-1]
                    path = bfs(maze.grid, start_point, end_point)

                if event.key == K_h:
                    h_key_held = True
                if event.key == K_w:
                    w_key_held = True

            if event.type == KEYUP:

                if event.key == K_h:
                    h_key_held = False
                if event.key == K_w:
                    w_key_held = False

        if start:
            maze.grid, start = maze.kill_mode(
                maze.grid,
                start,
                settings.GRID_POS,
                grid_size,
                cell_size,
            )

        if path:
            draw_path(screen, path, maze.grid, (255, 155, 55))

        # Draw all existing cell walls.
        draw_walls(screen, maze.grid, settings.GRID_COLOR)

        if text_group:
            text_group.draw(screen)

        size_group.draw(screen)

        pygame.display.set_caption(f"Maze (fps: {int(clock.get_fps())})")
        pygame.display.update()


def reset(group, text, maze, size, grid_size):
    """Reset grid."""

    start = False
    group.empty()
    group.add(text)
    maze = Maze(start, settings.GRID_POS, grid_size, size)
    grid_size = list(grid_size)
    path = []

    return start, maze, grid_size, path


def text_layout(texts, pos, spacing):
    """Set layout positions for text objects."""

    x, y = pos

    for text in texts.values():
        text.set_pos((x, y))
        y += spacing


def draw_walls(surface, grid, color):
    """Draw all existing walls."""

    for cell in grid.values():
        for direction in ["up", "right", "down", "left"]:
            if cell[direction]["wall"]:
                pygame.draw.line(
                    surface,
                    color,
                    cell[direction]["line"]["start"],
                    cell[direction]["line"]["end"],
                    width=1,
                )


if __name__ == "__main__":
    main()
