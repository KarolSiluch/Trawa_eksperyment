import pygame
from gameplay.tiles.foundation import Foundation


class Tile(Foundation):
    class Sprite:
        def __init__(self, image: pygame.Surface, sort_y_offset: int = 0, **pos: tuple[int]) -> None:
            self._show = True
            self._master_image = image
            self._image = image
            rect: pygame.FRect = image.get_frect(**pos)
            self.pos = rect.center
            self._sort_y_offset = sort_y_offset
            self._render_offset = pygame.Vector2()

        def set_visibility(self, visible=True):
            self._show = visible

        def rotate(self, angle: int):
            self._image = pygame.transform.rotate(self._image, angle)

        def flip(self, flip_x: bool = False, flip_y: bool = False):
            self._image = pygame.transform.flip(self._image, flip_x, flip_y)

        def scale(self, scale: float):
            size_x = self._image.get_width() * scale
            size_y = self._image.get_height() * scale
            self._image = pygame.transform.scale(self._image, (size_x, size_y))

        def update(self):
            self._image = self._master_image

        @property
        def show(self): return self._show

        @property
        def sort_y_offset(self): return self._sort_y_offset

        @property
        def render_offset(self): return self._render_offset

        @property
        def image(self): return self._image

        @property
        def rect(self): return self._image.get_frect(center=self.pos)

    def __init__(self, groups, type: str, image: pygame.Surface, sort_y_offset: int = 0,
                 offgrid_tile: bool = False, z=5, special_flags=0, **pos: tuple[int]) -> None:
        self.sprite = self.Sprite(image, sort_y_offset, **pos)
        self.hitbox: pygame.FRect = image.get_frect(**pos)
        self.z = z
        self.special_flags = special_flags
        super().__init__(groups, type, offgrid_tile)

    def get_sprite(self):
        return (self.sprite.image, self.sprite.rect)

    def update(self, dt):
        self.sprite.update()
