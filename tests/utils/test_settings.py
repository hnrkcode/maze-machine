from maze.utils import settings


def test_fps():
    assert settings.FPS == 60


def test_width():
    assert settings.WIDTH == 1280


def test_height():
    assert settings.HEIGHT == 720


def test_window_size():
    assert settings.WINDOW_SIZE == (1280, 720)


def test_highest_cell_size():
    assert settings.HIGHEST_CELL_SIZE == 100


def test_lowest_cell_size():
    assert settings.LOWEST_CELL_SIZE == 10


def test_default_cell_size():
    assert settings.CELL_SIZE == 100


def test_grid_width():
    assert settings.GRID_WIDTH == 900


def test_grid_height():
    assert settings.GRID_HEIGHT == 500


def test_grid_size():
    assert settings.GRID_SIZE == (900, 500)


def test_grid_pos():
    pos = (
        int(settings.WIDTH / 2 - settings.GRID_WIDTH / 2),
        int(settings.HEIGHT / 2 - settings.GRID_HEIGHT / 2),
    )

    assert settings.GRID_POS == pos


def test_background_color():
    assert settings.BG_COLOR == (0, 0, 0)


def test_grid_color():
    assert settings.GRID_COLOR == (255, 255, 255)


def test_text_color():
    assert settings.TEXT_COLOR == (255, 255, 255)


def test_large_text_size():
    assert settings.LARGE_TEXT == 50


def test_medium_text_size():
    assert settings.MEDIUM_TEXT == 20