import pygame


class Text(pygame.sprite.DirtySprite):
    def __init__(
        self,
        text,
        size,
        pos=(0, 0),
        color=(255, 255, 255),
    ):
        super().__init__()
        self.color = color
        self._font = pygame.font.Font(None, size)
        self.image = self._font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def set_pos(self, pos):
        self.rect.topleft = pos

    def center_pos(self, width):
        self.rect.topleft = (int(width / 2 - self.rect.w / 2), self.rect.h)

    def update_text(self, text):
        self.image = self._font.render(text, 1, self.color)