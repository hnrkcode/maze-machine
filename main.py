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
        start_text.rect.h
    )
    center_reset_text = (
        int(settings.WIDTH / 2 - reset_text.rect.w / 2),
        reset_text.rect.h
    )
    start_text.set_position(center_start_text)
    reset_text.set_position(center_reset_text)
    text_group = pygame.sprite.RenderUpdates(start_text)

    start = False
    maze = Maze(start, settings.GRID_POS, settings.GRID_SIZE, settings.CELL_SIZE)

    while True:

        clock.tick(settings.FPS)
        screen.fill(settings.BG_COLOR)

        for event in pygame.event.get():

            # Exit the program.
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                return

            if event.type == KEYDOWN:

                # Start the algorithm.
                if event.key == K_RETURN:
                    start = (0, 0)
                    text_group.empty()
                    text_group.add(reset_text)
                
                # Reset maze and prepare to generate a new maze.
                if event.key == K_r:
                    start = False
                    text_group.empty()
                    text_group.add(start_text)
                    maze = Maze(start, settings.GRID_POS, settings.GRID_SIZE, settings.CELL_SIZE)

        if start:
            maze.grid, start = maze.visualize_maze(
                maze.grid,
                start,
                settings.GRID_POS,
                settings.GRID_SIZE,
                settings.CELL_SIZE,
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

        pygame.display.set_caption(f"Maze (fps: {int(clock.get_fps())})")
        pygame.display.update()


if __name__ == "__main__":
    main()
