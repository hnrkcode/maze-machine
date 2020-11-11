import os
import random

import pygame
from pygame.locals import *

import settings
from maze import Maze
from text import Text


def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.font.init()
    screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    clock = pygame.time.Clock()

    start_text = Text("Press ENTER to start", 50)
    reset_text = Text("Press R to reset", 50)
    center_start_text = (
        int(settings.WIDTH / 2 - start_text.rect.w / 2),
        start_text.rect.h,
    )
    center_reset_text = (
        int(settings.WIDTH / 2 - reset_text.rect.w / 2),
        reset_text.rect.h,
    )
    start_text.set_position(center_start_text)
    reset_text.set_position(center_reset_text)
    text_group = pygame.sprite.RenderUpdates(start_text)

    cell_size = settings.CELL_SIZE
    size_text = Text(f"cell size: {cell_size}", 20, (20, (settings.HEIGHT - settings.GRID_SIZE[1]) / 2))
    size_group = pygame.sprite.RenderUpdates(size_text)

    start = False
    maze = Maze(start, settings.GRID_POS, settings.GRID_SIZE, cell_size)

    while True:

        clock.tick(settings.FPS)
        screen.fill(settings.BG_COLOR)

        for event in pygame.event.get():

            # Exit the program.
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                return

            # Change cell size with scrolling.
            if event.type == MOUSEWHEEL:
                if event.y > 0 and cell_size < 100:
                    cell_size += 1
                if event.y < 0 and cell_size > 10:
                    cell_size -= 1

                start, maze = reset(text_group, start_text, maze, cell_size)
                size_text.update_text(f"cell size: {cell_size}")

            if event.type == KEYDOWN:

                # Start the algorithm.
                if event.key == K_RETURN:
                    start = (0, 0)
                    text_group.empty()
                    text_group.add(reset_text)

                # Reset maze and prepare to generate a new maze.
                if event.key == K_r:
                    start, maze = reset(text_group, start_text, maze, cell_size)

        if start:
            maze.grid, start = maze.visualize_maze(
                maze.grid,
                start,
                settings.GRID_POS,
                settings.GRID_SIZE,
                cell_size,
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

        if text_group:
            text_group.draw(screen)

        size_group.draw(screen)

        pygame.display.set_caption(f"Maze (fps: {int(clock.get_fps())})")
        pygame.display.update()


def reset(group, text, maze, size):
    """Reset grid."""

    start = False
    group.empty()
    group.add(text)
    maze = Maze(start, settings.GRID_POS, settings.GRID_SIZE, size)

    return start, maze


if __name__ == "__main__":
    main()
