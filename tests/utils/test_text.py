import pytest
import pygame
from maze.utils.text import Text


@pytest.fixture
def text_object():

    pygame.font.init()
    text = Text("test", 20, (10, 10), (12, 12, 12))

    return text


class TestText:
    def test_color(self, text_object):
        assert text_object.color == (12, 12, 12)

    def test_pos(self, text_object):
        assert text_object.rect.topleft == (10, 10)

    def test_set_pos(self, text_object):

        pos = (100, 200)
        text_object.set_pos(pos)

        assert text_object.rect.topleft == pos

    def test_center_pos(self, text_object):

        width = 1280
        expected_result = (int(width / 2 - text_object.rect.w / 2), text_object.rect.h)
        text_object.center_pos(width)

        assert text_object.rect.topleft == expected_result